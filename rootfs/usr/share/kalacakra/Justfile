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
