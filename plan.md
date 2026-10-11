# **Dokumentasi Spesifikasi & Rencana Proyek: Kalacakra OS**

Dokumentasi ini dirancang sebagai **Architecture & Implementation Specification** komprehensif untuk Kalacakra OS. Dokumen ini dapat langsung diumpankan (*prompting*) ke AI tingkat lanjut saat mengeksekusi pembuatan kode, konfigurasi skrip, manifest build Containerfile, maupun modul pendukung sistem.

---

## **1. Ringkasan Eksekutif & Filosofi Desain**

* **Nama Proyek:** Kalacakra OS (Roda Waktu / Siklus Abadi)
* **Kategori:** Modern Immutable Desktop Linux Distribution (General-Purpose, Developer & Power-User)
* **Pondasi Konseptual (Triad Architecture):**
  * **Stabilitas Batu Karang (Rock-Solid Stability - Filosofi Setara Debian):** Root filesystem read-only/imutabel, pembaruan atomik berbasis OCI container image (*bootc/ostree*), sistem anti-rusak (*bulletproof*), dan zero-breakage update.
  * **Inovasi & Standar Modern (Basis Fedora & Universal Blue):** Wayland native, PipeWire audio graph, layout Btrfs subvolume + kompresi Zstandard, integrasi kernel performa tinggi (`sched-ext` / SCX + NPU acceleration), dan pengiriman image OCI terverifikasi.
  * **Fleksibilitas Tanpa Batas (Ekosistem Arch Linux & Cloud Native):** Akses transparan dan aman ke Arch User Repository (AUR), Homebrew on Linux, serta toolchain bleeding-edge melalui subsistem terisolasi (*Podman + Distrobox*) tanpa mengotori host OS.
* **Prinsip Utama:**
  * **Native Dual Language (English + Bahasa Indonesia First-Class Citizen):** Dukungan dwibahasa penuh dan setara sejak boot pertama di seluruh elemen: GUI KDE Plasma, pesan CLI suite, model AI/Voice, hingga dokumentasi tanpa memerlukan unduhan bahasa terpisah.
  * **100% Privacy-First & Zero-Telemetry:** Integrasi AI bersifat transparan, offline lokal secara default, tanpa telemetri pihak ketiga, dan memiliki opsi matikan instan (*kill-switch*) satu klik.
  * **Enterprise-Grade Defense-in-Depth & PQC-Ready:** Keamanan multi-lapis aktif secara default (SELinux Enforcing, OCI Cosign verification, USBGuard, MOK Secure Boot, DNS-over-TLS, dan roadmap Post-Quantum Cryptography).
  * **Zero Friction UX:** Pengalaman boot pertama siap pakai (*out-of-the-box*) untuk gaming, coding, dan produktivitas tanpa perlu konfigurasi manual berbelit-belit.
  * **Zero-Reinstall OS Lifecycle:** Migrasi varian hardware (seperti berpindah ke GPU Nvidia) dilakukan via *atomic rebase* dalam satu perintah tanpa instalasi ulang OS.
* **Target Pengguna:** Pengembang software, DevOps engineer, gamer, kreator konten, dan pengguna harian baik di Indonesia maupun komunitas global yang menginginkan sistem operasi modern yang indah, kencang, stabil seumur hidup, dan aman.

---

## **2. Arsitektur Teknis Sistem (System Architecture)**

```
+-----------------------------------------------------------------------+
|                       USER INTERACTION LAYER                          |
|  KDE Plasma 6 (Wayland) [EN/ID] | Polonium Tiling | Control Hub [EN/ID]|
|  Ptyxis Container Terminal | Global AI/Whisper HUD | HDR/WCG Pipeline |
+-----------------------------------------------------------------------+
|                       COGNITIVE & APP DELIVERY                        |
| Flatpak (Flathub GUI) | Kalacakra Spaces (Distrobox) | Homebrew CLI   |
| Universal Interceptor | Recipe Runner (kalacakra CLI)| Declarative Dot|
+-----------------------------------------------------------------------+
|                       SMART SERVICES & SECURITY                       |
|  k-ai Daemon (Ollama) | Whisper Voice (EN+ID)  | Semantic Vector Index|
|  k-agent System Auto  | USBGuard Screen-Lock   | Secret Sanitizer     |
|  DNS-over-TLS (DoT)   | Tailscale Mesh Hub     | Battery 80% Lifespan |
+-----------------------------------------------------------------------+
|                       CORE IMMUTABLE OS                               |
| Read-Only Root (/usr) | Atomic Updates (bootc / ostree) | ZRAM/zstd   |
| SELinux (Enforcing)   | Cosign Verification    | Kernel Sysctl Hardened|
| MicroVM Isolated Pods (Zero-Trust Sandbox)     | PQC Cryptography     |
+-----------------------------------------------------------------------+
|                       STORAGE & HETEROGENEOUS KERNEL                  |
| Btrfs (@, @home, @var, @snapshots) | Snapper (User Data Rollback)     |
| Linux Kernel + sched-ext (scx_lavd / scx_rusty) eBPF CPU Schedulers   |
| NPU Acceleration Subsystem (Intel IVPU / AMD XDNA / Qualcomm QAIC)    |
| TPM2 Auto-Unlock (LUKS2 Full Disk Encryption)                         |
+-----------------------------------------------------------------------+
```

