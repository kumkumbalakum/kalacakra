#!/usr/bin/env python3
"""
Kalacakra OS - Shared Core Library
Centralized helper functions for localization, secret sanitization, and package extraction.
"""

import os
import sys
import re
import json

# Pola regex deteksi rahasia / secret sebelum dikirim ke AI
SECRET_PATTERNS = [
    r"(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{8,})['\"]?",
    r"ghp_[A-Za-z0-9]{36}",                          # GitHub Personal Access Token
    r"AKIA[0-9A-Z]{16}",                             # AWS Access Key
    r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC )?PRIVATE KEY-----", # SSH/SSL Key
    r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}" # JWT Token
]

# Perintah berisiko tinggi / destruktif yang memerlukan peringatan keras
DESTRUCTIVE_PATTERNS = [
    # rm rekursif ke path absolut / home / glob: 'rm -rf /', '/*', '/var', '~', '$HOME'
    r"\brm\s+(?:-[a-zA-Z-]+\s+)+(?:/|~|\$HOME)",
    r"\bmkfs(?:\.\w+)?\s+",
    r"\bdd\s+if=.*?of=/dev/[a-z]+",
    r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",  # Fork bomb
    r">\s*/dev/sd[a-z]",
    r"\bchmod\s+-R\s+777\s+/"
]

def resolve_locales_dir() -> str:
    """
    Menemukan direktori locales secara fleksibel:
    1. Menggunakan env var KALACAKRA_LOCALES_DIR jika disetel.
    2. Mencari relatif terhadap repo / script.
    3. Fallback ke lokasi sistem produksi /usr/share/kalacakra/locales.
    """
    if "KALACAKRA_LOCALES_DIR" in os.environ and os.path.isdir(os.environ["KALACAKRA_LOCALES_DIR"]):
        return os.environ["KALACAKRA_LOCALES_DIR"]

    # Cari relatif dari file library ini: ../locales
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_locales = os.path.abspath(os.path.join(current_dir, "..", "locales"))
    if os.path.isdir(relative_locales):
        return relative_locales

    # Standar produksi di host OCI
    system_locales = "/usr/share/kalacakra/locales"
    if os.path.isdir(system_locales):
        return system_locales

    return relative_locales

def get_locale_strings(lang_override: str = None) -> tuple[dict, str]:
    """
    Mengambil kamus string lokalisasi dan kode bahasa aktif ('id' atau 'en').
    """
    lang = lang_override or os.environ.get("LANG", "en_US.UTF-8")
    is_id = "id" in lang.lower()
    locales_dir = resolve_locales_dir()
    locale_file = os.path.join(locales_dir, "id.json" if is_id else "en.json")

    if os.path.isfile(locale_file):
        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                return json.load(f), "id" if is_id else "en"
        except Exception:
            pass
    return {}, "id" if is_id else "en"

def redact_secrets(text: str) -> tuple[str, bool]:
    """
    Menyensor kredensial sensitif dalam string. Mengembalikan (text_disensor, ada_rahasia).
    """
    redacted = text
    found = False
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, redacted):
            found = True
            redacted = re.sub(pattern, "[REDACTED_SECRET]", redacted)
    return redacted, found

def is_dangerous_command(command: str) -> bool:
    """
    Mendeteksi apakah perintah berpotensi destruktif / berbahaya terhadap sistem.
    """
    for pattern in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command):
            return True
    return False

def extract_target_packages(args: list[str]) -> list[str]:
    """
    Memfilter flags dan subcommands untuk mendapatkan daftar nama paket target.
    """
    skip_tokens = {
        "install", "remove", "update", "upgrade", "purge", "reinstall",
        "-S", "-Syu", "-Syy", "-R", "-U", "-y", "-q", "--noconfirm",
        "-f", "--fix-broken", "-s", "--nodeps"
    }
    return [arg for arg in args if not arg.startswith("-") and arg not in skip_tokens]
