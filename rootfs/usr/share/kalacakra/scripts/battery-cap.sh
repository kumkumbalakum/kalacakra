#!/usr/bin/env bash
# ==============================================================================
# Kalacakra OS - Battery Lifespan Preservation Script
# Sets charge threshold limit (e.g. 80%) across various laptop vendors
# ==============================================================================

set -euo pipefail

LIMIT="${1:-80}"

echo "[Kalacakra Battery Shield] Setting battery charge threshold to ${LIMIT}%..."

FOUND=0

# Standard Linux sysfs battery charge control limit
for bat in /sys/class/power_supply/BAT*; do
    if [ -f "$bat/charge_control_limit_max" ]; then
        echo "$LIMIT" | sudo tee "$bat/charge_control_limit_max" >/dev/null
        echo " -> Updated $bat/charge_control_limit_max to ${LIMIT}%"
        FOUND=1
    elif [ -f "$bat/charge_stop_threshold" ]; then
        echo "$LIMIT" | sudo tee "$bat/charge_stop_threshold" >/dev/null
        echo " -> Updated $bat/charge_stop_threshold to ${LIMIT}%"
        FOUND=1
    fi
done

# ASUS specific threshold
if [ -f "/sys/class/power_supply/BAT0/charge_control_end_threshold" ]; then
    echo "$LIMIT" | sudo tee "/sys/class/power_supply/BAT0/charge_control_end_threshold" >/dev/null
    echo " -> Updated ASUS charge_control_end_threshold to ${LIMIT}%"
    FOUND=1
fi

if [ "$FOUND" -eq 1 ]; then
    echo "[Kalacakra Battery Shield] Berhasil diaktifkan! / Successfully activated!"
else
    echo "[Kalacakra Battery Shield] Hardware battery threshold not exposed by this vendor kernel driver."
fi