### **2.1 File System & Partitioning Scheme (Btrfs Layout)**

Pemasangan partisi otomatis menggunakan subvolume Btrfs terisolasi:

* `@` -> Mounted ke `/` (Sistem root imutabel / target deployment OCI ostree).
* `@home` -> Mounted ke `/home` (Data persisten pengguna, konfigurasi dotfiles, Homebrew prefix).
* `@var` -> Mounted ke `/var` (Data dinamis, flatpak runtimes, container images Podman, cache lokal).
* `@snapshots` -> Mounted ke `/.snapshots` (Penyimpanan state snapshot Snapper khusus `@home` & `@var`).
* **Kompresi:** `compress=zstd:1` diaktifkan secara default pada level filesystem untuk efisiensi ruang simpan SSD/NVMe dan peningkatan throughput I/O.
* **Swap Engine:** Menggunakan **ZRAM** berbobot 100% dari kapasitas RAM fisik dengan kompresi `zstd`, dipadu `systemd-oomd` untuk mencegah *freeze* sistem saat beban komputasi puncak.
* **Keamanan Disk:** Dukungan enkripsi partisi penuh LUKS2 dengan auto-unlock terikat hardware **TPM2** (*Trusted Platform Module*) via `systemd-cryptenroll`.

### **2.2 Dual-Tier Rollback Engine (Pemisahan Tanggung Jawab Rollback)**

1. **Tier 1 - Root OS Atomic Rollback (bootc / ostree):**
   * Pembaruan OS dilakukan secara atomik di latar belakang. Setiap pembaruan menghasilkan entri deployment baru di bootloader (`systemd-boot` / `GRUB`).
   * **Auto-Healing Boot Guard:** Menggunakan penghitung boot (`bootctl mark-bad` / `systemd-boot assessment`). Jika sistem mengalami kegagalan booting 3 kali berturut-turut pasca-update, bootloader otomatis beralih kembali (*automatic fallback rollback*) ke deployment OCI sebelumnya yang terbukti stabil.
   * Rollback manual dapat dilakukan sewaktu-waktu melalui menu boot atau perintah `kalacakra rollback`.
2. **Tier 2 - User & App State Rollback (Snapper Engine):**
   * Snapper didedikasikan khusus memantau subvolume `@home` dan data aplikasi di `@var`.
   * Melindungi data pengguna dari kesalahan penghapusan file, eksperimen konfigurasi yang salah, atau kerusakan data lokal tanpa menyentuh root filesystem OCI.

---

## **3. Strategi Pengiriman Aplikasi & User Experience**

### **3.1 Multi-Layer Delivery**

1. **Layer 1 - Aplikasi Desktop Sehari-hari (Flatpak / Flathub):**
   * Backend standar aplikasi GUI (Browser, LibreOffice, VLC, GIMP, Spotify, Steam, Obsidian).
   * Dikelola via GUI Software Center (KDE Discover) dengan integrasi **Flatseal** pre-installed untuk kontrol izin keamanan granular.
2. **Layer 2 - Utilitas Inti & Driver Perangkat Keras (Native Base):**
   * Driver GPU (Mesa untuk AMD/Intel, driver proprietary Nvidia pre-baked & signed), PipeWire, firmware hardware, network stack, dan shell inti.
3. **Layer 3 - Developer Toolchains & Homebrew on Linux:**
   * Dukungan **Homebrew** (`/home/linuxbrew`) terintegrasi *out-of-the-box* untuk paket CLI modern (`gh`, `ripgrep`, `k9s`, `kubectl`, dll.) tanpa mencemari sistem root.
4. **Layer 4 - Kalacakra Spaces & Ekosistem Arch (Podman + Distrobox):**
   * Lingkungan container rootless *out-of-the-box*.
   * Wrapper CLI `k-aur`: Memungkinkan instalasi paket atau script dari Arch User Repository (AUR) ke dalam container Arch terisolasi, lalu mengekspor biner dan shortcut `.desktop` ke host secara otomatis.
   * GUI Manager di Kalacakra Control Hub untuk memantau container aktif.

### **3.2 Universal Command Interceptor (The No-Confusion Shell)**

Fitur ramah pengguna baru untuk mengatasi kendala utama distro imutabel. Pesan interceptor secara dinamis mengikuti preferensi bahasa sistem:

* **Mode Bahasa Indonesia (`LANG=id_ID.UTF-8`):**
  ```text
  [Kalacakra Interceptor] Host sistem Anda berstatus Imutabel (Terproteksi).
  Paket '<nama_paket>' tersedia. Pilih metode instalasi yang diinginkan:
    [1] Flatpak (Rekomendasi untuk aplikasi Desktop / GUI)
    [2] Kalacakra Space (Arch Linux Container / AUR via k-aur)
    [3] Kalacakra Space (Debian / Ubuntu Container)
    [4] Homebrew on Linux (CLI tool terisolasi di /home)
    [5] Layer ke Host OS (rpm-ostree - memerlukan reboot)
  Pilihan Anda [1-5]:
  ```
