# ==============================================================================
# Kalacakra OS - Central System Recipes (Justfile)
# Declarative, reproducible system maintenance & quick action runner
# ==============================================================================

default:
    @just --list

# Perbarui seluruh sistem: host OCI, Flatpak, Homebrew, dan Spaces
update:
    @echo "=== [Kalacakra] Updating Host OS (Atomic bootc/rpm-ostree) ==="
    @rpm-ostree upgrade || true
    @echo "=== [Kalacakra] Updating Flatpak Apps ==="
    @flatpak update -y || true
    @if command -v brew >/dev/null 2>&1; then \
        echo "=== [Kalacakra] Updating Homebrew ==="; \
        brew update && brew upgrade; \
    fi
    @if command -v distrobox >/dev/null 2>&1; then \
        echo "=== [Kalacakra] Updating Distrobox Spaces ==="; \
        distrobox upgrade --all || true; \
    fi
    @echo "[Kalacakra] System update complete! Reboot jika ada update host OS."

# Bersihkan cache usang, snapshot lama, dan dangling container image
clean:
    @echo "=== [Kalacakra] Cleaning System Caches ==="
    @flatpak uninstall --unused -y || true
    @podman system prune -f || true
    @rpm-ostree cleanup -m || true
    @echo "[Kalacakra] System cleanup complete!"

# Pasang model AI lokal ke Ollama (default: llama3.2:1b)
install-model model="llama3.2:1b":
    @echo "=== [Kalacakra AI] Downloading model {{model}} ==="
    @ollama pull {{model}}

# Unduh model whisper.cpp untuk dikte suara offline (k-voice)
# Pakai: just install-whisper-model size=small   (tiny|base|small|medium)
install-whisper-model size="small":
    @echo "=== [Kalacakra Voice] Downloading whisper.cpp ggml-{{size}} model ==="
    @mkdir -p ~/.cache/whisper
    @if [ ! -f ~/.cache/whisper/ggml-{{size}}.bin ]; then \
        curl -fL --progress-bar \
          -o ~/.cache/whisper/ggml-{{size}}.bin \
          "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{{size}}.bin"; \
        echo "Model tersimpan di ~/.cache/whisper/ggml-{{size}}.bin"; \
    else \
        echo "Model sudah ada: ~/.cache/whisper/ggml-{{size}}.bin"; \
    fi

# Ganti penjadwal CPU dinamis (scx_lavd untuk gaming, scx_rusty untuk throughput)
scx scheduler="lavd":
    @echo "=== [Kalacakra SCX] Switching scheduler to scx_{{scheduler}} ==="
    @sudo systemctl stop scx.service 2>/dev/null || sudo pkill -f scx_ || true
    @if [ "{{scheduler}}" = "default" ]; then \
        echo "Scheduler reverted to default kernel EEVDF."; \
    else \
        sudo scx_{{scheduler}} & \
        echo "Active scheduler: scx_{{scheduler}}"; \
    fi

# Beralih varian driver tanpa install ulang (rebase nvidia / base)
rebase target="nvidia":
    @if [ "{{target}}" = "nvidia" ]; then \
        echo "Rebasing to Kalacakra OS Nvidia image..."; \
        rpm-ostree rebase ostree-unverified-registry:ghcr.io/kalacakra-os/kalacakra-nvidia:latest; \
    elif [ "{{target}}" = "base" ]; then \
        echo "Rebasing to Kalacakra OS Mesa base image..."; \
        rpm-ostree rebase ostree-unverified-registry:ghcr.io/kalacakra-os/kalacakra-base:latest; \
    else \
        echo "Target rebase tidak dikenal: {{target}}"; \
    fi

# Atur batas pengisian baterai laptop (default 80%)
battery-cap limit="80":
    @/usr/share/kalacakra/scripts/battery-cap.sh {{limit}}

# Jalankan diagnosa kesehatan sistem menyeluruh
doctor:
    @/usr/bin/k-doctor

# Beralih preferensi bahasa sistem (id / en)
lang code="id":
    @if [ "{{code}}" = "id" ]; then \
        echo "Mengalihkan bahasa ke Bahasa Indonesia (id_ID.UTF-8)..."; \
        sudo localectl set-locale LANG=id_ID.UTF-8; \
    elif [ "{{code}}" = "en" ]; then \
        echo "Switching system language to English (en_US.UTF-8)..."; \
        sudo localectl set-locale LANG=en_US.UTF-8; \
    else \
        echo "Kode bahasa tidak dikenal / Unknown language code: {{code}}"; \
    fi

# Kalacakra Rewind - Time-travel file recovery & snapshot browser
rewind action="list":
    @/usr/bin/k-rewind {{action}}

# Kalacakra Portal - Wireless second screen untuk tablet/ponsel
portal action="toggle":
    @/usr/bin/k-portal {{action}}

# Kalacakra Beam - P2P local mesh file transfer
beam action="receive":
    @/usr/bin/k-beam {{action}}

# Kalacakra OCR - AI Smart Screenshot with Local OCR
ocr:
    @/usr/bin/k-ocr

