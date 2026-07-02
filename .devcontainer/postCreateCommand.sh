#!/bin/bash

set -euo pipefail

python -m pip install --upgrade pip
python -m pip install --group dev

if [[ -f /host/.zshrc ]]; then
  ln -sf /host/.zshrc "$HOME/.zshrc"
fi