* **English Mode (`LANG=en_US.UTF-8`):**
  ```text
  [Kalacakra Interceptor] Your host system is Immutable (Protected).
  Package '<package_name>' is available. Choose preferred installation method:
    [1] Flatpak (Recommended for Desktop / GUI apps)
    [2] Kalacakra Space (Arch Linux Container / AUR via k-aur)
    [3] Kalacakra Space (Debian / Ubuntu Container)
    [4] Homebrew on Linux (Isolated CLI tool in /home)
    [5] Layer to Host OS (rpm-ostree - requires reboot)
  Your choice [1-5]:
  ```

### **3.3 Container-Aware Terminal: Integrasi Ptyxis**

* **Default Terminal:** Menggunakan **Ptyxis**, terminal emulator modern berbasis GPU yang dirancang khusus untuk alur kerja container.
* **Visual Space Badges:** Setiap tab terminal menampilkan indikator container yang jelas (`[Host]`, `[Arch Space]`, `[Ubuntu Dev]`).
* **One-Click Space Spawn:** Membuka tab shell baru di dalam container Distrobox langsung dari menu klik kanan tab tanpa perlu mengetik manual `distrobox enter`.

### **3.4 Arsitektur Dual Language Native (English + Bahasa Indonesia)**

Kalacakra OS memperlakukan Bahasa Indonesia dan Bahasa Inggris sebagai warga kelas satu (*first-class citizens*):

1. **System Locales Pre-Generated:**
   * Kedua locale `en_US.UTF-8` dan `id_ID.UTF-8` digenerate secara default di image base. Pengguna tidak perlu menjalankan `locale-gen` atau men-download file tambahan.
2. **Paket Bahasa Desktop Lengkap:**
   * Terpasang bawaan: `glibc-langpack-id`, `glibc-langpack-en`, `langpacks-id`, `langpacks-en`, serta paket terjemahan KDE Plasma 6. Seluruh menu sistem, setting, dialog, dan Discover langsung berubah seketika saat bahasa dialihkan.
3. **i18n CLI Architecture (Kalacakra Tooling):**
   * Semua utilitas buatan Kalacakra (`kalacakra`, `k-interceptor`, `k-ai`, `k-doctor`, `k-aur`, `k-semantic`) dibangun dengan arsitektur internasionalisasi (i18n).
   * Otomatis membaca variabel `$LANG`. Menyediakan opsi manual: `kalacakra --lang id` atau `kalacakra --lang en`, serta dapat dialihkan via GUI Kalacakra Control Hub.
4. **Dokumentasi & Halaman Bantuan Dwibahasa:**
   * Perintah `man` dan panduan online tersedia lengkap dalam dua versi bahasa: English dan Bahasa Indonesia.

---

## **4. Performa Tinggi, Kernel Sched-ext & Komputasi NPU**

### **4.1 Dynamic eBPF CPU Schedulers (`sched-ext` / SCX)**
Kalacakra OS menyertakan dukungan kernel `sched-ext` out-of-the-box, memungkinkan pergantian algoritma penjadwalan CPU secara dinamis tanpa kompilasi ulang kernel atau reboot:

1. **`scx_lavd` (Low Latency / Game Mode):**
   * Penjadwal yang sadar latensi kritis. Memprioritaskan frame loop game dan thread interaktif untuk mengeliminasi *micro-stuttering* dan meminimalkan latensi input mouse/keyboard.
   * Diaktifkan secara otomatis saat Game Mode menyala.
2. **`scx_rusty` (Throughput / Multi-Thread Workload):**
   * Penjadwal berbasis Rust yang memaksimalkan saturasi seluruh core/threads CPU saat proses berat seperti kompilasi kode (`cargo build`, `make -j`), rendering Blender, atau pelatihan model lokal.
3. **Default Kernel Scheduler (EEVDF):**
   * Digunakan untuk penggunaan normal dan komputasi hemat daya pada laptop baterai.

### **4.2 NPU Hardware Acceleration Subsystem (Hemat Daya Ekstrem)**
* Mengaktifkan modul driver kernel `accel` modern: **`intel-ivpu`** (Intel Core Ultra / Lunar Lake), **`amd-xdna`** (Ryzen AI Strix Point / Hawk Point), dan **`qaic`** (Qualcomm Snapdragon X Elite).
* Engine AI lokal (Ollama / whisper.cpp) otomatis memprioritaskan inferensi ke NPU jika hardware terdeteksi.
* Menjalankan dikte suara dan LLM lokal dengan konsumsi daya hanya 3–7 Watt, menjaga baterai laptop tetap tahan 10–15 jam saat AI bekerja di latar belakang.

---

## **5. Spesifikasi Integrasi Kecerdasan Buatan & Cognitive Stack**

### **5.1 Dual-Engine Architecture & Privasi**

* **Local Private Engine (Default & 100% Offline):**
  * Runtime: Biner resmi **Ollama** atau **llama.cpp** yang terdaftar sebagai *systemd user service* (`kalacakra-ai.service`).
  * Konfigurasi Model: Installer ISO tidak memaketkan model raksasa. Wizard boot pertama mendeteksi kapasitas VRAM/NPU/RAM dan menawarkan unduhan model lokal hemat daya (1B–3B parameter seperti Llama-3.2-1B/3B atau Qwen-2.5-Coder) yang dioptimalkan untuk bilingual EN-ID.
