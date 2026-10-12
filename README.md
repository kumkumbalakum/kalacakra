# ☸️ Kalacakra OS (Roda Waktu)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Base: Fedora bootc](https://img.shields.io/badge/Base-Fedora%20bootc%20%2F%20uBlue-red.svg)](https://github.com/ublue-os)
[![Desktop: KDE Plasma 6](https://img.shields.io/badge/Desktop-KDE%20Plasma%206%20Wayland-blue.svg)](https://kde.org)
[![Language: English & Indonesian](https://img.shields.io/badge/Language-English%20%7C%20Indonesia-green.svg)](#-native-dual-language-enid)

> **Kalacakra OS** adalah distribusi Linux desktop modern berbasis *immutable / atomic container* (`bootc` / `ostree`) dengan filosofi **Triad**: **stabilitas batu karang** (dicapai lewat model immutable + rollback atomik, bukan dengan memakai Debian), **fondasi modern Fedora & Universal Blue** (satu-satunya basis host literal), dan **fleksibilitas ekosistem Arch AUR** (disediakan sebagai *Space container* Distrobox, bukan sebagai host). Dilengkapi dukungan **Native Dual Language (English + Bahasa Indonesia)** dan kecerdasan buatan lokal terproteksi privasi.
>
> ℹ️ **Catatan kejujuran arsitektur:** Host Kalacakra adalah **Fedora Atomic (bootc/kinoite)** murni. Debian dan Arch **tidak** dijalankan di host — keduanya tersedia sebagai *Space container* opsional via Distrobox saat Anda ingin memakai `apt`/`pacman`/AUR. "Triad" adalah *filosofi*, bukan penggabungan teknis tiga distro di level host.

---

## 📖 DAFTAR ISI
1. [Fitur Utama](#-fitur-utama-highlights)
2. [Pilar Identitas: Kalacakra Look](#-pilar-identitas-kalacakra-look)
3. [6 Fitur Dahsyat (Killer Superpowers)](#-6-fitur-dahsyat-killer-superpowers)
3. [5 Fitur Ergonomi macOS (macOS-Inspired Ergonomics)](#-5-fitur-ergonomi-macos-macos-inspired-ergonomics)
4. [5 Fitur Keandalan openSUSE (openSUSE-Inspired Engineering)](#-5-fitur-keandalan-opensuse-opensuse-inspired-engineering)
5. [5 Fitur Ketangguhan UNIX FreeBSD (FreeBSD-Inspired Engineering)](#-5-fitur-ketangguhan-unix-freebsd-freebsd-inspired-engineering)
6. [5 Fitur Keamanan Legendaris OpenBSD (OpenBSD-Inspired Security)](#-5-fitur-keamanan-legendaris-openbsd-openbsd-inspired-security)
7. [Panduan Instalasi & Deployment](#-panduan-instalasi--deployment)
8. [Panduan Penggunaan Sehari-Hari](#-panduan-penggunaan-sehari-hari)
   * [Perintah Kalacakra CLI](#1-perintah-kalacakra-cli)
   * [Universal Command Interceptor](#2-universal-command-interceptor-k-interceptor)
   * [AI Terminal Companion](#3-ai-terminal-companion-k-ai)
   * [Arch Linux AUR Integration](#4-arch-linux-aur-integration-k-aur)
   * [Dikte Suara & Pintasan Keyboard](#5-dikte-suara--pintasan-keyboard)
9. [Panduan Build Image & ISO](#-panduan-build-image--iso)
   * [Build via CI/CD Otomatis](#opsi-a-build-via-cicd-github-actions--gitea-actions)
   * [Build 100% Lokal di Komputer](#opsi-b-build-100-lokal-di-komputer-podman)
10. [Struktur Repositori](#-struktur-repositori)
11. [Lisensi & Spesifikasi](#-lisensi--spesifikasi)

---

## ✨ Fitur Utama (Highlights)

* 🎨 **Kalacakra Look (`kalacakra look`) — Fitur Ikonik:** Ubah seluruh identitas desktop (tema KDE, skema warna, wallpaper, kursor, ikon, font, terminal, fastfetch) dengan **satu perintah**: `kalacakra look apply mandala-cyberpunk`. 5 preset siap pakai (Mandala Cyberpunk, Nusantara Bronze, Obsidian Minimal, Aurora Borealis, Kraton Gold), tersimpan sebagai konfigurasi *user* (aman untuk host immutable), **bisa di-rollback penuh**, dan dilengkapi `--screenshot` yang langsung menghasilkan caption siap-tempel untuk r/unixporn.
* 🛡️ **Bulletproof Immutable Root:** Root filesystem (`/usr`) berstatus *read-only*. Pembaruan sistem dilakukan secara atomik di latar belakang; sistem tidak akan pernah rusak (*zero-breakage*).
* 🔄 **Dual-Tier Rollback Engine:** Rollback root otomatis jika boot gagal 3x berturut-turut, dipadu snapshot Snapper khusus data pengguna (`@home` & `@var`).
* 🇮🇩 / 🇺🇸 **Native Dual Language (EN/ID):** Sistem dwibahasa penuh sejak boot pertama di seluruh elemen: GUI KDE Plasma 6, CLI tooling, voice Whisper, dan AI Terminal Companion.
* 🪄 **Immutable yang Tidak Menyakitkan:** `k-interceptor` kini **merekomendasikan metode terbaik secara cerdas** untuk paket yang Anda minta — mis. `sudo apt install vlc` langsung menyarankan *"opsi 1, vlc tersedia sebagai Flatpak resmi"* dan Anda cukup menekan **Enter**. Nama paket umum otomatis dipetakan ke ID Flathub. Painkiller untuk distro immutable — tanpa perlu tahu apa itu Flatpak/ostree.
* 🚀 **Universal Command Interceptor (`k-interceptor`):** Mencegat perintah `sudo apt install` atau `pacman -S` pada host imutabel dan memandu instalasi ke Flatpak, Arch Space, Debian Space, atau Homebrew tanpa kebingungan.
* ⚡ **Kernel Sched-ext (SCX Framework):** Penggantian *CPU scheduler* secara dinamis via eBPF (`scx_lavd` untuk gaming ultra-low latency, `scx_rusty` untuk kompilasi kode).
* 🤖 **Local Private AI (`k-ai`) & Voice (`k-voice` / `Super + V`):** Didukung runtime Ollama dan `whisper.cpp` offline lokal, dengan *Secret Sanitizer* otomatis untuk mencegah kebocoran data sensitif.
* 🎮 **Game Ready Profile:** Pre-configured Steam, Heroic Launcher, ProtonUp-Qt, MangoHud, gamemode, dan UMU Proton Launcher (.exe context menu).
* 🔒 **Enterprise-Grade Security:** Cosign image signature verification, SELinux Enforcing, MOK Secure Boot, USBGuard screen-lock binding, DNS-over-TLS (DoT), dan kesiapan Post-Quantum Cryptography (PQC).

---

## 🎨 Pilar Identitas: Kalacakra Look

Kalacakra bukan sekadar kumpulan tool — ia punya **identitas visual** yang bisa Anda nyalakan dalam satu perintah dan bagikan sebagai screenshot. Inilah fitur ikonik yang membedakan Kalacakra dari distro lain.

```bash
kalacakra look                       # lihat semua preset
kalacakra look apply mandala-cyberpunk   # terapkan tema
kalacakra look apply kraton-gold --screenshot   # + screenshot & caption r/unixporn
kalacakra look current               # tema apa yang aktif?
kalacakra look rollback              # kembali ke tampilan sebelumnya (aman)
kalacakra showcase                   # layar identitas siap-screenshot
```

| Preset | Nuansa |
|---|---|
| `mandala-cyberpunk` | Gradien neon magenta-cyan, gelap pekat, terinspirasi mandala Nusantara |
| `nusantara-bronze` | Tembaga-perunggu hangat yang tenang & elegan |
| `obsidian-minimal` | Hitam obsidian bersih, fokus tanpa gangguan |
| `aurora-borealis` | Hijau-teal aurora lembut dengan aksen ungu dingin |
| `kraton-gold` | Hitam keraton dengan aksen emas, mewah & sangat Indonesia |

> **Desain jujur:** Look menulis ke direktori konfigurasi **user** (XDG), sehingga *tidak* melanggar prinsip host immutable. Bila prasyarat Plasma (`plasma-apply-lookandfeel`, dll.) belum ada, langkah itu ditandai **SKIP** dengan pesan jelas — tool **tidak memalsukan keberhasilan**.

---

## 🧭 Status Implementasi (Jujur & Transparan)

README dan `plan.md` menggambarkan visi lengkap Kalacakra OS. Agar tidak menyesatkan, berikut pembagian jelas antara **yang sudah ada di repositori ini** dan **yang masih roadmap**:

**✅ Sudah diimplementasikan (ada kodenya di repo ini):**
* Seluruh 39 tool CLI di `rootfs/usr/bin/` (`kalacakra`, `k-interceptor`, `k-ai`, `k-ask`, `k-agent`, `k-semantic`, `k-aur`, `k-doctor`, `k-rewind`, `k-beam`, `k-portal`, `k-ocr`, `k-survival`, `k-precache`, `k-preview`, `k-spotlight`, `k-flow`, `k-snippet`, `k-keyring`, `k-hub`, `k-qa`, `k-snapboot`, `k-profile`, `k-pkg`, `k-jail`, `k-be`, `k-scrub`, `k-trace`, `k-sysrc`, `k-unveil`, `k-signify`, `k-pf`, `k-doas`, `k-wx`, `k-voice`, `k-game`, `k-look`, `k-showcase`, `k-welcome`).
* **Kalacakra Look** (`k-look`) — 5 preset tema lengkap dengan wallpaper SVG, penulisan konfigurasi KDE, riwayat & rollback, plus generator caption r/unixporn.
* i18n EN/ID dwibahasa (kamus `locales/en.json` & `id.json`).
* Konfigurasi sistem: hardening sysctl, DNS-over-TLS, ZRAM zstd, service AI Ollama.
* Integrasi desktop: KDE shortcuts (`.desktop`) & KIO service menu Dolphin.
* Build pipeline OCI + ISO (`Containerfile`, `Containerfile.nvidia`, GitHub Actions) & test suite (44 test).
* Secret sanitizer, safety-gate perintah destruktif, deteksi perangkat lunak yang absen (fail-soft).

**🧪 Sudah berjalan, tetapi bergantung pada komponen eksternal yang tidak dipaketkan di sini:**
* `k-aur` butuh `distrobox` + `podman` + image Arch.
* `k-beam` P2P lokal, `k-portal` (wayvnc), `k-flow` (deskflow/barrier) — backend opsional; tool memberi instruksi jika tak terpasang.
* `k-ai` butuh daemon Ollama + model yang diunduh terpisah.
* `k-voice` butuh `whisper-cli` + model `ggml-*.bin`.
* `k-game` butuh `umu-launcher` (repo Terra, tidak ada di Fedora resmi).
* `k-ai --file` & `k-ask` butuh daemon Ollama (sama seperti `k-ai`).
* `k-agent` memakai perencana berbasis aturan tanpa AI (pola konversi/arsip/pindah); perencanaan bebas butuh Ollama. Sandbox opsional butuh `bwrap`.

**🗺️ Masih roadmap (BELUM ada kodenya di repo ini):**
* Hybrid tiling Polonium (`Super + Y`).
* HDR / Wide Color Gamut pipeline bawaan.
* Konfigurasi installer Calamares (Btrfs `@/@home/@var`, LUKS2 + TPM2 auto-unlock) — ISO dihasilkan `bootc-image-builder`, bukan Calamares.
* Otomatisasi MOK Secure Boot enrollment & PQC (ML-KEM/ML-DSA) di seluruh stack.
* Vector embedding / NPU untuk `k-semantic`, dan perencanaan otonom penuh untuk `k-agent` — saat ini keduanya adalah **fondasi yang jujur** (lihat di bawah).
* Firmware-level battery cap ASUS/Lenovo (saat ini bergantung dukungan driver kernel vendor).

**⚠️ Fondasi jujur (ADA, tetapi dengan batasan yang dinyatakan terbuka):**
* `k-semantic` ada dan bekerja, tetapi indeksnya **leksikal (TF-IDF + sinonim ID/EN) di SQLite**, **bukan** vector embedding/NPU seperti target Fase 2 di `plan.md`. Ia tidak mengunggah data ke cloud dan dapat diganti mesin embedding kelak tanpa mengubah CLI.
* `k-agent` ada dan bekerja, tetapi perencana utamanya adalah **pola berbasis aturan** untuk beberapa intent (konversi gambar, arsip, pindah berkas); perencanaan bebas memerlukan `k-ai`/Ollama. Agen **menolak perintah berbahaya** dan menampilkan *action plan preview* sebelum eksekusi; sandbox nyata hanya aktif bila `bwrap` tersedia.

> Prinsip proyek ini: **jangan mengklaim fitur yang belum ada**. Setiap tool yang bergantung komponen absen akan memberi pesan instalasi yang jelas, bukan error misterius atau sukses palsu.

> **Catatan kejujuran BSD/UNIX-inspired:** Tool bertanda "OpenBSD-inspired" / "FreeBSD-inspired" adalah **reimplementasi konsep di atas primitif Linux**, bukan kode atau mekanisme OpenBSD/FreeBSD asli. Contoh: `k-unveil` memakai *bubblewrap* (bukan syscall `unveil(2)`), `k-jail` memakai user-namespace (bukan kernel jail), `k-pf` menulis aturan `nftables` (bukan pf), dan `k-wx` adalah **auditor** ELF — Linux tidak memiliki penegakan W^X bawaan seperti OpenBSD (`kern.wxabort`). Konsepnya diadopsi; jaminannya berbeda.

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

### 🖥️ 3. Kalacakra Portal (Mirror Layar ke Tablet / HP via VNC)
Pantau layar laptop di tablet, HP, atau laptop lama lewat browser pada jaringan Wi-Fi yang sama:
```bash
kalacakra portal start              # Aktifkan server VNC (wayvnc) di port 5800
kalacakra portal stop               # Matikan portal
```
* Buka `http://<IP-Laptop>:5800` di perangkat lain.
* **Cara kerja jujur:** ini adalah **mirror layar utama** (bukan layar kedua virtual), dikirim via `wayvnc`. Input yang diteruskan adalah **mouse & keyboard** — bukan sentuhan layar/stylus sebagai tablet input.
* **Keamanan:** `wayvnc` umumnya listen di semua interface **tanpa password**. Hanya gunakan di jaringan tepercaya, atau atur password di `~/.config/wayvnc/config`.

### 📷 4. AI Smart Screenshot with Local OCR (`Super + Shift + T`)
Ekstrak teks dari video, gambar tutorial, atau aplikasi apa pun:
* Tekan **`Super + Shift + T`** → seleksi area layar (`slurp` + `grim`).
* Teks diekstrak oleh `tesseract` offline dwibahasa (Indonesia + Inggris) dan **disalin ke clipboard**.
* Opsi terjemahan instan: `kalacakra ocr --translate` (dirutekan ke `k-ai` lokal).

### 🔋 5. Ultra-Battery Survival Mode (`k-survival`)
Penyelamat darurat ketika baterai tersisa sedikit:
```bash
kalacakra survival on               # Aktifkan mode darurat
kalacakra survival off              # Kembalikan ke mode normal
```
* **Efek nyata:** menurunkan refresh rate layar ke mode terendah (`kscreen-doctor`), membatasi frekuensi CPU ke 800MHz (frekuensi asli disimpan & dikembalikan saat `off`), memuat efek grayscale KWin **jika tersedia**, dan menidurkan `kalacakra-ai.service` jika sedang aktif.
* **Perkiraan:** penghematan baterai OLED dari grayscale + refresh rate rendah **bervariasi per perangkat** — umumnya terasa signifikan (<20% konsumsi layar), tetapi tidak ada angka jaminan universal. Tool ini melaporkan komponen mana yang berhasil aktif dan mana yang dilewati.

### 🎮 6. Vulkan Anti-Stutter Pre-Cache Engine (`k-precache`)
Mengurangi *micro-stuttering* saat game Proton pertama dibuka:
```bash
kalacakra precache                  # Kompilasi pipeline shader DXVK/VKD3D di latar belakang
```
* Menemukan database Fossilize Steam dan menjalankan `fossilize_replay` (termasuk di dalam Steam runtime) untuk mengompilasi shader lebih awal.
* **Catatan jujur:** ini **mengurangi** stutter akibat kompilasi shader parsial, bukan menjamin FPS terkunci mulus sejak detik pertama — performa akhir tetap bergantung GPU, driver, dan Proton.

---

## 🍎 5 Fitur Ergonomi macOS (macOS-Inspired Ergonomics)

### 🔍 1. Quick Look: Pratinjau Berkas Instan (`k-preview` / Klik Kanan di Dolphin)
Arahkan kursor ke berkas apa pun di file manager Dolphin, klik kanan → **"Quick Look Preview (Kalacakra)"**, untuk melihat pratinjau instan tanpa membuka aplikasi berat:
* **Markdown (`.md`)**: Dirender dengan `glow`.
* **PDF & Gambar**: Tampilan instan (`okular` / `gwenview`).
* **Arsip (`.zip`, `.tar.gz`)**: Daftar isi arsip tanpa mengekstrak.
* **Source Code**: Teks program dengan pewarnaan sintaks (`bat`).
```bash
kalacakra preview dokumen.pdf       # Pratinjau via CLI atau klik kanan di Dolphin
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
* **Touch ID (Fingerprint)**: Setelah `fprintd` dikonfigurasi untuk PAM, login & sudo bisa pakai sidik jari:
  ```bash
  kalacakra keyring enroll-finger   # Daftarkan sidik jari (fprintd-enroll)
  kalacakra keyring status          # Periksa status KWallet PAM, SSH-Agent & Touch ID
  ```
  *Catatan jujur:* pendaftaran sidik jari dilakukan di sini, tetapi **aktivasi PAM login/sudo** (`pam_fprintd`) tetap memerlukan konfigurasi root di `/etc/pam.d/` — `k-keyring` tidak melakukannya secara otomatis agar tidak merusak konfigurasi PAM sistem.

### 🎙️ 6. Diktir Suara Offline (`k-voice` / `Super + V`)
Rekam mikrofon, transkripsi lokal dengan `whisper.cpp`, hasil disalin ke clipboard — tanpa cloud:
```bash
kalacakra install-whisper-model small   # Unduh model ggml sekali saja
kalacakra voice                         # Rekam 8 detik, transkripsi, salin ke clipboard
kalacakra voice -d 15 -l id             # Durasi 15 detik, bahasa Indonesia
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

## 🔒 5 Fitur Keamanan Legendaris OpenBSD (OpenBSD-Inspired Security)

Terinspirasi dari moto *"Secure by Default, Proactive Auditing & Simplicity"* OpenBSD, Kalacakra mengintegrasikan proteksi tingkat sistem pertahanan dan isolasi path:

### 🛡️ 1. Kalacakra Unveil: Path & Namespace Isolation (`k-unveil`)
Isolasi aplikasi ketat ala `unveil(2)` dan `pledge(2)` OpenBSD. Membuka hanya path direktori yang ditentukan secara eksplisit dan menyembunyikan direktori privat (`~/.ssh`, `~/.gnupg`) dengan tmpfs sekali pakai:
```bash
kalacakra unveil --ro /usr --rw ~/Documents --hide-home libreoffice doc.odt
kalacakra unveil --ro ~/Photos --no-net feh ~/Photos/sample.png  # Isolasi offline total
kalacakra unveil --dry-run --ro /usr bash                        # Pratinjau susunan isolasi bwrap
```

### 🔑 2. Kalacakra Signify: Ed25519 Cryptographic Verifier (`k-signify`)
Penandatanganan dan verifikasi tanda tangan kriptografis berbasis kurva Edwards25519 ala `signify(1)` OpenBSD dengan kecepatan ultra-tinggi (<5ms) dan kebal celah tanpa kompleksitas PGP/GPG:
```bash
kalacakra signify generate              # Buat pasangan kunci Ed25519 baru (Mode 0600)
kalacakra signify sign -s key.sec -m update.tar.gz    # Tandatangani berkas/manifes
kalacakra signify verify -p key.pub -m update.tar.gz  # Verifikasi integritas instan
kalacakra signify status                # Periksa kunci yang tersedia di sistem
```

### 🧱 3. Kalacakra PF: Declarative Desktop Firewall & Panic Killswitch (`k-pf`)
Firewall desktop deklaratif ala OpenBSD Packet Filter (`pf` / `pfctl`) di atas Linux `nftables` dengan tombol darurat pemutus jaringan (*Panic Killswitch*):
```bash
kalacakra pf status                     # Tampilkan ringkasan aturan tabel firewall aktif
kalacakra pf panic                      # Mode Panik Darurat: Putus semua trafik internet luar!
kalacakra pf unpanic                    # Pulihkan koneksi normal kembali
kalacakra pf block-app untrusted-app    # Blokir akses internet keluar per-aplikasi (Anchor)
kalacakra pf allow-app untrusted-app    # Cabut blokir akses internet aplikasi
```

### ⚡ 4. Kalacakra doas: Safe Minimalist Privilege Elevation (`k-doas`)
Alternatif eksekusi hak istimewa administratif minimalis ala OpenBSD `doas(1)` dengan konfigurasi deklaratif ringkas di `/etc/doas.conf` dan pencatatan audit di `/var/log/kalacakra/doas.log`:
```bash
kalacakra doas check                    # Validasi sintaks & izin keamanan doas.conf
kalacakra doas init                     # Buat template aturan aman untuk grup wheel
kalacakra doas k-rewind list            # Eksekusi perintah administratif cepat
```

### 🧬 5. Kalacakra W^X: Memory Exploit Mitigation Auditor (`k-wx`)
Auditor kepatuhan proteksi memori biner dan pengerasan kernel ala OpenBSD *Write XOR Execute* (W^X):
```bash
kalacakra wx audit /usr/bin/firefox     # Audit segmen RWX & proteksi NX stack binary ELF
kalacakra wx scan --dir ~/.local/bin     # Pindai seluruh biner lokal pengguna
kalacakra wx check-kernel               # Periksa proteksi eksploitasi kernel (ASLR, YAMA, Ptrace)
kalacakra wx enforce                    # Terapkan konfigurasi pengerasan memori sysctl
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
kalacakra unveil --ro /usr app  # Isolasi path & namespace filesystem (OpenBSD unveil)
kalacakra signify verify -p key.pub -m pkg # Verifikasi Ed25519 ultra-cepat (signify)
kalacakra pf panic              # Mode panik killswitch darurat pemutus jaringan (pf)
kalacakra doas check            # Validasi aturan elevasi hak akses aman (doas)
kalacakra wx audit /usr/bin/app # Audit kepatuhan memori biner W^X & mitigasi exploit
kalacakra look list             # Lihat semua preset identitas desktop (fitur ikonik)
kalacakra look apply kraton-gold --screenshot  # Terapkan tema + screenshot & caption
kalacakra look rollback         # Kembalikan tampilan sebelumnya (aman, tanpa data loss)
kalacakra showcase              # Layar identitas siap-screenshot untuk r/unixporn
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
* **`Super + V`**: Diktir suara **offline** (`k-voice`, tenaga `whisper.cpp`). Rekam mikrofon 8 detik, transkripsi lokal, hasil **disalin ke clipboard** (Ctrl+V untuk menempel). Model harus diunduh dulu ke `~/.cache/whisper/`.
* **`Super + Shift + T`**: `k-ocr` — seleksi area layar, OCR lokal (`tesseract`), hasil ke clipboard.
* **`Super + Space`**: `k-spotlight` — kalkulasi matematika, konversi kurs/satuan, dan pertanyaan umum yang dirutekan ke `k-ai`.
* Pintasan di atas dideklarasikan lewat berkas `.desktop` dengan `X-KDE-Shortcuts` di `/usr/share/applications/`. Jika desktop Anda tidak menanganinya otomatis, daftarkan manual di **System Settings → Shortcuts → Custom Shortcuts**.
* **Game Windows Non-Steam:** Klik kanan file `.exe` di Dolphin → **"Jalankan dengan Kalacakra Game Launcher (Proton UMU)"**, atau via CLI:
  ```bash
  kalacakra game installer.exe              # Jalankan .exe via Proton UMU
  kalacakra game game.exe --game-id umu-starcitizen --proton GE-Proton
  ```
  *Catatan jujur:* wrapper ini membutuhkan `umu-run` (paket `umu-launcher`, tersedia di **repo Terra** — tidak ada di Fedora resmi/RPMFusion). Jika belum terpasang, `k-game` memberi instruksi instalasi, bukan error misterius.

---

## 🔨 Panduan Build Image & ISO

### Opsi A: Build via CI/CD (GitHub Actions / Gitea Actions)
Repositori ini telah dilengkapi workflow CI/CD otomatis di `.github/workflows/`:
1. Push commit ke branch `main`.
2. Workflow `build-oci.yml` otomatis membangun dan menandatangani image dengan Cosign.
3. Jalankan workflow `build-iso.yml` untuk menghasilkan file ISO installer bootable.

### Opsi B: Build 100% Lokal di Komputer (Podman)
Jika ingin mem-build secara lokal tanpa layanan cloud, ada **script pembantu** yang meniru workflow CI:

```bash
# Cek prasyarat dulu (engine container, disk, RAM)
scripts/build-local.sh check

# Build image OCI lokal (default: base). Varian: base | nvidia
scripts/build-local.sh image base
scripts/build-local.sh image nvidia

# Build ISO bootable (butuh podman + sudo, karena bootc-image-builder butuh --privileged)
scripts/build-local.sh iso
```

Atau lewat resep Justfile (jika `just` terpasang):

```bash
just build-check          # cek prasyarat
just build-image base     # atau: just build-image nvidia
just build-iso            # butuh podman + sudo
```

> **Catatan jujur:** CI resmi (Universal Blue) memakai **podman/buildah**. Script ini otomatis memakai podman bila ada, dan jatuh ke **docker** bila tidak. Karena `Containerfile` memuat `rpm-ostree install`, build lewat docker **bisa** berbeda/gagal — itu keterbatasan docker, **belum tentu bug Containerfile**. Untuk hasil setara CI, gunakan podman:
> ```bash
> sudo apt install -y podman
> ```

Jika lebih suka manual tanpa script:

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
├── STRATEGY.md             # Peta jalan viral (identitas, painkiller, cerita Indonesia)
├── Containerfile           # Image base OCI (Mesa / AMD Radeon / Intel)
├── Containerfile.nvidia    # Image base OCI dengan driver proprietary Nvidia
├── Justfile                # Resep deklaratif otomatisasi sistem
├── scripts/
│   └── build-local.sh      # Pembantu build image & ISO lokal (meniru CI)
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
│       │                   # k-jail, k-be, k-scrub, k-trace, k-sysrc,
│       │                   # k-unveil, k-signify, k-pf, k-doas, k-wx,
│       │                   # k-voice, k-game, k-look, k-showcase
│       └── share/
│           ├── applications/ # Desktop entries & scheme handler (.kpkg / kalacakra://)
│           ├── kalacakra/  # Fastfetch config, i18n locales (id/en), Justfile, shared lib
│           │   └── look/   # Preset tema Look (JSON) + wallpaper SVG (fitur ikonik)
│           └── kio/        # Dolphin context menu (Beam P2P, Game Launcher, Quick Look)
├── .github/workflows/      # Pipeline build OCI & bootc-image-builder ISO
└── tests/                  # Unit test suite untuk validasi CLI & keamanan
```

---

## 📜 Lisensi & Spesifikasi

* Kalacakra OS dilisensikan di bawah [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0).
* Rencana arsitektur teknis lengkap dan roadmap visi jangka panjang dapat dibaca di [plan.md](plan.md).
* Peta jalan identitas & viral (jujur, berbasis pilar) dapat dibaca di [STRATEGY.md](STRATEGY.md).
