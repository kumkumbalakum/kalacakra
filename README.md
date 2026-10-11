# ☸️ Kalacakra OS (Roda Waktu)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Base: Fedora bootc](https://img.shields.io/badge/Base-Fedora%20bootc%20%2F%20uBlue-red.svg)](https://github.com/ublue-os)
[![Desktop: KDE Plasma 6](https://img.shields.io/badge/Desktop-KDE%20Plasma%206%20Wayland-blue.svg)](https://kde.org)
[![Language: English & Indonesian](https://img.shields.io/badge/Language-English%20%7C%20Indonesia-green.svg)](#-native-dual-language-enid)

> **Kalacakra OS** adalah distribusi Linux desktop modern berbasis *immutable / atomic container* (`bootc` / `ostree`) dengan perpaduan arsitektur **Triad**: Filosofi Stabilitas Batu Karang setara Debian, Pondasi Modern Fedora & Universal Blue, serta fleksibilitas tanpa batas Arch Linux AUR. Dilengkapi dukungan **Native Dual Language (English + Bahasa Indonesia)** dan kecerdasan buatan lokal terproteksi privasi.

---

## 📖 DAFTAR ISI
1. [Fitur Utama](#-fitur-utama-highlights)
2. [6 Fitur Dahsyat (Killer Superpowers)](#-6-fitur-dahsyat-killer-superpowers)
3. [5 Fitur Ergonomi macOS (macOS-Inspired Ergonomics)](#-5-fitur-ergonomi-macos-macos-inspired-ergonomics)
4. [5 Fitur Keandalan openSUSE (openSUSE-Inspired Engineering)](#-5-fitur-keandalan-opensuse-opensuse-inspired-engineering)
5. [5 Fitur Ketangguhan UNIX FreeBSD (FreeBSD-Inspired Engineering)](#-5-fitur-ketangguhan-unix-freebsd-freebsd-inspired-engineering)
6. [Panduan Instalasi & Deployment](#-panduan-instalasi--deployment)
7. [Panduan Penggunaan Sehari-Hari](#-panduan-penggunaan-sehari-hari)
   * [Perintah Kalacakra CLI](#1-perintah-kalacakra-cli)
   * [Universal Command Interceptor](#2-universal-command-interceptor-k-interceptor)
   * [AI Terminal Companion](#3-ai-terminal-companion-k-ai)
   * [Arch Linux AUR Integration](#4-arch-linux-aur-integration-k-aur)
   * [Dikte Suara & Pintasan Keyboard](#5-dikte-suara--pintasan-keyboard)
8. [Panduan Build Image & ISO](#-panduan-build-image--iso)
   * [Build via CI/CD Otomatis](#opsi-a-build-via-cicd-github-actions--gitea-actions)
   * [Build 100% Lokal di Komputer](#opsi-b-build-100-lokal-di-komputer-podman)
9. [Struktur Repositori](#-struktur-repositori)
10. [Lisensi & Spesifikasi](#-lisensi--spesifikasi)

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

## ⚡ 6 Fitur Dahsyat (Killer Superpowers)

### ⏳ 1. Kalacakra Rewind (Time-Travel File Recovery)
Memanfaatkan kecepatan snapshot Btrfs/Snapper untuk memutar balik waktu file yang tidak sengaja terhapus atau rusak:
```bash
kalacakra rewind list               # Lihat daftar titik waktu snapshot masa lalu
kalacakra rewind create "Sebelum edit skripsi"  # Buat titik waktu baru instan
kalacakra rewind diff 12 dok.txt    # Bandingkan versi file saat ini dengan snapshot 12
kalacakra rewind restore 12 dok.txt # Kembalikan file dalam 1 detik!
```

### 📡 2. Kalacakra Beam (P2P Local Mesh File Transfer)
Transfer file berkecepatan Gigabit lokal antar laptop Linux, Windows, Mac, dan HP Android/iPhone di Wi-Fi yang sama tanpa internet, tanpa cloud, dan tanpa flashdisk:
* **Kirim via Dolphin:** Klik kanan file mana saja -> **"Beam to Device... (Kalacakra Beam)"**.
* **Mode Terima via Terminal:**
  ```bash
  kalacakra beam receive            # Membuka server upload lokal di http://<ip>:53317
  ```

### 🖥️ 3. Kalacakra Portal (Monitor Kedua Nirkabel untuk Tablet / HP)
Jadikan iPad, tablet Android, ponsel, atau laptop lama Anda sebagai monitor kedua 60fps dengan latensi ultra-rendah melalui Wayland:
```bash
kalacakra portal start              # Aktifkan portal layar kedua
kalacakra portal stop               # Matikan portal layar kedua
```
* Buka browser di tablet Anda: `http://<IP-Laptop>:5800`. Layar kedua langsung aktif dengan dukungan input sentuh (*touch screen*) dan *pen stylus*!

### 📷 4. AI Smart Screenshot with Local OCR (`Super + Shift + T`)
Ekstrak teks secara instan dari video YouTube, gambar tutorial, atau aplikasi apa pun yang teksnya tidak bisa diblok:
* Tekan tombol **`Super + Shift + T`** -> seleksi area layar.
* Teks otomatis diekstrak menggunakan engine Tesseract offline dwibahasa (Indonesia + Inggris) dan **langsung disalin ke clipboard**.
* Opsi terjemahan instan: `kalacakra ocr --translate`.

### 🔋 5. Ultra-Battery Survival Mode (`k-survival`)
Penyelamat darurat ketika baterai laptop tersisa 10%:
```bash
kalacakra survival on               # Aktifkan mode darurat
kalacakra survival off              # Kembalikan ke mode normal
```
* **Efek:** Mengubah layar menjadi **Monokrom Grayscale** (menghemat baterai OLED hingga 40%), menurunkan refresh rate layar ke **40Hz/30Hz**, membatasi frekuensi CPU ke **800MHz**, dan menidurkan daemon latar belakang. Menambah daya tahan ekstra 1,5 – 2 jam!

### 🎮 6. Vulkan Anti-Stutter Pre-Cache Engine (`k-precache`)
Mengeliminasi *micro-stuttering* saat game Proton pertama kali dibuka:
```bash
kalacakra precache                  # Kompilasi pipeline shader DXVK/VKD3D di latar belakang
```
* Saat game dimainkan, seluruh *shader* grafis sudah terkompilasi penuh; FPS langsung terkunci mulus 60–144 FPS sejak detik pertama!

---

## 🍎 5 Fitur Ergonomi macOS (macOS-Inspired Ergonomics)

### 🔍 1. Quick Look: Pratinjau Berkas Instan 0.1s (`k-preview` / `Space` di Dolphin)
Arahkan kursor dan tekan tombol **`Spasi`** pada berkas apa pun di file manager Dolphin untuk melihat pratinjau instan tanpa menunggu aplikasi berat terbuka:
* **Markdown (`.md`)**: Dirender visual indah dengan `glow`.
* **PDF & Gambar**: Tampilan instan resolusi penuh (`okular` / `gwenview`).
* **Arsip (`.zip`, `.tar.gz`)**: Struktur isi folder arsip langsung terbaca tanpa perlu mengekstrak.
* **Source Code**: Teks program dengan pewarnaan sintaks kaya (`bat`).
```bash
kalacakra preview dokumen.pdf       # Pratinjau via CLI atau tekan Spasi di Dolphin
```

### 💡 2. Supercharged Spotlight & KRunner Apex (`k-spotlight` / `Super + Space`)
Pusat kalkulasi, konversi, dan pencarian cepat:
* **Kalkulasi Matematika Cepat**: `kalacakra spotlight "150 * 1.11"`
* **Konversi Kurs Valuta Asing**: `kalacakra spotlight "100 usd to idr"`
* **Konversi Satuan Suhu & Berat**: `kalacakra spotlight "75 kg to lbs"`, `kalacakra spotlight "30 c to f"`
* **Pertanyaan Bahasa Alami**: Pertanyaan umum otomatis dirutekan ke `k-ai` lokal.

### 🔄 3. Universal Control & Flow (`k-flow`)
Satu mouse dan satu keyboard laptop Kalacakra meluncur mulus melintasi layar laptop Windows, Mac, atau Linux lain di sebelah Anda melalui jaringan Wi-Fi lokal:
```bash
kalacakra flow server               # Berbagi mouse & keyboard sebagai host
kalacakra flow client 192.168.1.50  # Sambungkan ke host PC lain
kalacakra flow status               # Cek status koneksi Universal Control
```

### ✍️ 4. Global Text Replacement & Snippets (`k-snippet`)
Pintasan teks otomatis yang bekerja di seluruh sistem operasi (browser, editor, terminal, chat):
```bash
kalacakra snippet list              # Lihat daftar pintasan aktif
kalacakra snippet add ";;rek" "BCA 1234567890 a.n. Kalacakra"
kalacakra snippet add ";;shrug" "¯\_(ツ)_/¯"
```
Ketik `;;rek` di aplikasi mana saja, otomatis terurai menjadi nomor rekening lengkap! Kompatibel dengan Espanso.

### 🔐 5. Unified Zero-Friction Keyring & Touch ID (`k-keyring`)
Keamanan tanpa friksi setara macOS Keychain:
* **SDDM PAM Auto-Unlock**: KWallet terbuka otomatis saat login; tidak ada lagi popup *"Enter password for wallet"*.
* **Single-SignOn SSH-Agent**: Sesi kunci SSH otomatis aktif di seluruh tab terminal via `/etc/profile.d/kalacakra-ssh-agent.sh`.
* **Touch ID (Fingerprint)**: Login dan `sudo` cukup tempelkan jari pada sensor sidik jari laptop:
  ```bash
  kalacakra keyring enroll-finger   # Daftarkan sidik jari untuk login & sudo
  kalacakra keyring status          # Periksa status KWallet PAM, SSH-Agent & Touch ID
  ```

---

## 🦎 5 Fitur Keandalan openSUSE (openSUSE-Inspired Engineering)

### 🎛️ 1. Kalacakra Control Hub: YaST-Style TUI Management (`k-hub`)
Dashboard administrasi terpusat berbasis antarmuka terminal interaktif (TUI) ala YaST openSUSE yang dapat dioperasikan tanpa desktop GUI (sangat bermanfaat saat rescue mode atau via SSH):
```bash
kalacakra hub                       # Buka menu interaktif TUI
kalacakra hub --status              # Ringkasan cepat SELinux, USBGuard, Sched-ext, & Btrfs
```

### 🧪 2. Kalacakra QA: openQA-Style Automated Verification (`k-qa`)
Engine pengujian kualitas otomatis untuk memverifikasi integritas OS dan image OCI sebelum dan sesudah update:
```bash
kalacakra qa                        # Jalankan 5 uji regresi integritas sistem
kalacakra qa --json                 # Format JSON untuk automasi CI/CD pipeline
```
* Memvalidasi seluruh biner CLI, integritas kamus i18n dwibahasa, konfigurasi sysctl kernel, dan integrasi desktop Dolphin KIO.

### ⏱️ 3. Kalacakra SnapBoot: Btrfs Bootloader Integration (`k-snapboot`)
Integrasi snapshot Snapper langsung ke menu bootloader (`systemd-boot`/`GRUB`) ala `grub2-snapper-plugin` openSUSE:
```bash
kalacakra snapboot list             # Daftar snapshot yang dapat di-booting langsung
kalacakra snapboot sync             # Sinkronisasi snapshot ke entri menu bootloader
kalacakra snapboot select 2         # Atur snapshot #2 sebagai target boot berikutnya
```

### 🧩 4. Kalacakra Workload Profiles: Zypper Patterns (`k-profile`)
Pemasangan stack lingkungan kerja kurasi lengkap dalam satu perintah deklaratif tanpa mengotori host OS imutabel:
```bash
kalacakra profile list              # Lihat daftar profil beban kerja tersedia
kalacakra profile apply web-dev     # Pasang VS Code, Postman, & Arch Space Node.js
kalacakra profile apply content-creator # Pasang Kdenlive, OBS Studio, GIMP, Audacity
kalacakra profile apply data-science   # Pasang JupyterLab & Python AI space
kalacakra profile apply gaming         # Pasang Steam, Heroic, MangoHud, Gamemode
kalacakra profile apply cybersec       # Pasang Arch Space dengan tools audit jaringan
```

### 📦 5. Kalacakra 1-Click Installer & Scheme Handler (`k-pkg`)
Penangan instalasi 1-klik deklaratif ala Open Build Service (OBS) `.ymp` dan web scheme `kalacakra://`:
```bash
kalacakra pkg app.kpkg              # Pasang manifes aplikasi lokal
kalacakra pkg "kalacakra://install?name=VLC&method=flatpak&package=org.videolan.VLC"
```
* Terintegrasi dengan web browser: Klik tautan di web, sistem langsung menampilkan dialog verifikasi keamanan dan mengeksekusi instalasi sandbox terisolasi.

---

## 😈 5 Fitur Ketangguhan UNIX FreeBSD (FreeBSD-Inspired Engineering)

### 🏰 1. Kalacakra Jail: Ephemeral Disposable Sandbox (`k-jail`)
Isolasi proses dan pengujian malware/skrip asing sekali pakai ala FreeBSD Jails menggunakan Bubblewrap (`bwrap`):
```bash
kalacakra jail ./script-dari-internet.sh  # Jalankan dalam sandbox terisolasi
kalacakra jail --no-net ./malware-check  # Putus akses internet total
kalacakra jail --pure ./evaluasi.py      # Berikan direktori home kosong (disposable tmpfs)
```
* Begitu proses selesai, sandbox langsung lenyap tanpa meninggalkan jejak atau modifikasi pada host OS.

### 🧬 2. Kalacakra Boot Environments: bectl for Linux (`k-be`)
Manajemen kloning dan peralihan sistem bootable terpadu ala `bectl` ZFS FreeBSD untuk deployment atomik `bootc`/`ostree`:
```bash
kalacakra be list                       # Tampilkan status aktif (NR), space, & deployment
kalacakra be create "Eksperimen-KDE"    # Kloning deployment bootable instan
kalacakra be activate 1                 # Aktifkan deployment #1 sebagai default boot
kalacakra be destroy 2                  # Hapus pin cadangan deployment lama
```

### 🛡️ 3. Kalacakra Scrub: Btrfs Bitrot Guard (`k-scrub`)
Pemeriksa integritas blok data berkala ala ZFS scrub untuk mendeteksi *silent bitrot* dan kerusakan perangkat keras SSD:
```bash
kalacakra scrub status                  # Tampilkan ringkasan checksum blok data
kalacakra scrub start /home             # Mulai verifikasi kriptografis di latar belakang
kalacakra scrub cancel                  # Hentikan proses verifikasi
```

### 🔬 4. Kalacakra Trace: Dynamic System Profiler (`k-trace`)
Pelacak kinerja dan bottleneck sistem dinamis ala DTrace (Solaris/FreeBSD) berbasis Linux eBPF & procfs:
```bash
kalacakra trace io                      # Lacak proses yang membuat SSD bottleneck
kalacakra trace game                    # Lacak pencuri siklus CPU & frame drop saat gaming
kalacakra trace battery                 # Lacak aplikasi yang menguras daya baterai laptop
```

### ⚙️ 5. Kalacakra sysrc: Safe Atomic Config Manager (`k-sysrc`)
Pengelola variabel konfigurasi sistem bertipe dan atomik ala `sysrc` FreeBSD tanpa perlu membuka teks editor manual di `/etc`:
```bash
kalacakra sysrc                         # Tampilkan semua variabel konfigurasi aktif
kalacakra sysrc battery.limit=85        # Atur batas pengisian daya baterai ke 85%
kalacakra sysrc scx.scheduler=rusty     # Beralih penjadwal CPU eBPF ke throughput
kalacakra sysrc ai.killswitch=true      # Matikan seluruh daemon AI instan
```

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
kalacakra doctor            # Diagnosa kesehatan Btrfs, ZRAM, AI, dan integritas sistem
kalacakra clean             # Bersihkan cache Flatpak usang dan container dangling images
kalacakra install-model     # Unduh model AI lokal ke Ollama (contoh: Llama 3.2 1B)
kalacakra scx lavd          # Aktifkan scheduler gaming latensi ultra-rendah (scx_lavd)
kalacakra scx rusty         # Aktifkan scheduler kompilasi multi-core (scx_rusty)
kalacakra rebase nvidia     # Berpindah ke varian driver Nvidia tanpa install ulang OS
kalacakra battery-cap 80    # Batasi pengisian baterai laptop ke 80% (Preservasi baterai)
kalacakra lang id           # Ganti bahasa sistem ke Bahasa Indonesia (atau 'en' untuk English)
kalacakra rewind list       # Telusuri riwayat snapshot waktu file
kalacakra portal toggle     # Nyalakan/matikan monitor kedua nirkabel
kalacakra beam receive      # Buka penerima file P2P lokal
kalacakra ocr               # Jalankan tangkapan layar teks OCR
kalacakra survival toggle   # Nyalakan/matikan mode darurat hemat baterai
kalacakra precache          # Pra-kompilasi shader game Vulkan
kalacakra preview berkas.md # Quick Look pratinjau instan (Spasi di Dolphin)
kalacakra spotlight "100 $" # Kalkulasi matematika & konversi kurs cepat
kalacakra flow server       # Universal Control mouse & keyboard roaming
kalacakra snippet list      # Kelola pintasan teks global
kalacakra keyring status    # Periksa status keyring, Touch ID, & SSH-agent
kalacakra hub               # Buka Central Management TUI Dashboard (YaST-style)
kalacakra qa                # Jalankan automated system QA & regression testing
kalacakra snapboot sync     # Sinkronisasi snapshot Btrfs ke menu bootloader
kalacakra profile apply dev # Pasang stack beban kerja lengkap (Zypper Patterns)
kalacakra pkg app.kpkg      # Pasang aplikasi 1-klik deklaratif (OBS-style)
kalacakra jail ./script.sh  # Jalankan skrip di sandbox sekali pakai (FreeBSD Jails)
kalacakra be list           # Kelola Boot Environments & kloning deployment (bectl)
kalacakra scrub status      # Periksa integritas data & deteksi bitrot Btrfs (ZFS)
kalacakra trace io          # Analisis bottleneck disk & latensi game eBPF (DTrace)
kalacakra sysrc battery=85  # Atur konfigurasi sistem secara aman & atomik (sysrc)
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
  `k-ai` akan menampilkan preview perintah dan meminta konfirmasi `[Y/n/e]` sebelum dijalankan.
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
# Pasang paket dari AUR (bisa multi-paket sekaligus!)
k-aur install visual-studio-code-bin discord-canary

# Cari paket di AUR
k-aur search brave-bin

# Hapus paket
k-aur remove visual-studio-code-bin
```

---

### 5. Dikte Suara & Pintasan Keyboard
* **`Super + V`**: Buka mikrofon dikte suara offline (`whisper.cpp`). Bicara dalam Bahasa Indonesia atau Inggris, teks langsung disisipkan di kursor aktif.
* **`Super + Shift + T`**: AI Smart Screenshot OCR untuk mengambil teks dari area layar mana saja ke clipboard.
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
│   │   └── profile.d/      # Homebrew path, interceptor hooks, & SSH agent
│   └── usr/
│       ├── bin/            # Kalacakra CLI suite:
│       │                   # kalacakra, k-interceptor, k-ai, k-aur, k-doctor,
│       │                   # k-rewind, k-beam, k-portal, k-ocr, k-survival, k-precache,
│       │                   # k-preview, k-spotlight, k-flow, k-snippet, k-keyring,
│       │                   # k-hub, k-qa, k-snapboot, k-profile, k-pkg,
│       │                   # k-jail, k-be, k-scrub, k-trace, k-sysrc
│       └── share/
│           ├── applications/ # Desktop entries & scheme handler (.kpkg / kalacakra://)
│           ├── kalacakra/  # Fastfetch config, i18n locales (id/en), Justfile, shared lib
│           └── kio/        # Dolphin context menu (Beam P2P, Game Launcher, Quick Look)
├── .github/workflows/      # Pipeline build OCI & bootc-image-builder ISO
└── tests/                  # Unit test suite untuk validasi CLI & keamanan
```

---

## 📜 Lisensi & Spesifikasi

* Kalacakra OS dilisensikan di bawah [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0).
* Rencana arsitektur teknis lengkap dan roadmap visi jangka panjang dapat dibaca di [plan.md](plan.md).