* **Cloud / BYOK Engine (Bring Your Own Key):**
  * Antarmuka GUI di Kalacakra Control Hub untuk menghubungkan API keys (OpenAI, Anthropic, Gemini, Groq, atau endpoint LiteLLM lokal/organisasi).
* **Privacy Shield & Kill-Switch:**
  * Zero-telemetry di seluruh komponen sistem.
  * Sakelar instan (*kill-switch*) di taskbar dan System Settings untuk mematikan seluruh daemon AI bagi pengguna yang tidak ingin menggunakannya.

### **5.2 Fitur Native AI & Voice (Bilingual Support)**

1. **k-ai Terminal Companion (Dwibahasa):**
   * Menerjemahkan bahasa alami ke perintah Bash dengan *safety gate* (preview perintah, analisis dampak, konfirmasi `[Y/n]`).
   * Memahami instruksi pengguna dalam Bahasa Indonesia maupun English (contoh: *"cari file lebih dari 100MB"* atau *"find files larger than 100MB"* menghasilkan perintah `find . -size +100M`).
   * Auto-diagnostik error terminal: Menganalisis output stderr ketika perintah gagal (exit code != 0) dan memberikan saran perbaikan interaktif dalam bahasa pilihan pengguna.
2. **Offline Global Voice-to-Text (`Super + V` - EN & ID):**
   * Integrasi **whisper.cpp** yang berjalan 100% lokal (NPU/GPU/CPU) dengan model multilingual yang dioptimalkan untuk mengenali ucapan Bahasa Indonesia dan English secara akurat.
   * Menekan pintasan `Super + V` membuka overlay mikrofon minimalis; ucapan langsung ditranskripsi ke teks dan disisipkan di posisi kursor aplikasi apa pun tanpa perlu koneksi internet.
3. **OS-Wide Selection Assistant (`Super + Space`):**
   * HUD popup saat teks diseleksi:
     * **Translate:** Terjemahan instan dua arah (Bahasa Indonesia ↔ English) dan bahasa utama dunia lainnya.
     * **Proofread:** Memperbaiki tata bahasa dan ejaan dalam Bahasa Indonesia maupun English.
     * **Summarize:** Peringkasan teks dokumen/artikel.
4. **KRunner Quick AI Integration:**
   * Runner desktop cerdas untuk perhitungan cepat, konversi waktu, kalkulasi kode, dan peringkasan tanpa membuka browser.

### **5.3 AI Secret Sanitizer & Data Leak Guardrails (K-AI Shield)**
* **Local Regex Secret Redaction:** `k-ai` secara otomatis memindai dan menyensor token sensitif (misal: API key `ghp_...`, `AKIA...`, `Bearer eyJ...`, blok `BEGIN PRIVATE KEY`, password) sebelum prompt dikirim ke engine AI lokal maupun cloud.
* **Protected File Blacklist:** `k-ai` menolak membaca atau menyertakan isi berkas direktori sensitif (`~/.ssh/`, `~/.gnupg/`, `~/.aws/`, `.env`) ke dalam konteks penalaran.

### **5.4 Local Semantic Vector Indexing Daemon (`k-semantic`)**
* Daemon cerdas berbasis vector embedding lokal (NPU accelerated).
* Mengindeks dokumen lokal (PDF, Markdown, catatan, repositori kode) secara berkala tanpa mengunggah 1 byte pun ke cloud.
* Pengguna dapat mencari file di Dolphin dan KRunner berdasarkan makna semantik dalam Bahasa Indonesia maupun English (contoh: *"surat perjanjian sewa tahun lalu"* atau *"auth token middleware function"*).

### **5.5 Autonomous Task Agent (`k-agent`)**
* Agen eksekusi tugas otonom multi-langkah di tingkat sistem operasi.
* Menerima instruksi dalam Bahasa Indonesia maupun English (misal: *"Konversi semua gambar PNG di folder Downloads menjadi WebP, buat arsip zip, lalu pindahkan ke folder Backup"*).
* Bekerja di dalam sandbox terisolasi dengan verifikasi rencana (*action plan preview*) sebelum eksekusi dimulai.

---

## **6. Fitur Penunjang Desktop, Gaming & Power-User**

### **6.1 Gaming Stack "Out-of-the-Box" (Game-Ready Profile)**
* Pre-configured: **Steam**, **Heroic Games Launcher**, **ProtonUp-Qt**, dan **UMU Launcher** (Unified Metal Underlayer).
* **Context Menu Dolphin (.exe Launcher):** Klik kanan file installer atau executable Windows `.exe` -> *"Jalankan dengan Kalacakra Game Launcher (Proton UMU)"* / *"Run with Kalacakra Game Launcher (Proton UMU)"*.
* Optimasi performa: Integrasi `gamemode`, `gamescope`, dan MangoHud overlay.
* **Game Mode Taskbar Toggle:**
  * Menonaktifkan compositor unredirect.
  * Mengaktifkan CPU scheduler `scx_lavd` via eBPF.
  * Mengatur CPU governor ke mode `performance`.

