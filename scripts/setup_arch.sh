#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ARCH_PACKAGES=(
  base-devel
  gcc
  cmake
  make
  python
  python-pip
  python-virtualenv
  cairo
  pango
  pkgconf
  harfbuzz
  fribidi
  ffmpeg
  sox
  git
  openssl
  mesa
)

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Este script está pensado para Arch Linux." >&2
  exit 1
fi

if command -v pacman >/dev/null 2>&1; then
  for pkg in "${ARCH_PACKAGES[@]}"; do
    if ! pacman -Q "$pkg" >/dev/null 2>&1; then
      echo "Instalando paquete faltante: $pkg"
      if command -v sudo >/dev/null 2>&1; then
        sudo pacman -S --needed --noconfirm "$pkg"
      else
        pacman -S --needed --noconfirm "$pkg"
      fi
    fi
  done
else
  echo "No se encontró pacman en este sistema." >&2
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creando entorno virtual .venv"
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [[ -f "cpp/Makefile" ]]; then
  echo "Compilando C++"
  make -C cpp
fi

echo "Setup de Arch completado."
