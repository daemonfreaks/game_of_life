FROM python:3.14

# Install zsh, vim, and lv
RUN apt update -y && apt install -y --no-install-recommends zsh vim lv && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN (type -p wget >/dev/null || (apt update -y && apt install -y wget)) \
    && mkdir -p -m 755 /etc/apt/keyrings \
    && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    && cat $out | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && mkdir -p -m 755 /etc/apt/sources.list.d \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update -y \
    && apt install gh -y

# Install npm and Codex
RUN apt update -y && apt install -y --no-install-recommends npm && rm -rf /var/lib/apt/lists/*
RUN npm install -g @openai/codex