### **6.2 Hybrid Dynamic Tiling Window Manager (Polonium on KDE Plasma 6)**
* Menggabungkan kenyamanan floating window KDE Plasma 6 dengan kecepatan tiling ala Hyprland/COSMIC.
* **Pintasan Toggle `Super + Y`:** Mengaktifkan atau menonaktifkan mode Auto-Tiling seketika.
* Mendukung layout *binary split*, *half-screen*, dan multi-monitor per-workspace management secara Wayland-native.

### **6.3 Layar & Warna Profesional: Wayland HDR & Wide Color Gamut (WCG)**
* Dukungan native untuk monitor OLED/Mini-LED HDR dengan color profile ICC akurat out-of-the-box.
* Sakelar 1-klik di taskbar untuk mengaktifkan mode HDR saat menonton konten HDR atau bermain game.

### **6.4 Kesehatan Baterai: Battery Lifespan Preservation Daemon (80% Cap)**
* Terintegrasi langsung dengan firmware laptop (ASUS, Lenovo, Dell, ThinkPad, Framework) untuk membatasi pengisian daya baterai pada ambang batas 80% (*bypass charging*).
* Menjaga masa pakai fisik baterai tetap prima hingga 5–10 tahun penggunaan.

### **6.5 Declarative Dotfiles & Workspace Sync (`kalacakra sync-config`)**
* Pengguna dapat mengikat konfigurasi desktop (`/home` dotfiles, shortcut, ekstensi KDE, daftar Flatpak) ke repositori Git pribadi.
* Saat berpindah ke laptop baru, cukup jalankan `kalacakra sync-config <git-url>` untuk mereplikasi seluruh lingkungan kerja dalam 2 menit.

### **6.6 Recipe-Driven System Management CLI (`kalacakra` CLI / `k-just`)**
Toolchain deklaratif berbasis *just* dengan dukungan dwibahasa penuh:
```bash
kalacakra update            # Perbarui host OCI, Flatpak, Homebrew, & Spaces
kalacakra clean             # Bersihkan cache lama, snapshot usang, & dangling images
kalacakra install-model     # Wizard pengunduhan model AI lokal (Llama, Qwen, DeepSeek)
kalacakra toggle-tiling     # Aktifkan/nonaktifkan auto-tiling KWin
kalacakra scx [lavd|rusty]  # Ganti dynamic CPU scheduler on-the-fly
kalacakra rebase nvidia     # Berpindah ke image driver Nvidia tanpa install ulang OS
kalacakra battery-cap 80    # Aktifkan batas pengisian baterai 80%
kalacakra lang [id|en]      # Beralih bahasa sistem seketika
kalacakra rewind list       # Telusuri riwayat titik waktu file snapshot
kalacakra portal toggle     # Nyalakan/matikan monitor kedua nirkabel untuk tablet
kalacakra beam receive      # Buka penerima file P2P lokal
kalacakra ocr               # Jalankan tangkapan layar teks OCR
kalacakra survival toggle   # Nyalakan/matikan mode darurat hemat baterai
kalacakra precache          # Pra-kompilasi shader game Vulkan
kalacakra doctor            # Menjalankan diagnostik menyeluruh sistem
```

### **6.7 Kalacakra Rewind: Time-Travel File Recovery (`k-rewind`)**
* Memanfaatkan integrasi snapshot Btrfs/Snapper untuk memutar balik waktu file atau direktori yang tidak sengaja terhapus, rusak, atau salah timpa.
* Menyediakan perbandingan versi (*visual diff*) dan pengembalian instan 1-detik tanpa membebani sistem.

### **6.8 Kalacakra Beam: P2P Local Mesh File Transfer (`k-beam`)**
* Transfer file langsung berkecepatan Gigabit lokal antar perangkat di jaringan Wi-Fi yang sama (Linux, Android, iOS, Windows, Mac) tanpa internet, cloud, atau flashdisk.
* Terintegrasi dengan menu klik kanan Dolphin (*"Beam to Device..."*) dan server upload web lokal.

### **6.9 Kalacakra Portal: Wireless Virtual Second Display (`k-portal`)**
* Mengubah iPad, tablet Android, ponsel, atau laptop lama menjadi monitor kedua nirkabel 60fps dengan latensi ultra-rendah melalui output virtual Wayland.
* Mendukung input sentuh (*touchscreen*) dan stylus pen dari tablet ke layar desktop.

### **6.10 Kalacakra OCR: AI Smart Screenshot with Local OCR (`k-ocr` / `Super + Shift + T`)**
* Mengambil tangkapan layar area mana saja dan mengekstrak teks secara instan menggunakan engine Tesseract offline dwibahasa (Indonesia + Inggris).
* Teks hasil ekstraksi otomatis disalin ke clipboard dan siap diterjemahkan via `k-ai`.

