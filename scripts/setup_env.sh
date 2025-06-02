#!/bin/bash
set -e

echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
  echo "Error: Failed to create virtual environment. Make sure python3 and venv are installed."
  exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r configs/requirements.txt

echo ""
echo "✅ Setup complete!"
echo "To activate the environment, run:"
echo "    source venv/bin/activate"
