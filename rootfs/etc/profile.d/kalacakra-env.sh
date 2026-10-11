# ==============================================================================
# Kalacakra OS - Default Environment Profile
# Sets up Homebrew path, Starship prompt, modern aliases, and Command Interceptor
# ==============================================================================

# 1. Integrasi Homebrew on Linux (/home/linuxbrew)
if [ -d "/home/linuxbrew/.linuxbrew/bin" ]; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv 2>/dev/null)"
fi

# 2. Modern CLI coreutils aliases (fallback to standard if missing)
if command -v eza >/dev/null 2>&1; then
    alias ls='eza --icons --group-directories-first'
    alias ll='eza -la --icons --group-directories-first'
    alias lt='eza --tree --level=2 --icons'
fi

if command -v bat >/dev/null 2>&1; then
    alias cat='bat --paging=never'
fi

# 3. Universal Command Interceptor shell hooks
# Mencegat perintah instalasi berbasis apt / pacman pada host OS imutabel
apt() {
    /usr/bin/k-interceptor apt "$@"
}

apt-get() {
    /usr/bin/k-interceptor apt "$@"
}

pacman() {
    /usr/bin/k-interceptor pacman "$@"
}

yay() {
    /usr/bin/k-interceptor yay "$@"
}

# 4. Fastfetch greeting on interactive shell
if [[ $- == *i* ]] && command -v fastfetch >/dev/null 2>&1 && [ -z "$KALACAKRA_FETCH_DONE" ]; then
    export KALACAKRA_FETCH_DONE=1
    if [ -f "/usr/share/kalacakra/fastfetch/config.jsonc" ]; then
        fastfetch --config /usr/share/kalacakra/fastfetch/config.jsonc
    else
        fastfetch
    fi
fi