### **6.11 Kalacakra Survival: Ultra-Battery Emergency Mode (`k-survival`)**
* Penyelamat darurat saat baterai laptop tersisa di bawah 10%:
  * Mengaktifkan filter layar monokrom grayscale untuk menghemat daya layar OLED hingga 40%.
  * Menurunkan refresh rate layar ke 40Hz/30Hz.
  * Membatasi frekuensi CPU maksimum ke 800MHz dan menidurkan proses AI latar belakang, memberikan daya tahan ekstra 1,5–2 jam.

### **6.12 Kalacakra Precache: Vulkan Anti-Stutter Shader Engine (`k-precache`)**
* Pra-kompilasi pipeline shader DXVK/VKD3D secara otomatis di latar belakang saat game Steam/Heroic/Lutris dipasang.
* Menghilangkan *micro-stuttering* saat game pertama kali dibuka, menjamin gameplay terkunci pada 60–144 FPS sejak detik pertama.

---

## **7. Arsitektur Keamanan Sistem (Enterprise-Grade Security Hardening)**

Menerapkan prinsip *defense-in-depth* komprehensif untuk melindungi dari ancaman siber, fisik, maupun supply chain:

### **7.1 Supply Chain Integrity: OCI Image Signing via Sigstore / Cosign**
* Seluruh OCI container image Kalacakra ditandatangani secara kriptografis menggunakan **Cosign** di pipeline build GitHub Actions resmi.
* Client policy (`/etc/containers/policy.json`) dikonfigurasi untuk memverifikasi tanda tangan publik Kalacakra sebelum mengizinkan penulisan deployment baru melalui `bootc update`. Pembaruan yang tidak tertandatangani atau rusak akan ditolak otomatis.

### **7.2 Secure Boot & MOK (Machine Owner Key) Management**
* Mendukung penuh UEFI Secure Boot modern dengan sertifikat ganda (kompatibel dengan standar key update 2026).
* Modul kernel kustom dan driver proprietary Nvidia ditandatangani menggunakan sertifikat resmi Kalacakra MOK.
* *First-Run Wizard* secara otomatis memandu pengguna melakukan pendaftaran MOK satu kali di layar UEFI, menjamin Secure Boot tetap aktif tanpa perlu mematikan proteksi BIOS.

### **7.3 Mandatory Access Control: SELinux in Enforcing Mode**
* SELinux berjalan aktif pada mode **`Enforcing`** secara default.
* Dilengkapi policy terintegrasi untuk subsistem container Podman dan Distrobox, memastikan proses yang terkompromi di dalam container tidak dapat menembus atau memanipulasi kernel host OS.

### **7.4 Physical Attack Defense: USBGuard with Screen-Locker Binding**
* Mengintegrasikan **USBGuard** untuk menangkal serangan fisik *BadUSB / Rubber Ducky* (injeksi keystroke perangkat jahat).
* **Screen-Lock Binding:** Ketika layar komputer terkunci (KDE Screen Locker aktif), seluruh port USB otomatis memblokir pendaftaran perangkat HID baru. Hanya perangkat terpercaya yang diizinkan beroperasi sampai pengguna memasukkan password.

### **7.5 Network & DNS Hardening: DNS-over-TLS (DoT) & Default-Deny Firewall**
* **DNS-over-TLS (DoT) Default:** `systemd-resolved` dikonfigurasi menggunakan DoT terenkripsi dengan resolver terpercaya (Quad9 / Cloudflare / AdGuard) untuk mencegah *DNS spoofing* dan pemantauan ISP di Wi-Fi publik.
* **Default-Deny Inbound Firewall:** `firewalld` aktif secara default; seluruh port masuk diblokir kecuali port esensial yang diizinkan (KDE Connect, WireGuard/Tailscale mesh).

### **7.6 Kernel Sysctl Hardening Toggles**
Konfigurasi pengerasan kernel bawaan pada `/etc/sysctl.d/99-kalacakra-security.conf`:
* `kernel.kptr_restrict = 2`: Menyembunyikan alamat pointer kernel untuk menggagalkan exploit memori.
* `kernel.dmesg_restrict = 1`: Membatasi pembacaan buffer log dmesg hanya untuk pengguna dengan hak istimewa.
* `kernel.unprivileged_bpf_disabled = 1`: Mencegah pengguna non-root mengeksekusi BPF sembarangan untuk mereduksi *attack surface*.
* `fs.protected_fifos = 2` & `fs.protected_regular = 2`: Mencegah eksploitasi file temp symlink/hardlink race condition.
* `net.ipv4.conf.all.rp_filter = 1`: Proteksi terhadap teknik IP spoofing jaringan.

### **7.7 Post-Quantum Cryptography (PQC-Ready Architecture)**
* Bersiap menghadapi ancaman komputasi kuantum (*Harvest Now, Decrypt Later*).
* Mengintegrasikan algoritma tahan kuantum standar NIST (**ML-KEM / Kyber** untuk key exchange dan **ML-DSA / Dilithium** untuk tanda tangan digital) pada stack OpenSSH, handshake Tailscale/WireGuard, dan enkripsi LUKS2.

