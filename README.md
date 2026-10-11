# ☸️ Kalacakra OS (Roda Waktu)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Base: Fedora bootc](https://img.shields.io/badge/Base-Fedora%20bootc%20%2F%20uBlue-red.svg)](https://github.com/ublue-os)
[![Desktop: KDE Plasma 6](https://img.shields.io/badge/Desktop-KDE%20Plasma%206%20Wayland-blue.svg)](https://kde.org)
[![Language: English & Indonesian](https://img.shields.io/badge/Language-English%20%7C%20Indonesia-green.svg)](#-native-dual-language-enid)

> **Kalacakra OS** adalah distribusi Linux desktop modern berbasis *immutable / atomic container* (`bootc` / `ostree`) dengan perpaduan arsitektur **Triad**: Filosofi Stabilitas Batu Karang setara Debian, Pondasi Modern Fedora & Universal Blue, serta fleksibilitas tanpa batas Arch Linux AUR. Dilengkapi dukungan **Native Dual Language (English + Bahasa Indonesia)** dan kecerdasan buatan lokal terproteksi privasi.

---

## 📖 DAFTAR ISI
1. [Fitur Utama](#-fitur-utama-highlights)
2. [Panduan Instalasi & Deployment](#-panduan-instalasi--deployment)
3. [Panduan Penggunaan Sehari-Hari](#-panduan-penggunaan-sehari-hari)
   * [Perintah Kalacakra CLI](#1-perintah-kalacakra-cli)
   * [Universal Command Interceptor](#2-universal-command-interceptor-k-interceptor)
   * [AI Terminal Companion](#3-ai-terminal-companion-k-ai)
   * [Arch Linux AUR Integration](#4-arch-linux-aur-integration-k-aur)
   * [Dikte Suara & Pintasan Keyboard](#5-dikte-suara--pintasan-keyboard)
4. [Panduan Build Image & ISO](#-panduan-build-image--iso)
   * [Build via CI/CD Otomatis](#opsi-a-build-via-cicd-github-actions--gitea-actions)
   * [Build 100% Lokal di Komputer](#opsi-b-build-100-lokal-di-komputer-podman)
5. [Struktur Repositori](#-struktur-repositori)
6. [Lisensi & Spesifikasi](#-lisensi--spesifikasi)

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

## 💿 Panduan Instalasi & Deployment

### Metode 1: Instalasi Baru via File ISO
1. Siapkan file `.iso` Kalacakra OS hasil build.
2. Buat *bootable USB* menggunakan **Ventoy**, **Rufus**, atau `dd`:
   ```bash
   sudo dd if=kalacakra-os-installer.iso of=/dev/sdX bs=4M status=progress oflag=sync
   ```
3. Boot komputer Anda ke USB drive dan ikuti panduan grafis Calamares. Partisi Btrfs (`@`, `@home`, `@var`) dan swap ZRAM akan dikonfigurasi otomatis.

### Metode 2: Rebase Instan (Dari Distro Fedora Atomic yang Sudah Ada)
Jika Anda sudah menggunakan Fedora Silverblue, Kinoite, Bazzite, atau Aurora, Anda dapat beralih ke Kalacakra OS **dalam 1 perintah tanpa instalasi ulang**:
```bash
# Rebase ke Kalacakra OS
rpm-ostree rebase ostree-unverified-registry:http://vps-rastavarian:3000/kumkum/kalacakra:latest
systemctl reboot
```

---

## 🚀 Panduan Penggunaan Sehari-Hari

### 1. Perintah Kalacakra CLI (`kalacakra`)
Perintah pusat berbasis resep deklaratif untuk perawatan sistem:
```bash
kalacakra update            # Perbarui seluruh sistem: Host OCI, Flatpak, Homebrew, & Spaces
kalacakra doctor            # Jalankan diagnosa kesehatan Btrfs, ZRAM, AI, dan sistem
kalacakra clean             # Bersihkan cache Flatpak usang dan container dangling images
kalacakra install-model     # Unduh model AI lokal ke Ollama (contoh: Llama 3.2 1B)
kalacakra scx lavd          # Aktifkan scheduler gaming latensi ultra-rendah (scx_lavd)
kalacakra scx rusty         # Aktifkan scheduler kompilasi multi-core (scx_rusty)
kalacakra rebase nvidia     # Berpindah ke varian driver Nvidia tanpa install ulang OS
kalacakra battery-cap 80    # Batasi pengisian baterai laptop ke 80% (Preservasi baterai)
kalacakra lang id           # Ganti bahasa sistem ke Bahasa Indonesia (atau 'en' untuk English)
```

---

### 2. Universal Command Interceptor (`k-interceptor`)
Di sistem imutabel, perintah manajemen paket konvensional (`apt` atau `pacman`) secara otomatis dicegat oleh shell guard untuk mengarahkan pengguna ke metode yang aman:

```bash
sudo apt install vlc
# atau
pacman -S neovim
```
**Tampilan Interaktif:**
```text
[Kalacakra Interceptor] Host sistem Anda berstatus Imutabel (Terproteksi).
Perintah 'apt install vlc' terdeteksi.

Pilih metode instalasi yang diinginkan:
  [1] Flatpak (Rekomendasi untuk aplikasi Desktop / GUI)
  [2] Kalacakra Space (Arch Linux Container / AUR via k-aur)
  [3] Kalacakra Space (Debian / Ubuntu Container)
  [4] Homebrew on Linux (CLI tool terisolasi di /home)
  [5] Layer ke Host OS (rpm-ostree - memerlukan reboot)

Pilihan Anda [1-5]: 
```

---

### 3. AI Terminal Companion (`k-ai`)
Asisten terminal cerdas berbasis bahasa alami dengan perlindungan data:
* **Tanya Perintah Bash:**
  ```bash
  k-ai "cari file video yang lebih dari 1GB lalu urutkan dari yang terbesar"
  ```
  `k-ai` akan menampilkan preview perintah dan meminta konfirmasi `[Y/n]` sebelum dijalankan.
* **Auto-Diagnosa Error Terminal:**
  ```bash
  k-ai --diagnose
  ```
* **Secret Sanitizer Guardrail:**
  `k-ai` secara otomatis mendeteksi dan menyensor API key (`ghp_...`, `AKIA...`, private key) sebelum prompt diproses, mencegah kebocoran rahasia.

---

### 4. Arch Linux AUR Integration (`k-aur`)
Memasang paket khusus dari Arch User Repository (AUR) ke dalam container terisolasi dan mengekspor shortcut-nya langsung ke menu desktop host:
```bash
# Pasang paket dari AUR (contoh: visual-studio-code-bin)
k-aur install visual-studio-code-bin

# Cari paket di AUR
k-aur search discord-canary

# Hapus paket
k-aur remove visual-studio-code-bin
```

---

### 5. Dikte Suara & Pintasan Keyboard
* **`Super + V`**: Buka mikrofon dikte suara offline (`whisper.cpp`). Bicara dalam Bahasa Indonesia atau Inggris, teks langsung disisipkan di kursor aktif.
* **`Super + Y`**: Toggle mode **Auto-Tiling KWin (Polonium)** untuk beralih instan antara mode jendela floating tradisional dan tiling otomatis.
* **`Super + Space`**: Buka HUD Selection Assistant untuk menerjemahkan teks atau memperbaiki tata bahasa secara instan.
* **Game Windows Non-Steam:** Klik kanan file `.exe` installer game di Dolphin -> pilih **"Jalankan dengan Kalacakra Game Launcher (Proton UMU)"**.

---

## 🔨 Panduan Build Image & ISO

### Opsi A: Build via CI/CD (GitHub Actions / Gitea Actions)
Repositori ini telah dilengkapi workflow CI/CD otomatis di `.github/workflows/`:
1. Push commit ke branch `main`.
2. Workflow `build-oci.yml` otomatis membangun dan menandatangani image dengan Cosign.
3. Jalankan workflow `build-iso.yml` untuk menghasilkan file ISO installer bootable.

### Opsi B: Build 100% Lokal di Komputer (Podman)
Jika ingin mem-build secara lokal tanpa layanan cloud:

```bash
# 1. Build image container base
podman build -t localhost/kalacakra-os:latest -f Containerfile .

# 2. Build image varian Nvidia
podman build -t localhost/kalacakra-nvidia:latest -f Containerfile.nvidia .

# 3. Generate file ISO bootable ke folder ./output
mkdir -p ./output
podman run --rm --privileged \
  --security-opt label=type:unconfined_t \
  -v ./output:/output \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  quay.io/centos-bootc/bootc-image-builder:latest \
  --type iso \
  localhost/kalacakra-os:latest
```

---

## 🏗️ Struktur Repositori

```text
kalacakra/
├── plan.md                 # Master Architecture Specification & 10-Year Roadmap
├── README.md               # Dokumentasi resmi dan panduan pengguna lengkap
├── Containerfile           # Image base OCI (Mesa / AMD Radeon / Intel)
├── Containerfile.nvidia    # Image base OCI dengan driver proprietary Nvidia
├── Justfile                # Resep deklaratif otomatisasi sistem
├── rootfs/                 # Overlay filesystem sistem operasi
│   ├── etc/
│   │   ├── systemd/        # Unit zram, ollama user service, DNS-over-TLS
│   │   ├── sysctl.d/       # Kernel security hardening
│   │   └── profile.d/      # Homebrew path & interceptor shell hooks
│   └── usr/
│       ├── bin/            # Kalacakra CLI suite (kalacakra, k-interceptor, k-ai, k-aur, k-doctor)
│       └── share/kalacakra/
│           ├── fastfetch/  # Logo mandala ASCII & config Fastfetch
│           ├── locales/    # File i18n dwibahasa (id.json & en.json)
│           └── scripts/    # Battery lifespan 80% cap limiter
├── .github/workflows/      # Pipeline build OCI & bootc-image-builder ISO
└── tests/                  # Unit test suite untuk validasi CLI & keamanan
```

---

## 📜 Lisensi & Spesifikasi

* Kalacakra OS dilisensikan di bawah [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0).
* Rencana arsitektur teknis lengkap dan roadmap visi jangka panjang dapat dibaca di [plan.md](plan.md).
