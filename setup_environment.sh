#!/bin/bash

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "Setting up/updating virtual environment..."
if [[ ! -d "${THIS_DIR}/venv" ]]; then
  python3 -m venv "${THIS_DIR}"/venv
  source "${THIS_DIR}"/venv/bin/activate
  pip3 install --upgrade pip wheel
  pip3 install -r "${THIS_DIR}"/requirements.txt
else
  source "${THIS_DIR}"/venv/bin/activate
  pip3 install --upgrade pip --quiet
  pip3 install -r "${THIS_DIR}"/requirements.txt --quiet
fi

echo "Downloading/synchronizing BMRB data..."
rsync -ahv --prune-empty-dirs --include='*/' --include "bmr*_3.str" --exclude="*" rsync://rsync.bmrb.io:/macromolecules/ bmrb_entries