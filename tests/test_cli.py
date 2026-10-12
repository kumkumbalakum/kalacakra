import unittest
import os
import sys

ROOTFS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rootfs"))
LIB_PATH = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "lib")
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)


def iter_python_cli_scripts():
    """Kembalikan path script Python di rootfs/usr/bin (lewati yang shebang bash/dll)."""
    bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
    for name in sorted(os.listdir(bin_dir)):
        path = os.path.join(bin_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                first = f.readline()
        except (UnicodeDecodeError, OSError):
            continue
        if first.startswith("#!") and "python" in first:
            yield path

from kalacakra_common import (
    get_locale_strings,
    redact_secrets,
    is_dangerous_command,
    extract_target_packages,
    resolve_locales_dir,
    SECRET_PATTERNS
)

class TestKalacakraCommon(unittest.TestCase):
    def test_locales_resolution_and_content(self):
        locales_dir = resolve_locales_dir()
        self.assertTrue(os.path.isdir(locales_dir), f"Locales directory {locales_dir} should exist")
        
        required_keys = [
            "interceptor_title",
            "ai_safety_warning",
            "doctor_header",
            "doctor_label_btrfs",
            "ai_dangerous_warning",
            "rewind_header",
            "beam_header",
            "portal_ready",
            "ocr_copied",
            "survival_enabled",
            "precache_header",
            "preview_header",
            "spotlight_calculating",
            "flow_starting",
            "snippet_added",
            "keyring_configured",
            "hub_header",
            "qa_header",
            "qa_passed",
            "snapboot_header",
            "snapboot_synced",
            "profile_header",
            "profile_applied",
            "pkg_header",
            "pkg_installing",
            "jail_header",
            "jail_running",
            "be_header",
            "be_activated",
            "scrub_header",
            "scrub_healthy",
            "trace_header",
            "sysrc_header",
            "sysrc_updated",
            "unveil_header",
            "unveil_running",
            "signify_header",
            "signify_verified",
            "pf_header",
            "pf_panic",
            "doas_header",
            "doas_verified",
            "wx_header",
            "wx_compliant"
        ]

        for lang in ["id", "en"]:
            strings, resolved_lang = get_locale_strings(lang)
            self.assertEqual(resolved_lang, lang)
            for k in required_keys:
                self.assertIn(k, strings, f"Key '{k}' must exist in {lang}.json")

    def test_secret_redaction(self):
        sample_gh = "Run deploy script with token ghp_123456789012345678901234567890123456"
        redacted, had_secret = redact_secrets(sample_gh)
        self.assertTrue(had_secret)
        self.assertNotIn("ghp_123456789012345678901234567890123456", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)

        sample_aws = "Error accessing S3 with key AKIAIOSFODNN7EXAMPLE"
        redacted_aws, had_aws = redact_secrets(sample_aws)
        self.assertTrue(had_aws)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", redacted_aws)
        self.assertIn("[REDACTED_SECRET]", redacted_aws)

        clean_text = "find . -type f -name '*.txt'"
        clean_res, clean_flag = redact_secrets(clean_text)
        self.assertFalse(clean_flag)
        self.assertEqual(clean_res, clean_text)

    def test_dangerous_command_detection(self):
        self.assertTrue(is_dangerous_command("rm -rf /"))
        self.assertTrue(is_dangerous_command("rm -rf / --no-preserve-root"))
        self.assertTrue(is_dangerous_command("mkfs.ext4 /dev/sda1"))
        self.assertTrue(is_dangerous_command(":(){ :|:& };:"))
        # Pola tambahan: rm rekursif ke root/home/glob
        self.assertTrue(is_dangerous_command("rm -rf /*"))
        self.assertTrue(is_dangerous_command("rm -rf ~"))
        self.assertTrue(is_dangerous_command("rm -rf $HOME"))
        self.assertTrue(is_dangerous_command("rm -rf /var/lib"))
        self.assertTrue(is_dangerous_command("sudo rm -rf /tmp/cache"))
        self.assertTrue(is_dangerous_command("rm -fr /home"))
        # Bukan berbahaya
        self.assertFalse(is_dangerous_command("ls -la /tmp"))
        self.assertFalse(is_dangerous_command("podman run alpine echo hello"))
        self.assertFalse(is_dangerous_command("rm -f build.log"))
        self.assertFalse(is_dangerous_command("rm file.txt"))

    def test_package_extractor_multi_package(self):
        res1 = extract_target_packages(["install", "-y", "vlc", "ffmpeg", "mpv"])
        self.assertEqual(res1, ["vlc", "ffmpeg", "mpv"])

        res2 = extract_target_packages(["-S", "--noconfirm", "neovim", "ripgrep"])
        self.assertEqual(res2, ["neovim", "ripgrep"])

        res3 = extract_target_packages(["update"])
        self.assertEqual(res3, [])


class TestRepoConsistency(unittest.TestCase):
    def test_justfile_root_and_rootfs_in_sync(self):
        """Justfile (root) dan rootfs/usr/share/kalacakra/Justfile harus identik
        agar image OCI selalu memakai resep yang sama dengan repo."""
        REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        root_just = os.path.join(REPO_DIR, "Justfile")
        rootfs_just = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "Justfile")

        self.assertTrue(os.path.isfile(root_just), "Justfile di root repo harus ada")
        self.assertTrue(os.path.isfile(rootfs_just), "Justfile di rootfs harus ada (di-copy ke image)")

        with open(root_just, "r", encoding="utf-8") as f1, open(rootfs_just, "r", encoding="utf-8") as f2:
            self.assertEqual(
                f1.read(), f2.read(),
                "Justfile root dan rootfs tidak sinkron! Jalankan: cp Justfile rootfs/usr/share/kalacakra/Justfile"
            )

    def test_k_doctor_clean_without_container_tools(self):
        """k-doctor --clean tidak boleh crash jika podman/flatpak tidak tersedia."""
        import subprocess, tempfile
        doctor_path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-doctor")
        with tempfile.TemporaryDirectory() as empty_bin:
            env = os.environ.copy()
            env["PATH"] = empty_bin
            env["LANG"] = "en_US.UTF-8"
            res = subprocess.run(
                [sys.executable, doctor_path, "--clean"],
                capture_output=True, text=True, env=env, timeout=30
            )
        self.assertEqual(res.returncode, 0, f"stderr: {res.stderr}")
        self.assertNotIn("Traceback", res.stderr)

    def test_all_locale_keys_used_by_cli_exist(self):
        """Setiap strings.get(\"key\") di seluruh CLI harus tersedia di locale id & en.
        Menangkap regresi key hilang seperti yang pernah terjadi pada label k-doctor."""
        import re
        import json
        bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
        used_keys = set()
        for name in os.listdir(bin_dir):
            path = os.path.join(bin_dir, name)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        used_keys |= set(re.findall(r'strings\.get\("([^"]+)"', f.read()))
                except (UnicodeDecodeError, OSError):
                    continue
        self.assertTrue(used_keys, "Tidak ada key strings.get ditemukan - pola tes mungkin rusak")

        for lang in ("id", "en"):
            path = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "locales", f"{lang}.json")
            with open(path, "r", encoding="utf-8") as f:
                locale_keys = set(json.load(f).keys())
            missing = used_keys - locale_keys
            self.assertFalse(missing, f"Key hilang di {lang}.json: {sorted(missing)}")

    def test_new_cli_scripts_compile(self):
        """Semua tool di rootfs/usr/bin wajib lolos py_compile (cek sintaks dasar)."""
        import py_compile
        import tempfile
        bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
        failures = []
        with tempfile.TemporaryDirectory() as tmp:
            for name in sorted(os.listdir(bin_dir)):
                path = os.path.join(bin_dir, name)
                if not os.path.isfile(path):
                    continue
                with open(path, "rb") as fh:
                    first_line = fh.readline()
                if b"python" not in first_line:
                    continue
                try:
                    py_compile.compile(path, cfile=os.path.join(tmp, name + ".pyc"), doraise=True)
                except py_compile.PyCompileError as e:
                    failures.append(str(e))
        self.assertFalse(failures, "Script gagal compile:\n" + "\n".join(failures))

    def test_no_undefined_names(self):
        """Tangkap undefined name (mis. 'shutil' terpakai tapi tak di-import) via pyflakes.
        Skip jika pyflakes tidak terpasang - CI selalu menginstalnya."""
        try:
            from pyflakes.api import checkPath
            from pyflakes.reporter import Reporter
        except ImportError:
            self.skipTest("pyflakes tidak terpasang")
        import io
        bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
        problems = []
        for name in sorted(os.listdir(bin_dir)):
            path = os.path.join(bin_dir, name)
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as fh:
                first_line = fh.readline()
            if b"python" not in first_line:
                continue
            warn_stream, err_stream = io.StringIO(), io.StringIO()
            reporter = Reporter(warn_stream, err_stream)
            checkPath(path, reporter)
            output = warn_stream.getvalue()
            for line in output.splitlines():
                if "undefined name" in line:
                    problems.append(f"{name}: {line.strip()}")
        self.assertFalse(problems, "Undefined name ditemukan:\n" + "\n".join(problems))

    def test_desktop_exec_targets_exist(self):
        """Setiap binary yang dipanggil berkas .desktop harus ada di rootfs/usr/bin
        ATAU ada di allowlist dependensi eksternal yang dinyatakan eksplisit.

        Menangkap phantom dependency seperti Exec=umu-run (biner polos, tidak
        dipasang di image) - nama biner polos TANPA path absolut tidak boleh
        dipakai, karena tidak bisa diverifikasi."""
        import glob
        # Allowlist: biner eksternal yang SUDAH dipastikan ada di base image
        # (kinoite-main) atau diinstal di Containerfile. Nama lain harus lewat
        # wrapper /usr/bin/k-* milik kita agar bisa diverifikasi.
        ALLOWED_EXTERNAL = {
            "bash", "sh",          # shell bawaan
            "env",
        }

        own_scripts = set(os.listdir(os.path.join(ROOTFS_DIR, "usr", "bin")))
        desktop_files = (
            glob.glob(os.path.join(ROOTFS_DIR, "usr", "share", "applications", "*.desktop")) +
            glob.glob(os.path.join(ROOTFS_DIR, "usr", "share", "kio", "servicemenus", "*.desktop"))
        )
        self.assertTrue(desktop_files, "Tidak ada berkas .desktop ditemukan - pola tes mungkin rusak")

        problems = []
        for df in desktop_files:
            with open(df, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("Exec="):
                        continue
                    target = line.strip().split("=", 1)[1].split()[0]
                    base = target.rsplit("/", 1)[-1]
                    if base in ALLOWED_EXTERNAL:
                        continue
                    if target.startswith("/usr/bin/"):
                        if base not in own_scripts:
                            problems.append(f"{os.path.basename(df)} -> {target} (path absolut, script tak ada)")
                    else:
                        problems.append(
                            f"{os.path.basename(df)} -> '{target}' (biner polos tak terverifikasi; "
                            f"pakai wrapper /usr/bin/k-* atau tambahkan ke allowlist)"
                        )
        self.assertFalse(
            problems,
            "Exec berisiko phantom dependency:\n" + "\n".join(problems)
        )

    def test_dispatcher_references_exist(self):
        """Semua find_bin(\"k-x\") di dispatcher harus menunjuk file yang ada."""
        import re
        dispatcher = os.path.join(ROOTFS_DIR, "usr", "bin", "kalacakra")
        with open(dispatcher, "r", encoding="utf-8") as f:
            refs = set(re.findall(r'find_bin\("([a-z0-9._-]+)"\)', f.read()))
        self.assertTrue(refs, "Tidak ada find_bin() ditemukan - pola tes mungkin rusak")

        own_scripts = set(os.listdir(os.path.join(ROOTFS_DIR, "usr", "bin")))
        missing = sorted(refs - own_scripts)
        self.assertFalse(
            missing,
            f"find_bin() merujuk tool yang tidak ada di rootfs/usr/bin: {missing}"
        )

    def test_containerfiles_chmod_all_cli_scripts(self):
        """Setiap script di rootfs/usr/bin harus ada di daftar chmod Containerfile
        (kedua varian identik), agar tool baru tidak kehilangan bit eksekusi."""
        import re
        scripts = {n for n in os.listdir(os.path.join(ROOTFS_DIR, "usr", "bin"))
                   if os.path.isfile(os.path.join(ROOTFS_DIR, "usr", "bin", n))}
        REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        for cf in ("Containerfile", "Containerfile.nvidia"):
            path = os.path.join(REPO_DIR, cf)
            self.assertTrue(os.path.isfile(path), f"{cf} harus ada")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            listed = set(re.findall(r"/usr/bin/([A-Za-z0-9._-]+)", content))
            missing = sorted(scripts - listed)
            self.assertFalse(
                missing,
                f"{cf}: script berikut tidak ada di daftar chmod: {missing}"
            )


def load_cli_module(name):
    """Muat script CLI tanpa ekstensi .py sebagai modul Python importable.
    Wajib memakai SourceFileLoader eksplisit karena nama file tanpa .py."""
    import importlib.util
    from importlib.machinery import SourceFileLoader
    path = os.path.join(ROOTFS_DIR, "usr", "bin", name)
    loader = SourceFileLoader(f"kalacakra_cli_{name}", path)
    spec = importlib.util.spec_from_loader(f"kalacakra_cli_{name}", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestKQASync(unittest.TestCase):
    def test_k_qa_expected_bins_matches_actual_bin_dir(self):
        """Daftar expected_bins di k-qa harus persis sama dengan isi rootfs/usr/bin.
        Mencegah tool baru (mis. k-voice/k-game) luput dari verifikasi QA."""
        import re
        bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
        actual = {n for n in os.listdir(bin_dir) if os.path.isfile(os.path.join(bin_dir, n))}

        qa_path = os.path.join(bin_dir, "k-qa")
        with open(qa_path, "r", encoding="utf-8") as f:
            content = f.read()
        block = re.search(r"expected_bins = \[(.*?)\]", content, re.DOTALL)
        self.assertIsNotNone(block, "expected_bins tidak ditemukan di k-qa")
        listed = set(re.findall(r'"([^"]+)"', block.group(1)))

        self.assertEqual(
            listed, actual,
            f"k-qa expected_bins tidak sinkron dengan rootfs/usr/bin. "
            f"Kurang: {sorted(actual - listed)} | Berlebih: {sorted(listed - actual)}"
        )


class TestPureLogicUnits(unittest.TestCase):
    """Unit test untuk logika murni yang tidak butuh sistem berjalan."""

    def test_wx_parse_elf_self_and_system(self):
        """k-wx.parse_elf harus mengenali ELF asli (pakai biner sistem /usr/bin/ls)."""
        kwx = load_cli_module("k-wx")
        target = "/usr/bin/ls"
        if not os.path.isfile(target):
            self.skipTest("/usr/bin/ls tidak ada")
        res = kwx.parse_elf(target)
        self.assertTrue(res["is_elf"], "ls harus terdeteksi sebagai ELF")
        self.assertEqual(res["compliant"], len(res["wx_violations"]) == 0 and not res["exec_stack"])

        # File non-ELF harus ditandai jujur
        non_elf = load_cli_module("k-wx").parse_elf(__file__)
        self.assertFalse(non_elf["is_elf"])

    def test_wx_parse_elf_missing_file(self):
        kwx = load_cli_module("k-wx")
        res = kwx.parse_elf("/nonexistent/binary/xyz")
        self.assertFalse(res["is_elf"])

    def test_spotlight_math_evaluation(self):
        ks = load_cli_module("k-spotlight")
        self.assertIn("4", ks.evaluate_math("2 + 2"))
        self.assertIn("2", ks.evaluate_math("4 / 2"))
        # Ekspresi berbahaya dibersihkan: tidak boleh mengeksekusi kode arbitrer
        self.assertIsNone(ks.evaluate_math("__import__('os').system('echo pwn')"))

    def test_spotlight_unit_conversion(self):
        ks = load_cli_module("k-spotlight")
        conv = ks.evaluate_conversion("100 usd to idr")
        self.assertIsNotNone(conv)
        self.assertIn("Rp", conv)
        temp = ks.evaluate_conversion("100 c to f")
        self.assertIsNotNone(temp)

    def test_signify_ed25519_roundtrip(self):
        """Ed25519 pure-python harus tahan verifikasi: sign lalu verify, dan
        tanda tangan harus GAGAL untuk pesan yang dimodifikasi (anti-tamper)."""
        ksig = load_cli_module("k-signify")
        sk = bytes(range(32))
        pk = ksig.ed25519_publickey(sk)
        self.assertEqual(len(pk), 32)

        msg = b"Kalacakra OS - integritas berkas"
        sig = ksig.ed25519_sign(msg, sk, pk)
        self.assertEqual(len(sig), 64)
        self.assertTrue(ksig.ed25519_verify(sig, msg, pk))
        self.assertFalse(ksig.ed25519_verify(sig, msg + b"tampered", pk))

    def test_signify_rejects_wrong_signer(self):
        ksig = load_cli_module("k-signify")
        sk1 = bytes(range(32))
        sk2 = bytes(range(1, 33))
        pk1 = ksig.ed25519_publickey(sk1)
        pk2 = ksig.ed25519_publickey(sk2)
        msg = b"payload"
        sig1 = ksig.ed25519_sign(msg, sk1, pk1)
        self.assertFalse(ksig.ed25519_verify(sig1, msg, pk2),
                         "Tanda tangan penyerang tidak boleh lolos verifikasi kunci lain")


class TestCommonHelpers(unittest.TestCase):
    """Uji perilaku tepi helper bersama di kalacakra_common."""

    def test_redact_multiple_secret_types(self):
        from kalacakra_common import redact_secrets
        text = (
            "aws AKIAIOSFODNN7EXAMPLE and jwt "
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        )
        redacted, found = redact_secrets(text)
        self.assertTrue(found)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)

    def test_locale_fallback_for_unknown_lang(self):
        from kalacakra_common import get_locale_strings
        strings, lang = get_locale_strings("en")
        self.assertEqual(lang, "en")
        strings_id, lang_id = get_locale_strings("id")
        self.assertEqual(lang_id, "id")

    def test_dangerous_and_safe_boundary(self):
        from kalacakra_common import is_dangerous_command
        # Batas: rm -rf ke path relatif aman, destructive tidak
        self.assertFalse(is_dangerous_command("rm -rf ./build"))
        self.assertTrue(is_dangerous_command("dd if=/dev/zero of=/dev/sda"))
        self.assertTrue(is_dangerous_command("chmod -R 777 /"))


if __name__ == "__main__":
    unittest.main()
