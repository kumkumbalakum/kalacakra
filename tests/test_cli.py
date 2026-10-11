import unittest
import os
import sys

ROOTFS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rootfs"))
LIB_PATH = os.path.join(ROOTFS_DIR, "usr", "share", "kalacakra", "lib")
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

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
            "pkg_installing"
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
        self.assertFalse(is_dangerous_command("ls -la /tmp"))
        self.assertFalse(is_dangerous_command("podman run alpine echo hello"))

    def test_package_extractor_multi_package(self):
        res1 = extract_target_packages(["install", "-y", "vlc", "ffmpeg", "mpv"])
        self.assertEqual(res1, ["vlc", "ffmpeg", "mpv"])

        res2 = extract_target_packages(["-S", "--noconfirm", "neovim", "ripgrep"])
        self.assertEqual(res2, ["neovim", "ripgrep"])

        res3 = extract_target_packages(["update"])
        self.assertEqual(res3, [])

if __name__ == "__main__":
    unittest.main()
