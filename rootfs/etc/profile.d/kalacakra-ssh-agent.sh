# Kalacakra OS - Unified SSH Agent Autostart
# Seamlessly starts and manages ssh-agent across terminal sessions

if [ -z "$SSH_AUTH_SOCK" ]; then
    SSH_ENV="$HOME/.ssh/agent-environment"
    if [ -f "$SSH_ENV" ]; then
        . "$SSH_ENV" > /dev/null
        ps -ef | grep "$SSH_AGENT_PID" | grep -v grep | grep ssh-agent > /dev/null || {
            eval "$(ssh-agent -s)" > /dev/null
            echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_ENV"
            echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_ENV"
        }
    else
        eval "$(ssh-agent -s)" > /dev/null
        mkdir -p "$HOME/.ssh"
        echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_ENV"
        echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_ENV"
    fi
fi