### **7.8 MicroVM Zero-Trust App Sandboxing (Roadmap)**
* Menyiapkan ekosistem micro-hypervisor ringan (berbasis Firecracker / Cloud-Hypervisor) dengan boot-time <50ms.
* Menjalankan aplikasi berisiko tinggi (browser sesi mencurigakan, dokumen eksternal asing, script untrusted) di dalam MicroVM terisolasi perangkat keras, mencegah malware menyentuh host OS.

---

## **8. Roadmap Visi 10 Tahun (2026–2036): The Cognitive, Quantum-Resistant & Ubiquitous OS**

Kalacakra OS dirancang bukan sekadar untuk bertahan, melainkan untuk memimpin transformasi sistem operasi personal selama 1 dekade ke depan:

```
+---------------------------------------------------------------------------------+
|                       ROADMAP 10 TAHUN KALACAKRA OS                             |
+---------------------------------------------------------------------------------+
| 2026 - 2027: FASE 1 - MODERN APEX (PERFORMA, IMMUTABLE, & SECURITY)             |
| * Immutable OCI Core (bootc/ostree) + Dual-Tier Rollback Engine                 |
| * Native Dual Language (EN + ID) di seluruh UI, CLI, dan Voice AI Stack         |
| * Dynamic CPU Scheduler (sched-ext SCX) + NPU Driver Hardware Acceleration      |
| * Sigstore Cosign Verification, USBGuard, MOK Secure Boot, DoT Default          |
| * Ptyxis Container Terminal + Polonium Hybrid Auto-Tiling + k-interceptor       |
+---------------------------------------------------------------------------------+
| 2028 - 2030: FASE 2 - THE COGNITIVE OS (SEMANTIC KNOWLEDGE & AUTONOMOUS AGENTS) |
| * Local Semantic Vector Filesystem (k-semantic) menggantikan folder hierarkis   |
| * Autonomous Multi-Step Task Agent (k-agent) untuk automasi sistem operasi      |
| * MicroVM Zero-Trust Pods untuk isolasi aplikasi berisiko tinggi (<50ms boot)   |
| * Declarative Dotfiles & Workspace Git-State Sync                               |
+---------------------------------------------------------------------------------+
| 2031 - 2036: FASE 3 - QUANTUM-RESISTANT & UBIQUITOUS CONTINUUM                  |
| * Full Post-Quantum Cryptography (PQC) default di seluruh lapisan jaringan/disk |
| * Ubiquitous Cross-Device Spatial Continuum (Fluid Session Handoff antar layar) |
| * Eco-Compute Carbon-Aware Background Task Scheduling                           |
| * Dukungan Tier-1 untuk arsitektur CPU masa depan: ARM64 & RISC-V               |
+---------------------------------------------------------------------------------+
```

---

## **9. Identitas Visual & "The Rice" (Aesthetic & First Impression)**

Agar memiliki daya tarik viral di komunitas (Reddit `r/unixporn`, YouTube, X/Twitter):

* **Identitas Visual Kalacakra:**
  * Perpaduan estetika geometri kosmologis (Roda Waktu Nusantara) dengan sentuhan futuristik modern (*Dark Slate, Obsidian, dan Bronze/Copper Accent*).
  * Tema visual KDE Plasma 6 yang elegan, clean, modern blur, dan responsif terhadap dark/light mode.
* **Terminal Experience Kelas Dunia:**
  * **Shell Prompt:** Konfigurasi bawaan **Starship Prompt** menampilkan status branch Git, runtime aktif (Python/Node/Rust), dan indikator status Kalacakra Space.
  * **Fastfetch Kustom:** Tampilan ASCII art Kalacakra Mandala bergaya cyberpunk saat terminal dibuka, disertai rincian efisiensi kompresi Btrfs, status AI engine, active CPU scheduler (`scx`), dan deployment OCI aktif.
  * Utilitas CLI modern terpasang bawaan: `bat` (cat dengan syntax highlight), `eza` (modern ls), `fzf` (fuzzy search), dan `zoxide` (smart directory jump).
* **Kalacakra Welcome & First-Run Wizard:**
  * Wizard elegan yang menyapa pengguna saat boot pertama:
    1. **Pemilihan Bahasa Utama:** **[ English (US) ]** atau **[ Bahasa Indonesia ]**.
    2. Pemilihan privasi & status AI (Lokal NPU/CPU / Cloud / Nonaktif).
    3. Deteksi & pengaktifan driver GPU (Nvidia/Mesa) + MOK Secure Boot setup.
    4. Batas proteksi baterai (80% threshold switch).
    5. Pilihan aplikasi awal (Office, Browser pilihan, Gaming suite).
    6. Koneksi akun KDE Connect dan Tailscale.

---

## **10. Rencana Jalur Implementasi & Build Pipeline**

### **Fase 1: Pembuatan Base Image OCI (Multi-Target Containerfile)**

Membangun image berbasis Universal Blue (*kinoite-main* dan *kinoite-nvidia*):

