#!/usr/bin/env bash
# ==============================================================================
# Kalacakra OS - Local Build Helper
# Meniru .github/workflows/build-oci.yml (build image) & build-iso.yml (ISO)
# di mesin lokal, memakai podman (disarankan, cocok dgn CI) atau docker.
#
# Penggunaan:
#   scripts/build-local.sh check              # cek prasyarat (podman/docker, disk, RAM)
#   scripts/build-local.sh image [base|nvidia]# build image OCI lokal (default: base)
#   scripts/build-local.sh iso                # build ISO bootable via bootc-image-builder
#   scripts/build-local.sh all                # image base + nvidia
# ==============================================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# --- Deteksi engine container: utamakan podman (sesuai CI Universal Blue) ---
detect_engine() {
    if command -v podman >/dev/null 2>&1; then
        ENGINE="podman"
    elif command -v docker >/dev/null 2>&1; then
        ENGINE="docker"
        echo "[build-local] PERINGATAN: podman tidak ada, memakai docker."
        echo "[build-local] Containerfile memakai 'rpm-ostree install' yang bisa rewel"
        echo "[build-local] di docker. Jika build gagal, itu belum tentu bug Containerfile."
    else
        echo "[build-local Error] podman/docker tidak terpasang."
        echo "   Pasang podman: sudo apt install -y podman"
        exit 1
    fi
}

LOCAL_BASE="localhost/kalacakra-os:local"
LOCAL_NVIDIA="localhost/kalacakra-nvidia:local"

cmd_check() {
    detect_engine
    echo "[build-local] Engine          : $ENGINE ($($ENGINE --version | head -1))"
    echo "[build-local] Disk kosong /   : $(df -h / | awk 'NR==2{print $4}')"
    echo "[build-local] RAM             : $(free -h | awk '/^Mem:/{print $2}')"
    if [ "$(free -m | awk '/^Mem:/{print $2}')" -lt 3500 ]; then
        echo "[build-local] PERINGATAN: RAM < 3.5 GB, build image bisa lambat/gagal."
    fi
    if [ "$(df -m / | awk 'NR==2{print $4}')" -lt 12000 ]; then
        echo "[build-local] PERINGATAN: disk < 12 GB, ruang mungkin tidak cukup."
    fi
    echo "[build-local] Prasyarat OK."
}

cmd_image() {
    detect_engine
    local variant="${1:-base}"
    case "$variant" in
        base)   CF="Containerfile";        TAG="$LOCAL_BASE" ;;
        nvidia) CF="Containerfile.nvidia"; TAG="$LOCAL_NVIDIA" ;;
        *) echo "[build-local Error] varian tak dikenal: $variant (base|nvidia)"; exit 1 ;;
    esac
    echo "=== [build-local] Build image ($variant) dari $CF ==="
    echo "=== Tag: $TAG"
    "$ENGINE" build -f "$CF" -t "$TAG" .
    echo "=== [build-local] Selesai. Uji cepat:"
    echo "    $ENGINE run --rm $TAG /usr/bin/kalacakra --help"
}

cmd_iso() {
    detect_engine
    if [ "$ENGINE" != "podman" ]; then
        echo "[build-local Error] Build ISO butuh podman (bootc-image-builder pakai"
        echo "   storage khusus & butuh --privileged). Docker tidak didukung di sini."
        echo "   Pasang podman: sudo apt install -y podman"
        exit 1
    fi

    # bootc-image-builder butuh image SUMBER yang bisa di-pull/di-referensi.
    # Untuk build ISO lokal, kita pakai image lokal $LOCAL_BASE hasil 'image base'.
    local SRC_IMAGE="${1:-$LOCAL_BASE}"

    local CAP="quay.io/centos-bootc/bootc-image-builder:latest"
    echo "=== [build-local] Menyiapkan build ISO ==="
    echo "=== Image sumber : $SRC_IMAGE"
    echo "=== Perhatian    : langkah ini BUTUH sudo/root & --privileged."
    echo "===               Podman rootless tidak cukup untuk bootc-image-builder."

    mkdir -p output
    # Selaras dengan .github/workflows/build-iso.yml, tapi dengan storage root.
    sudo podman run \
        --rm \
        --privileged \
        --security-opt label=type:unconfined_t \
        -v ./output:/output \
        -v /var/lib/containers/storage:/var/lib/containers/storage \
        "$CAP" \
        --type iso \
        "$SRC_IMAGE"

    echo "=== [build-local] ISO selesai (jika tidak ada error di atas):"
    ls -lh output/bootiso/*.iso 2>/dev/null || echo "   (tidak ada .iso di output/bootiso/)"
}

cmd_all() {
    cmd_image base
    cmd_image nvidia
}

main() {
    local action="${1:-check}"
    shift || true
    case "$action" in
        check)  cmd_check ;;
        image)  cmd_image "$@" ;;
        iso)    cmd_iso "$@" ;;
        all)    cmd_all ;;
        *) echo "Penggunaan: $0 {check|image [base|nvidia]|iso|all}"; exit 1 ;;
    esac
}

main "$@"
