# ☸️ Kalacakra OS (Roda Waktu)

[![Build and Sign OCI](https://github.com/kalacakra-os/kalacakra/actions/workflows/build-oci.yml/badge.svg)](https://github.com/kalacakra-os/kalacakra/actions/workflows/build-oci.yml)
[![Build ISO](https://github.com/kalacakra-os/kalacakra/actions/workflows/build-iso.yml/badge.svg)](https://github.com/kalacakra-os/kalacakra/actions/workflows/build-iso.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> **Kalacakra OS** adalah distribusi Linux desktop modern berbasis *immutable / atomic container* (`bootc` / `ostree`) dengan perpaduan arsitektur **Triad**: Filosofi Stabilitas Batu Karang setara Debian, Pondasi Modern Fedora & Universal Blue, serta fleksibilitas tanpa batas Arch Linux AUR. Dilengkapi dukungan **Native Dual Language (English + Bahasa Indonesia)** dan kecerdasan buatan lokal terproteksi privasi.

---

## ✨ Fitur Utama (Highlights)

* 🛡️ **Bulletproof Immutable Root:** Root filesystem (`/usr`) berstatus *read-only*. Pembaruan sistem dilakukan secara atomik di latar belakang; sistem tidak akan pernah rusak (*zero-breakage*).
* 🔄 **Dual-Tier Rollback Engine:** Rollback root otomatis jika boot gagal 3x berturut-turut, dipadu snapshot Snapper khusus data pengguna (`@home` & `@var`).
* 🇮🇩 / 🇺🇸 **Native Dual Language (EN/ID):** Sistem dwibahasa penuh sejak boot pertama di seluruh elemen: GUI KDE Plasma 6, CLI tooling, voice Whisper, dan AI Terminal Companion.
* 🚀 **Universal Command Interceptor (`k-interceptor`):** Mencegat perintah `sudo apt install` atau `pacman -S` pada host imutabel dan memandu instalasi ke Flatpak, Arch Space, Debian Space, atau Homebrew tanpa kebingungan.
* ⚡ **Kernel Sched-ext (SCX Framework):** Penggantian *CPU scheduler* secara dinamis via eBPF (`scx_lavd` untuk gaming ultra-low latency, `scx_rusty` untuk kompilasi kode).
* 🤖 **Local Private AI (`k-ai`) & Voice (`Super + V`):** Didukung runtime Ollama dan `whisper.cpp` offline lokal (dioptimalkan untuk NPU/GPU), dengan *Secret Sanitizer* otomatis untuk mencegah kebocoran data sensitif.
* 🎮 **Game Ready Profile:** Pre-configured Steam, Heroic Launcher, ProtonUp-Qt, MangoHud, gamemode, dan UMU Proton Launcher (.exe context menu).
* 🔒 **Enterprise-Grade Security:** Cosign image signature verification, SELinux Enforcing, MOK Secure Boot, USBGuard screen-lock binding, DNS-over-TLS (DoT), dan kesiapan Post-Quantum Cryptography (PQC).

---

## 🏗️ Struktur Repositori

```text
kalacakra/
├── plan.md                 # Spesifikasi arsitektur & roadmap visi 10 tahun
├── Containerfile           # Image base OCI (Mesa / AMD Radeon / Intel)
├── Containerfile.nvidia    # Image base OCI dengan driver proprietary Nvidia
├── Justfile                # Resep deklaratif manajemen sistem
├── rootfs/                 # Overlay sistem operasi yang diinjeksi ke image
│   ├── etc/
│   │   ├── systemd/        # Unit zram, ollama user service, DNS-over-TLS
│   │   ├── sysctl.d/       # Kernel hardening configuration
│   │   └── profile.d/      # Homebrew path & interceptor shell hooks
│   └── usr/
│       ├── bin/            # Kalacakra CLI suite (kalacakra, k-interceptor, k-ai, k-aur, k-doctor)
│       └── share/kalacakra/
│           ├── fastfetch/  # Logo mandala ASCII & config
│           ├── locales/    # String lokalisasi id.json & en.json
│           └── scripts/    # Battery lifespan 80% cap limiter
└── .github/workflows/      # Automasi build OCI & bootc-image-builder ISO
```

---

## 🛠️ Panduan Perintah Kalacakra CLI

```bash
# Perbarui seluruh sistem (Host OCI, Flatpak, Homebrew, dan Spaces)
kalacakra update

# Jalankan diagnosa kesehatan sistem menyeluruh
kalacakra doctor

# Bersihkan cache usang dan dangling container images
kalacakra clean

# Pasang model AI lokal ke Ollama (contoh: Llama 3.2 1B)
kalacakra install-model llama3.2:1b

# Ganti penjadwal CPU dinamis (lavd untuk gaming / rusty untuk dev)
kalacakra scx lavd

# Beralih varian driver tanpa install ulang (Rebase)
kalacakra rebase nvidia

# Batasi pengisian daya baterai laptop ke 80% (Preservasi fisik baterai)
kalacakra battery-cap 80

# Beralih preferensi bahasa sistem (id / en)
kalacakra lang id
```

---

## 🔨 Membangun Image Secara Lokal

Pastikan Anda memiliki `podman` atau `docker`:

```bash
# Build image base Mesa/Intel/AMD
podman build -t kalacakra-os:latest -f Containerfile .

# Build image varian Nvidia
podman build -t kalacakra-nvidia:latest -f Containerfile.nvidia .
```

---

## 📜 Lisensi

Kalacakra OS dilisensikan di bawah [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0).
Dokumentasi arsitektur mengacu pada [plan.md](plan.md).