```dockerfile
# Contoh Kerangka Containerfile Kalacakra OS
FROM ghcr.io/ublue-os/kinoite-main:latest

LABEL maintainer="Kalacakra OS Project"
LABEL description="Kalacakra OS - Rock-Solid Modern Immutable Desktop (Dual Language EN/ID)"

# 1. Pemasangan bahasa, utilitas dasar, container toolchain, security, & gaming
RUN rpm-ostree install \
    glibc-langpack-id \
    glibc-langpack-en \
    langpacks-id \
    langpacks-en \
    snapper \
    zram-generator \
    distrobox \
    podman \
    wireguard-tools \
    tailscale \
    firewalld \
    usbguard \
    gamemode \
    gamescope \
    mangohud \
    ptyxis \
    just \
    scx-scheds \
    plasma-vault \
    fastfetch \
    starship \
    bat \
    eza \
    fzf \
    zoxide && \
    rpm-ostree cleanup -m

# 2. Pemasangan biner Ollama & whisper.cpp secara langsung (Clean Binaries)
RUN curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.gz | tar -xz -C /usr/

# 3. Injeksi overlay konfigurasi sistem & script Kalacakra Core (SELinux, sysctl, scripts, locales)
COPY rootfs/ /

# 4. Pengaktifan system service penting
RUN systemctl enable zram-generator.service && \
    systemctl enable tailscaled.service && \
    systemctl enable firewalld.service && \
    systemctl enable usbguard.service
```

*Varian Nvidia:* Dibuat menggunakan build target terpisah `FROM ghcr.io/ublue-os/kinoite-nvidia:latest` dengan driver proprietary pre-compiled dan MOK signing key otomatis.

### **Fase 2: Pengembangan Tooling Khusus (Kalacakra Core Suite - Native i18n)**

Membangun utilitas inti dengan arsitektur i18n (menggunakan Rust / Go untuk performa instan dan konsumsi memori minim):

1. `kalacakra` (atau `k-just`): Central CLI & Recipe Runner berbasis *just* untuk automasi maintenance, rebase, battery cap, language switch, dan toggle sistem.
2. `k-interceptor`: Universal shell dispatcher dwibahasa yang mencegat perintah `apt`/`pacman` dan memandu pengguna ke metode instalasi yang tepat.
3. `k-ai`: Antarmuka CLI interaktif dwibahasa (EN/ID) dengan safety-gate Bash, secret redaction, dan auto-diagnostic stderr.
4. `k-semantic`: Local vector indexing daemon untuk pencarian file semantik (EN/ID).
5. `k-agent`: Sandboxed autonomous agent untuk otomasi tugas multi-langkah di OS.
6. `k-aur`: Wrapper integrasi Distrobox Arch untuk manajemen paket AUR dan ekspor shortcut desktop.
7. `k-doctor`: Skrip automasi diagnosa kesehatan dan verifikasi integritas sistem (laporan dwibahasa).
8. `k-rewind`: Time-travel file recovery dan snapshot browser berbasis Btrfs Snapper.
9. `k-beam`: AirDrop-like P2P local mesh file transfer tanpa internet.
10. `k-portal`: Wireless virtual second display engine untuk tablet dan ponsel via Wayland.
11. `k-ocr`: AI smart screenshot dengan OCR lokal offline dwibahasa (EN/ID).
12. `k-survival`: Ultra-battery emergency survival mode (layar monokrom, 40Hz, CPU cap 800MHz).
13. `k-precache`: Vulkan DXVK/VKD3D anti-stutter shader pre-compilation engine.

### **Fase 3: Media Installer ISO & Delivery Pipeline**

1. **Automasi Build ISO:**
   * Menggunakan **`bootc-image-builder`** di GitHub Actions CI/CD.
   * Container image yang selesai di-build diubah secara otomatis menjadi file ISO installer bootable dan image raw disk untuk bare-metal dengan installer Calamares dwibahasa.
2. **Kustomisasi Desktop & Skrip First-Run:**
   * Pemaketan tema KDE Plasma, instalasi skrip Polonium Auto-Tiling, konfigurasi shortcut global (`Super + Space`, `Super + V`, `Super + Y`), dan aplikasi wizard sambutan *Kalacakra Welcome* dwibahasa.
3. **Automated Testing & Security Scan:**
   * Scanning kerentanan container image via Trivy / Grype di GitHub Actions.
   * Pengujian boot otomatis via headless QEMU/KVM sebelum image dipublikasikan ke GitHub Container Registry (`ghcr.io`).

---

## **11. Format Prompt untuk AI Code Generation**

Saat Anda meminta AI untuk mulai mengeksekusi kode per modul, gunakan template prompt terstandarisasi berikut:

> *"Bertindaklah sebagai Senior Linux System Architect & Rust/Go Systems Engineer. Berdasarkan dokumen spesifikasi Kalacakra OS, buatkan implementasi lengkap untuk [Nama Modul, contoh: modul CLI k-interceptor menggunakan Rust dengan dukungan i18n EN/ID / Containerfile OCI bootc / konfigurasi Polonium auto-tiling / skrip recipe kalacakra CLI / policy SELinux / k-semantic daemon]. Pastikan kode memenuhi standar produksi, memiliki error handling yang tangguh, mendukung lokalisasi dwibahasa (English & Bahasa Indonesia), aman dijalankan di mode non-root, mematuhi prinsip privasi data, menerapkan pengerasan keamanan (security hardening), dan sepenuhnya kompatibel dengan arsitektur imutabel Btrfs."*