# Kalacakra OS - Unified SSH Agent Autostart
# Seamlessly starts and manages ssh-agent across terminal sessions

if [ -z "$SSH_AUTH_SOCK" ]; then
    SSH_ENV="$HOME/.ssh/agent-environment"
    if [ -f "$SSH_ENV" ] && [ -S "$(sed -n 's/^export SSH_AUTH_SOCK=//p' "$SSH_ENV" 2>/dev/null)" ]; then
        . "$SSH_ENV" > /dev/null
        # Hanya cek proses jika PID benar-benar terisi
        if [ -n "$SSH_AGENT_PID" ]; then
            ps -p "$SSH_AGENT_PID" -o comm= 2>/dev/null | grep -q ssh-agent || {
                eval "$(ssh-agent -s)" > /dev/null
                echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_ENV"
                echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_ENV"
            }
        fi
    else
        eval "$(ssh-agent -s)" > /dev/null
        mkdir -p "$HOME/.ssh"
        echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_ENV"
        echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_ENV"
    fi
fi
