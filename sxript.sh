#!/bin/bash

# آدرس مخزن و فایل پایتون در GitHub
REPO_URL="Fhttps://raw.githubusercontent.com/hosseinpv1379/tunnel/main/tun.py"
PYTHON_FILE="tun.py"

# بررسی وجود پایتون 3
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found, please install Python 3"
    exit 1
fi

# دانلود فایل پایتون از GitHub
echo "Downloading Python script from GitHub..."
curl -L -o $PYTHON_FILE $REPO_URL

# بررسی موفقیت دانلود
if [ ! -f "$PYTHON_FILE" ]; then
    echo "Failed to download the Python script."
    exit 1
fi

# اجرای اسکریپت پایتون
echo "Running the Python script..."
sudo python3 $PYTHON_FILE
