#!/bin/bash

python -m pip install --upgrade pip 
python -m pip install --group dev

ln -sf $HOME/.host_zshrc $HOME/.zshrc && source $HOME/.zshrc