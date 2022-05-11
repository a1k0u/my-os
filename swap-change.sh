#!/bin/bash

new_swap_size="$1"
correct_input=$(echo "$new_swap_size" | grep -E -o "^[0-9]+[\.]?[0-9]*[BKMGTP]+")

if [ -z "$new_swap_size" ] || [ ${#correct_input} -ne ${#new_swap_size} ]; then
  echo "[LOG] Empty or wrong input, exit..."
  exit
fi

echo "[LOG] Before update swap file had $(swapon --show \
                                        | grep -E -o "[0-9]+[BKMGTP]" \
                                        | head -n 1)..."

echo "[LOG] Stop swap file..."
sudo swapoff -a /swapfile

echo "[LOG] Delete previous swap file..."
sudo rm /swapfile

echo "[LOG] Create new swap file with swap_size=$new_swap_size..."
sudo fallocate -l "$new_swap_size" /swapfile

echo "[LOG] Marked new swap file..."
sudo mkswap /swapfile
sudo chmod 600 /swapfile

echo "[LOG] Enable new file..."
sudo swapon /swapfile

echo "[LOG] Updated swap file has $(swapon --show \
                                  | grep -E -o "[0-9]+[BKMGTP]" \
                                  | head -n 1)..."
