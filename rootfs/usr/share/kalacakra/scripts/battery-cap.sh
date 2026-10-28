#!/usr/bin/env bash
# ==============================================================================
# Kalacakra OS - Battery Lifespan Preservation Script
# Sets charge threshold limit (e.g. 80%) across various laptop vendors.
# Jujur: hanya menulis ke sysfs yang benar-benar ada; bila driver vendor
# tidak mengekspos antarmuka, skrip melaporkan SKIP (tidak memalsukan sukses).
# ==============================================================================

set -u

LIMIT="${1:-80}"

# Validasi input numerik
case "$LIMIT" in
    ''|*[!0-9]*) echo "[k-battery] Error: limit harus angka 1-100."; exit 2 ;;
esac
if [ "$LIMIT" -lt 1 ] || [ "$LIMIT" -gt 100 ]; then
    echo "[k-battery] Error: limit harus 1-100."; exit 2
fi

echo "[Kalacakra Battery Shield] Setting battery charge threshold to ${LIMIT}%..."

FOUND=0

write_sysfs() {
    # $1 = path, $2 = value
    if [ -w "$1" ] 2>/dev/null || [ -f "$1" ]; then
        if echo "$2" | sudo tee "$1" >/dev/null 2>&1; then
            echo " -> Updated $1 to $2"
            FOUND=1
            return 0
        fi
    fi
    return 1
}

# Standard Linux sysfs battery charge control
for bat in /sys/class/power_supply/BAT*; do
    [ -e "$bat" ] || continue
    if [ -f "$bat/charge_control_limit_max" ]; then
        write_sysfs "$bat/charge_control_limit_max" "$LIMIT" || true
    fi
    if [ -f "$bat/charge_stop_threshold" ]; then
        write_sysfs "$bat/charge_stop_threshold" "$LIMIT" || true
    fi
    if [ -f "$bat/charge_control_end_threshold" ]; then
        write_sysfs "$bat/charge_control_end_threshold" "$LIMIT" || true
    fi
done

# ASUS (charge_control_end_threshold sudah ditangani di atas; tambahan start threshold)
for f in /sys/class/power_supply/BAT*/charge_control_start_threshold; do
    [ -f "$f" ] && write_sysfs "$f" "$((LIMIT - 5 < 1 ? 1 : LIMIT - 5))" || true
done

# Lenovo IdeaPad conservation mode (0/1, bukan persentase)
for f in /sys/bus/platform/drivers/ideapad_acpi/*/conservation_mode \
         /sys/bus/platform/drivers/ideapad_laptop/*/conservation_mode; do
    [ -f "$f" ] || continue
    if [ "$LIMIT" -le 80 ]; then
        write_sysfs "$f" "1" || true
    else
        write_sysfs "$f" "0" || true
    fi
done

# Lenovo ThinkPad charge thresholds (tp_smapi / thinkpad_acpi)
for f in /sys/devices/platform/smapi/BAT0/stop_charge_thresh \
         /sys/devices/platform/smapi/BAT1/stop_charge_thresh; do
    [ -f "$f" ] && write_sysfs "$f" "$LIMIT" || true
done

# Framework / generic charge limit via cros_ec (best-effort)
for f in /sys/class/power_supply/BAT*/charge_limit; do
    [ -f "$f" ] && write_sysfs "$f" "$LIMIT" || true
done

if [ "$FOUND" -eq 1 ]; then
    echo "[Kalacakra Battery Shield] Berhasil diaktifkan! / Successfully activated!"
else
    echo "[Kalacakra Battery Shield] Hardware battery threshold not exposed by this vendor kernel driver."
    echo "   Untuk ASUS/Lenovo/ThinkPad, pastikan modul kernel vendor (asus-wmi, ideapad_laptop, thinkpad_acpi) aktif."
fi
