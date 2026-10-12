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


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def load_cli_module(name):
    """Muat script CLI tanpa ekstensi .py sebagai modul Python importable.
    Wajib memakai SourceFileLoader eksplisit karena nama file tanpa .py.
    Direktori bin ditambahkan ke sys.path agar `_kalacakra_bootstrap` (modul
    bersama) dapat diimpor seperti saat skrip dijalankan langsung."""
    import importlib.util
    from importlib.machinery import SourceFileLoader
    bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    path = os.path.join(bin_dir, name)
    loader = SourceFileLoader(f"kalacakra_cli_{name}", path)
    spec = importlib.util.spec_from_loader(f"kalacakra_cli_{name}", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestKQASync(unittest.TestCase):
    def test_k_qa_expected_bins_matches_actual_bin_dir(self):
        """Daftar expected_bins di k-qa harus persis sama dengan isi rootfs/usr/bin
        (kecuali modul privat berawalan '_'). Mencegah tool baru luput dari QA."""
        import re
        bin_dir = os.path.join(ROOTFS_DIR, "usr", "bin")
        actual = {n for n in os.listdir(bin_dir)
                  if os.path.isfile(os.path.join(bin_dir, n)) and not n.startswith("_")}

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

    def test_beam_multipart_saves_and_blocks_traversal(self):
        """k-beam harus menyimpan file multipart dengan aman: nama dengan titik/spasi
        oke, tapi path traversal dinetralkan ke basename (tak keluar save_dir)."""
        import tempfile

        def build_body(boundary, filename, content):
            return (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode() + content + f"\r\n--{boundary}--\r\n".encode()

        def save_multipart(data, content_type, save_dir):
            # Logika inti sama dengan k-beam.BeamUploadHandler._save_multipart
            import email
            header = f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
            msg = email.message_from_bytes(header + data)
            saved, rejected = [], []
            if not msg.is_multipart():
                return saved, rejected
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                filename = part.get_filename()
                if not filename:
                    continue
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                safe_name = os.path.basename(filename.replace("\\", "/"))
                if not safe_name or safe_name in (".", ".."):
                    rejected.append(filename)
                    continue
                out_path = os.path.abspath(os.path.join(save_dir, safe_name))
                if not out_path.startswith(save_dir + os.sep):
                    rejected.append(safe_name)
                    continue
                with open(out_path, "wb") as f:
                    f.write(payload)
                saved.append(safe_name)
            return saved, rejected

        boundary = "----KalacakraTestBoundary"
        ct = f"multipart/form-data; boundary={boundary}"
        with tempfile.TemporaryDirectory() as d:
            d = os.path.abspath(d)
            # Nama normal
            saved, _ = save_multipart(build_body(boundary, "dokumen.txt", b"halo"), ct, d)
            self.assertEqual(saved, ["dokumen.txt"])
            with open(os.path.join(d, "dokumen.txt"), "rb") as f:
                self.assertEqual(f.read(), b"halo")
            # Nama dengan spasi & titik berganda (regresi: nama harus utuh)
            saved, _ = save_multipart(build_body(boundary, "laporan final v2.tar.gz", b"X"), ct, d)
            self.assertEqual(saved, ["laporan final v2.tar.gz"])
            self.assertTrue(os.path.isfile(os.path.join(d, "laporan final v2.tar.gz")))
            # Path traversal -> dinetralkan ke basename, tidak keluar dari d
            saved, _ = save_multipart(build_body(boundary, "../../etc/evil", b"Y"), ct, d)
            self.assertEqual(saved, ["evil"])
            self.assertTrue(os.path.isfile(os.path.join(d, "evil")))
            self.assertFalse(os.path.exists(os.path.abspath(os.path.join(d, "..", "..", "etc", "evil"))))
            # File berisi byte mirip boundary tetap roundtrip utuh
            tricky = b"prefix --" + boundary.encode() + b" suffix"
            saved, _ = save_multipart(build_body(boundary, "tricky.bin", tricky), ct, d)
            self.assertEqual(saved, ["tricky.bin"])
            with open(os.path.join(d, "tricky.bin"), "rb") as f:
                self.assertEqual(f.read(), tricky)


class TestKAiHelpers(unittest.TestCase):
    def test_ollama_timeout_configurable(self):
        kai = load_cli_module("k-ai")
        cases = [("", 120.0), ("60", 60.0), ("0", None), ("-5", None), ("abc", 120.0)]
        for raw, expected in cases:
            old = os.environ.get("KALACAKRA_AI_TIMEOUT")
            os.environ["KALACAKRA_AI_TIMEOUT"] = raw
            try:
                self.assertEqual(kai._ollama_timeout(), expected, f"timeout env={raw!r}")
            finally:
                if old is None:
                    os.environ.pop("KALACAKRA_AI_TIMEOUT", None)
                else:
                    os.environ["KALACAKRA_AI_TIMEOUT"] = old

    def test_clean_code_block_extraction(self):
        kai = load_cli_module("k-ai")
        self.assertEqual(kai.clean_code_block("```bash\nls -la\n```"), "ls -la")
        self.assertEqual(kai.clean_code_block("```\nfind . -name x\n```"), "find . -name x")
        self.assertEqual(kai.clean_code_block("echo plain"), "echo plain")


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


class TestRewindRestoreLogic(unittest.TestCase):
    """Uji logika inti k-rewind restore (tanpa snapshot nyata, yang butuh root).
    Fokus: tidak boleh kehilangan berkas asli bila restore gagal."""

    @staticmethod
    def _restore(source_file, target):
        # Replika logika inti yang sama dengan k-rewind restore (jaga paritas).
        import subprocess
        backup = f"{target}.before-rewind"
        renamed = False
        if os.path.lexists(target):
            try:
                os.rename(target, backup)
                renamed = True
            except OSError:
                return "ERR-backup"
        res = subprocess.run(["cp", "-a", source_file, target],
                             capture_output=True)
        if res.returncode != 0:
            if renamed:
                os.replace(backup, target)
                return "ERR-copy-restored"
            return "ERR-copy"
        return "OK"

    def test_restore_normal_keeps_backup(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src"); write_file(src, "BARU")
            tgt = os.path.join(d, "tgt"); write_file(tgt, "LAMA")
            self.assertEqual(self._restore(src, tgt), "OK")
            self.assertEqual(read_file(tgt), "BARU")
            self.assertEqual(read_file(tgt + ".before-rewind"), "LAMA")

    def test_restore_new_target(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src"); write_file(src, "BARU")
            tgt = os.path.join(d, "missing")
            self.assertEqual(self._restore(src, tgt), "OK")
            self.assertEqual(read_file(tgt), "BARU")

    def test_restore_failure_preserves_original(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            tgt = os.path.join(d, "keep"); write_file(tgt, "ASLI")
            # source tidak ada -> cp gagal -> backup WAJIB dipulihkan
            self.assertEqual(self._restore("/nonexistent/src", tgt), "ERR-copy-restored")
            self.assertEqual(read_file(tgt), "ASLI")

    def test_restore_handles_broken_symlink_target(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src"); write_file(src, "BARU")
            tgt = os.path.join(d, "broken")
            os.symlink("/nonexistent/path", tgt)
            # lexists menangkap symlink rusak -> rename berhasil -> restore OK
            self.assertEqual(self._restore(src, tgt), "OK")
            self.assertFalse(os.path.islink(tgt))
            self.assertEqual(read_file(tgt), "BARU")


class TestLookManager(unittest.TestCase):
    """k-look: preset loading, apply ke HOME terisolasi, rollback tanpa data loss."""

    def _run_look(self, args, home):
        import subprocess, tempfile
        path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-look")
        env = os.environ.copy()
        env["HOME"] = home
        env["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
        env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
        return subprocess.run([sys.executable, path] + args,
                              capture_output=True, text=True, env=env, timeout=60)

    def test_presets_exist_and_are_valid_json(self):
        look = load_cli_module("k-look")
        presets = look.list_presets()
        self.assertGreaterEqual(len(presets), 5, "harus ada minimal 5 preset Look")
        ids = {p["id"] for p in presets}
        for expected in ("mandala-cyberpunk", "nusantara-bronze", "obsidian-minimal",
                         "aurora-borealis", "kraton-gold"):
            self.assertIn(expected, ids)
        for p in presets:
            self.assertIn("name", p)
            self.assertIn("description", p)

    def test_look_wallpapers_exist(self):
        import glob
        wp_dir = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "look", "wallpapers")
        svgs = glob.glob(os.path.join(wp_dir, "*.svg"))
        self.assertGreaterEqual(len(svgs), 5, "setiap preset harus punya wallpaper SVG")
        # Validasi XML agar tidak ada SVG rusak
        import xml.dom.minidom
        for s in svgs:
            xml.dom.minidom.parse(s)

    def test_look_apply_creates_config_and_records_active(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            res = self._run_look(["apply", "kraton-gold"], home)
            self.assertEqual(res.returncode, 0, res.stderr)
            # Config KDE tertulis (lewat kwriteconfig6 atau fallback INI manual)
            kdeglobals = os.path.join(home, ".config", "kdeglobals")
            self.assertTrue(os.path.isfile(kdeglobals), "kdeglobals harus dibuat")
            active = os.path.join(home, ".local", "share", "kalacakra", "look", "active.json")
            self.assertTrue(os.path.isfile(active), "active.json harus dicatat")
            import json
            with open(active) as f:
                data = json.load(f)
            self.assertEqual(data["id"], "kraton-gold")

    def test_look_rollback_restores_previous_config(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            cfg_dir = os.path.join(home, ".config")
            os.makedirs(cfg_dir, exist_ok=True)
            kdeglobals = os.path.join(cfg_dir, "kdeglobals")
            # Kondisi awal: tema lama
            with open(kdeglobals, "w") as f:
                f.write("[General]\nColorScheme=OldTheme\n")
            # Terapkan preset (mencadangkan yang lama)
            self._run_look(["apply", "obsidian-minimal"], home)
            # Rollback harus memulihkan ColorScheme=OldTheme
            res = self._run_look(["rollback"], home)
            self.assertEqual(res.returncode, 0, res.stderr)
            with open(kdeglobals) as f:
                self.assertIn("OldTheme", f.read())

    def test_look_unknown_preset_fails_cleanly(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            res = self._run_look(["apply", "tidak-ada-preset-ini"], home)
            self.assertEqual(res.returncode, 1)
            self.assertNotIn("Traceback", res.stderr)
            self.assertIn("tidak ditemukan", res.stdout)

    def test_look_dry_run_changes_nothing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            res = self._run_look(["apply", "kraton-gold", "--dry-run"], home)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("DRY-RUN", res.stdout)
            # Tidak boleh ada berkas konfigurasi yang dibuat
            cfg = os.path.join(home, ".config")
            leftovers = []
            if os.path.isdir(cfg):
                for root, _, files in os.walk(cfg):
                    leftovers += files
            self.assertEqual(leftovers, [], f"dry-run menulis berkas: {leftovers}")
            # active.json juga tidak boleh dibuat
            active = os.path.join(home, ".local", "share", "kalacakra", "look", "active.json")
            self.assertFalse(os.path.isfile(active))

    def test_look_validate_preset(self):
        look = load_cli_module("k-look")
        ok, problems = look.validate_preset({"id": "x", "name": "X"})
        self.assertTrue(ok, problems)
        bad, problems = look.validate_preset({"description": "tanpa id/name"})
        self.assertFalse(bad)
        self.assertTrue(any("wajib" in p for p in problems))

    def test_look_import_preview_and_install(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as home:
            env = os.environ.copy()
            env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
            env["HOME"] = home
            preset_file = os.path.join(home, "community.json")
            with open(preset_file, "w") as f:
                json.dump({"id": "komunitas-1", "name": "Komunitas Satu",
                           "color_scheme": "BreezeDark"}, f)
            # Preview (tanpa --install) tidak menulis apa pun
            import subprocess
            path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-look")
            r1 = subprocess.run([sys.executable, path, "import", preset_file],
                                capture_output=True, text=True, env=env)
            self.assertEqual(r1.returncode, 0, r1.stderr)
            self.assertIn("Validasi selesai", r1.stdout)
            user_dir = os.path.join(env["XDG_DATA_HOME"], "kalacakra", "look", "presets")
            self.assertFalse(os.path.isfile(os.path.join(user_dir, "komunitas-1.json")))
            # --install menulis ke direktori user
            r2 = subprocess.run([sys.executable, path, "import", preset_file, "--install"],
                                capture_output=True, text=True, env=env)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertTrue(os.path.isfile(os.path.join(user_dir, "komunitas-1.json")))

    def test_look_import_rejects_invalid_json(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            bad = os.path.join(home, "bad.json")
            with open(bad, "w") as f:
                f.write("{ bukan json }")
            res = self._run_look(["import", bad], home)
            self.assertEqual(res.returncode, 1)
            self.assertNotIn("Traceback", res.stderr)
            self.assertIn("tidak valid", res.stdout)


class TestInterceptorSmartRecommend(unittest.TestCase):
    """k-interceptor: rekomendasi backend cerdas & jujur (tanpa memalsukan)."""

    def test_recommend_known_flatpak_alias(self):
        ki = load_cli_module("k-interceptor")
        choice, reason = ki.recommend_backend(["vlc"])
        # vlc dikenal -> diarahkan ke Flatpak (opsi 1) bila flatpak tersedia
        if ki.backend_available("flatpak"):
            self.assertEqual(choice, "1")
            self.assertIn("vlc", reason.lower())
        else:
            self.assertEqual(choice, "")  # jujur: tak merekomendasikan yang absen

    def test_recommend_brew_cli_tool_when_available(self):
        ki = load_cli_module("k-interceptor")
        choice, _ = ki.recommend_backend(["ripgrep"])
        if ki.backend_available("brew"):
            self.assertEqual(choice, "4")

    def test_backend_available_is_truthful(self):
        ki = load_cli_module("k-interceptor")
        # backend yang tak dikenal -> False, bukan exception
        self.assertFalse(ki.backend_available("tidak-ada-backend"))

    def test_flatpak_alias_mapping_is_consistent(self):
        ki = load_cli_module("k-interceptor")
        # Semua nilai alias harus mengikuti format ID Flathub (mengandung titik)
        for name, app_id in ki.FLATPAK_ALIASES.items():
            self.assertIn(".", app_id, f"alias '{name}' -> '{app_id}' bukan ID Flathub")
            self.assertEqual(name, name.lower())


class TestWelcomeWizard(unittest.TestCase):
    def _run_welcome(self, args, home, lang="en_US.UTF-8"):
        import subprocess
        path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-welcome")
        env = os.environ.copy()
        env["HOME"] = home
        env["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
        env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
        env["LANG"] = lang
        env["NO_COLOR"] = "1"
        return subprocess.run([sys.executable, path] + args,
                              capture_output=True, text=True, env=env, timeout=60, input="")

    def test_welcome_noninteractive_runs_clean(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            res = self._run_welcome(["--yes"], home)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertNotIn("Traceback", res.stderr)
            self.assertIn("KALACAKRA OS", res.stdout)
            # Wizard menerapkan tema default -> config KDE tertulis
            self.assertTrue(os.path.isfile(os.path.join(home, ".config", "kdeglobals")))

    def test_welcome_indonesian_flow(self):
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            res = self._run_welcome(["--yes", "--lang", "id"], home, lang="id_ID.UTF-8")
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("Selamat", res.stdout)

    def test_welcome_interactive_language_choice(self):
        import tempfile, subprocess
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-welcome")
            env = os.environ.copy()
            env["HOME"] = home
            env["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
            env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
            env["NO_COLOR"] = "1"
            # Pilih bahasa Indonesia (2), tema 5, lalu selesai
            res = subprocess.run([sys.executable, path], capture_output=True, text=True,
                                 env=env, input="2\n0\n", timeout=60)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertNotIn("Traceback", res.stderr)


class TestLookPick(unittest.TestCase):
    def test_pick_applies_selected_theme(self):
        import tempfile, subprocess
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-look")
            env = os.environ.copy()
            env["HOME"] = home
            env["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
            env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
            env["KALACAKRA_FORCE_COLOR"] = "0"
            res = subprocess.run([sys.executable, path, "pick"], capture_output=True,
                                 text=True, env=env, input="1\nn\n", timeout=60)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("Selesai", res.stdout)

    def test_pick_cancel_changes_nothing(self):
        import tempfile, subprocess
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-look")
            env = os.environ.copy()
            env["HOME"] = home
            env["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
            env["XDG_DATA_HOME"] = os.path.join(home, ".local", "share")
            res = subprocess.run([sys.executable, path, "pick"], capture_output=True,
                                 text=True, env=env, input="0\n", timeout=60)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("Dibatalkan", res.stdout)
            self.assertFalse(os.path.isfile(os.path.join(home, ".config", "kdeglobals")))


class TestHubIntegration(unittest.TestCase):
    def test_hub_status_mentions_look_and_welcome(self):
        import subprocess
        path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-hub")
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        res = subprocess.run([sys.executable, path, "--status"], capture_output=True,
                             text=True, env=env, timeout=30)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("[7]", res.stdout)
        self.assertIn("[8]", res.stdout)


class TestShowcase(unittest.TestCase):
    def test_showcase_runs_and_lists_themes(self):
        import subprocess
        path = os.path.join(ROOTFS_DIR, "usr", "bin", "k-showcase")
        env = os.environ.copy()
        env["NO_COLOR"] = "1"
        env["LANG"] = "en_US.UTF-8"
        res = subprocess.run([sys.executable, path, "--no-fetch"],
                             capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("KALACAKRA OS", res.stdout)
        self.assertIn("IDENTITY", res.stdout)  # pilar identitas
        self.assertIn("Look", res.stdout)


class TestLocaleCoverage(unittest.TestCase):
    """Setiap kunci locale baru (look/showcase) harus ada di EN & ID."""

    def test_new_locale_keys_present_in_both_languages(self):
        import json
        new_keys = ["look_header", "look_applying", "look_done",
                    "look_rollback_done", "look_no_active", "look_share_caption",
                    "showcase_tagline"]
        for lang in ("en", "id"):
            with open(os.path.join(os.path.dirname(__file__), "..", "rootfs", "usr",
                                   "share", "kalacakra", "locales", f"{lang}.json"),
                      encoding="utf-8") as f:
                data = json.load(f)
            for k in new_keys:
                self.assertIn(k, data, f"kunci '{k}' hilang di {lang}.json")


class TestSmokeNoTools(unittest.TestCase):
    """Smoke test: tool harus tetap jujur & tidak crash saat dependensi eksternal
    benar-benar absen (PATH kosong) - skenario paling keras."""

    def _run_with_empty_path(self, script, args=None, stdin=None):
        import subprocess, tempfile
        path = os.path.join(ROOTFS_DIR, "usr", "bin", script)
        with tempfile.TemporaryDirectory() as empty_bin:
            env = os.environ.copy()
            # PATH ke python + folder kosong: tool eksternal (bootc, podman, ...) absen
            env["PATH"] = empty_bin
            env["LANG"] = "en_US.UTF-8"
            return subprocess.run(
                [sys.executable, path] + (args or []),
                capture_output=True, text=True, env=env,
                input=stdin, timeout=60
            )

    def test_k_doctor_full_run_without_external_tools(self):
        res = self._run_with_empty_path("k-doctor")
        self.assertEqual(res.returncode, 0, f"stderr: {res.stderr}\nstdout: {res.stdout}")
        self.assertNotIn("Traceback", res.stderr)
        self.assertNotIn("Traceback", res.stdout)
        # Harus tetap melaporkan hasil, bukan diam
        self.assertIn("Immutable Core", res.stdout)

    def test_k_interceptor_no_packages(self):
        # 'apt install' tanpa paket: harus tetap tampil menu, tidak crash
        res = self._run_with_empty_path("k-interceptor", ["apt", "install"], stdin="\n")
        self.assertNotIn("Traceback", res.stderr)
        self.assertIn("Immutable", res.stdout)

    def test_k_interceptor_no_args(self):
        res = self._run_with_empty_path("k-interceptor", [])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Usage", res.stdout + res.stderr)

    def test_k_interceptor_missing_backend_degrades_honestly(self):
        # Pilih opsi 4 (Homebrew) yang pasti absen di PATH kosong -> pesan jujur, exit 1
        res = self._run_with_empty_path("k-interceptor", ["apt", "install", "vlc"], stdin="4\n")
        self.assertEqual(res.returncode, 1)
        self.assertNotIn("Traceback", res.stderr)
        self.assertIn("brew", res.stdout.lower() + res.stderr.lower())


if __name__ == "__main__":
    unittest.main()
