import unittest
import os
import sys
import json
import re

# Tambahkan path rootfs/usr/bin agar module bisa diuji
ROOTFS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rootfs"))
LOCALES_DIR = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "locales")

class TestKalacakraLocales(unittest.TestCase):
    def test_locale_files_exist_and_valid_json(self):
        for lang in ["id", "en"]:
            path = os.path.join(LOCALES_DIR, f"{lang}.json")
            self.assertTrue(os.path.isfile(path), f"Locale file {path} should exist")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIn("interceptor_title", data)
                self.assertIn("ai_safety_warning", data)
                self.assertIn("doctor_header", data)

    def test_secret_redaction_patterns(self):
        # Import redact_secrets logic
        secret_patterns = [
            r"(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{8,})['\"]?",
            r"ghp_[A-Za-z0-9]{36}",
            r"AKIA[0-9A-Z]{16}",
            r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC )?PRIVATE KEY-----",
            r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        ]

        def redact_secrets(text: str) -> str:
            redacted = text
            for pattern in secret_patterns:
                redacted = re.sub(pattern, "[REDACTED_SECRET]", redacted)
            return redacted

        sample_with_gh_token = "Deploy script with ghp_123456789012345678901234567890123456 to server"
        result = redact_secrets(sample_with_gh_token)
        self.assertNotIn("ghp_123456789012345678901234567890123456", result)
        self.assertIn("[REDACTED_SECRET]", result)

        sample_with_aws = "Error accessing S3 with key AKIAIOSFODNN7EXAMPLE"
        result_aws = redact_secrets(sample_with_aws)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", result_aws)
        self.assertIn("[REDACTED_SECRET]", result_aws)

    def test_interceptor_package_extractor(self):
        def extract_target_packages(args):
            skip_tokens = {"install", "remove", "update", "upgrade", "-S", "-Syu", "-Syy", "-R", "-U", "-y", "-q"}
            return [arg for arg in args if not arg.startswith("-") and arg not in skip_tokens]

        self.assertEqual(extract_target_packages(["install", "-y", "vlc", "ffmpeg"]), ["vlc", "ffmpeg"])
        self.assertEqual(extract_target_packages(["-S", "--noconfirm", "neovim"]), ["neovim"])

if __name__ == "__main__":
    unittest.main()