# Kalacakra Voice - Dikte suara offline via whisper.cpp (butuh model: just install-whisper-model)
voice +args="":
    @/usr/bin/k-voice {{args}}

# Kalacakra Game - Jalankan game/.exe Windows via Proton UMU (butuh umu-run/umu-launcher)
game +args:
    @/usr/bin/k-game {{args}}

# Kalacakra Survival - Mode darurat baterai laptop (layar monokrom, 40Hz, CPU cap)
survival action="toggle":
    @/usr/bin/k-survival {{action}}

# Kalacakra Precache - Vulkan DXVK anti-stutter shader pre-compiler
precache:
    @/usr/bin/k-precache run

# Kalacakra Quick Look - Pratinjau berkas instan (Spasi di Dolphin)
preview file="":
    @/usr/bin/k-preview {{file}}

# Kalacakra Spotlight - Kalkulator, konversi mata uang/satuan, & router AI
spotlight query="":
    @/usr/bin/k-spotlight {{query}}

# Kalacakra Flow - Universal Control kendali mouse & keyboard lintas laptop
flow action="server":
    @/usr/bin/k-flow {{action}}

# Kalacakra Snippet - Pengganti pintasan teks global (Text Replacement)
snippet action="list":
    @/usr/bin/k-snippet {{action}}

# Kalacakra Keyring - Zero-friction PAM auto-unlock, KWallet, & Touch ID
keyring action="status":
    @/usr/bin/k-keyring {{action}}

# Kalacakra Control Hub - Pusat Kendali Terpadu Ala YaST (TUI Dashboard)
hub action="":
    @/usr/bin/k-hub {{action}}

# Kalacakra QA - Validasi & Pengujian Regresi Otomatis Ala openQA
qa action="":
    @/usr/bin/k-qa {{action}}

# Kalacakra SnapBoot - Sinkronisasi & Integrasi Snapshot Snapper ke Menu Bootloader
snapboot action="list":
    @/usr/bin/k-snapboot {{action}}

# Kalacakra Profile - Pemasangan Paket Stack Kerja Lengkap Ala Zypper Patterns
profile action="list":
    @/usr/bin/k-profile {{action}}

# Kalacakra 1-Click - Pemasangan Paket & Skema Web 1-Klik Ala OBS
pkg target="":
    @/usr/bin/k-pkg {{target}}

# Kalacakra Jail - Sandbox Terisolasi Sekali Pakai Ala FreeBSD Jails
jail +args:
    @/usr/bin/k-jail {{args}}

# Kalacakra BE - Manajemen Kloning & Boot Environments Ala bectl
be action="list":
    @/usr/bin/k-be {{action}}

# Kalacakra Scrub - Pemeriksa Integritas & Deteksi Bitrot Btrfs Ala ZFS
scrub action="status":
    @/usr/bin/k-scrub {{action}}

# Kalacakra Trace - Profiling Kinerja Sistem & Bottleneck eBPF Ala DTrace
trace target="io":
    @/usr/bin/k-trace {{target}}

# Kalacakra sysrc - Pengubah Variabel Konfigurasi Sistem Aman & Atomik
sysrc assignment="":
    @/usr/bin/k-sysrc {{assignment}}

# Kalacakra Unveil - Pembatasan Path Filesystem & Namespace Ala OpenBSD unveil/pledge
unveil +args:
    @/usr/bin/k-unveil {{args}}

# Kalacakra Signify - Kriptografi Ed25519 Ringkas & Cepat Ala OpenBSD signify
signify action="status":
    @/usr/bin/k-signify {{action}}

# Kalacakra PF - Minimalist Desktop Packet Filter & Panic Killswitch Ala OpenBSD pf
pf action="status":
    @/usr/bin/k-pf {{action}}

# Kalacakra doas - Elevasi Hak Akses Minimalis & Aman Ala OpenBSD doas
doas action="status":
    @/usr/bin/k-doas {{action}}

# Kalacakra W^X - Auditor Mitigasi Eksploitasi Memori & Binary Ala OpenBSD W^X
wx action="check-kernel":
    @/usr/bin/k-wx {{action}}

# Kalacakra Look - Manajer identitas & tampilan desktop satu perintah (fitur ikonik)
look action="list" +args="":
    @/usr/bin/k-look {{action}} {{args}}

# Kalacakra Showcase - Tampilan identitas siap screenshot untuk r/unixporn
showcase +args="":
    @/usr/bin/k-showcase {{args}}

# Kalacakra Welcome - Wizard penyambutan boot pertama (bahasa, tema Look, AI)
welcome +args="":
    @/usr/bin/k-welcome {{args}}

# Kalacakra Ask - Tanya AI dari KRunner/Dolphin (wrapper k-ai)
ask +args="":
    @/usr/bin/k-ask {{args}}

# --- Build lokal (meniru CI GitHub Actions; butuh podman/docker) ---
# Cek prasyarat build (engine, disk, RAM)
build-check:
    @scripts/build-local.sh check

# Build image OCI lokal dari Containerfile (default: base)
build-image variant="base":
    @scripts/build-local.sh image {{variant}}

# Build ISO bootable via bootc-image-builder (butuh podman + sudo)
build-iso:
    @scripts/build-local.sh iso



