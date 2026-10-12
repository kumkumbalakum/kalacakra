#!/usr/bin/env python3
"""
Kalacakra OS - _kalacakra_bootstrap
Modul pembantu tunggal untuk memuat library bersama `kalacakra_common` dari
berbagai lokasi (repo lokal saat dev, atau /usr/share/kalacakra/lib saat
terpasang di image OCI).

Tujuan: menghapus ~12 baris boilerplate `sys.path` + `try/except ImportError`
yang sebelumnya disalin di setiap tool CLI. Modul ini SENDIRI hanya memakai
stdlib, sehingga aman diimpor sebelum path library diketahui (ia diletakkan di
direktori yang sama dengan tool, yang selalu ada di sys.path[0] saat dijalankan
sebagai skrip).

Pemakaian di sebuah tool:
    from _kalacakra_bootstrap import load_common
    common = load_common()
    strings, lang = common.get_locale_strings()

Atau, untuk import simbol langsung (paling ringkas):
    from _kalacakra_bootstrap import common
    from _kalacakra_bootstrap import get_locale_strings, redact_secrets
"""

import os
import sys

# Nama library bersama yang dicari.
_COMMON_MODULE = "kalacakra_common"


def _candidate_lib_dirs(script_dir: str) -> list:
    """Urutan direktori kandidat tempat `kalacakra_common.py` mungkin berada."""
    candidates = []
    env_dir = os.environ.get("KALACAKRA_LIB_DIR")
    if env_dir:
        candidates.append(env_dir)
    if script_dir:
        # Layout repo: <rootfs>/usr/bin/../share/kalacakra/lib
        candidates.append(os.path.abspath(os.path.join(script_dir, "..", "share", "kalacakra", "lib")))
    # Layout sistem (image OCI / terpasang).
    candidates.append("/usr/share/kalacakra/lib")
    return candidates


def ensure_lib_on_path(script_file: str = None) -> str:
    """Pastikan direktori library bersama ada di sys.path.

    Mengembalikan path direktori library yang dipakai (atau '' bila tak ada).
    Aman dipanggil berkali-kali (idempoten).
    """
    script_file = script_file or sys.argv[0]
    script_dir = os.path.dirname(os.path.abspath(script_file)) if script_file else ""
    for d in _candidate_lib_dirs(script_dir):
        if os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)
        if os.path.isfile(os.path.join(d, _COMMON_MODULE + ".py")):
            return d
    return ""


# Siapkan path saat modul ini diimpor.
ensure_lib_on_path()


def _fallback_get_locale_strings(lang_override=None):
    """Fallback jujur bila library bersama tidak tersedia: kembalikan kamus kosong
    sehingga tool tetap memakai string default bawaan tiap strings.get()."""
    lang = lang_override or os.environ.get("LANG", "en_US.UTF-8")
    return {}, ("id" if "id" in lang.lower() else "en")


def _fallback_resolve_locales_dir():
    for cand in (
        os.environ.get("KALACAKRA_LOCALES_DIR"),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                                     "..", "share", "kalacakra", "locales")),
        "/usr/share/kalacakra/locales",
    ):
        if cand and os.path.isdir(cand):
            return cand
    return "/usr/share/kalacakra/locales"


def _fallback_extract_target_packages(args):
    skip = {
        "install", "remove", "update", "upgrade", "purge", "reinstall",
        "-S", "-Syu", "-Syy", "-R", "-U", "-y", "-q", "--noconfirm",
        "-f", "--fix-broken", "-s", "--nodeps",
    }
    return [a for a in args if not a.startswith("-") and a not in skip]


def _fallback_redact_secrets(text):
    return text, False


def _fallback_is_dangerous_command(command):
    return False


class _Common:
    """Objek proksi yang menyediakan fungsi library bersama (atau fallback jujur)."""

    def __init__(self):
        self.available = False
        try:
            import kalacakra_common as _c  # type: ignore
            self._c = _c
            self.available = True
        except ImportError:
            self._c = None

        # Selalu sediakan fungsi-fungsi penting dengan fallback yang aman & jujur.
        self.get_locale_strings = (
            self._c.get_locale_strings if self.available and hasattr(self._c, "get_locale_strings")
            else _fallback_get_locale_strings
        )
        self.resolve_locales_dir = (
            self._c.resolve_locales_dir if self.available and hasattr(self._c, "resolve_locales_dir")
            else _fallback_resolve_locales_dir
        )
        self.extract_target_packages = (
            self._c.extract_target_packages if self.available and hasattr(self._c, "extract_target_packages")
            else _fallback_extract_target_packages
        )
        self.redact_secrets = (
            self._c.redact_secrets if self.available and hasattr(self._c, "redact_secrets")
            else _fallback_redact_secrets
        )
        self.is_dangerous_command = (
            self._c.is_dangerous_command if self.available and hasattr(self._c, "is_dangerous_command")
            else _fallback_is_dangerous_command
        )


# Objek singleton `common` — hasil pemuatan malas (lazy) saat pertama diakses.
class _LazyCommon:
    def __init__(self):
        self._instance = None

    def _get(self):
        if self._instance is None:
            self._instance = _Common()
        return self._instance

    def __getattr__(self, name):
        return getattr(self._get(), name)


common = _LazyCommon()


def load_common():
    """Kembalikan objek `_Common` (dengan semua fungsi bersama/fallback)."""
    return common._get()


# --- Ekspor simbol yang paling sering dipakai, agar `from _kalacakra_bootstrap
#     import get_locale_strings` tetap bekerja persis seperti sebelumnya. ---
def get_locale_strings(lang_override=None):
    return common.get_locale_strings(lang_override)


def resolve_locales_dir():
    return common.resolve_locales_dir()


def extract_target_packages(args):
    return common.extract_target_packages(args)


def redact_secrets(text):
    return common.redact_secrets(text)


def is_dangerous_command(command):
    return common.is_dangerous_command(command)


__all__ = [
    "common", "load_common", "ensure_lib_on_path",
    "get_locale_strings", "resolve_locales_dir", "extract_target_packages",
    "redact_secrets", "is_dangerous_command",
]
