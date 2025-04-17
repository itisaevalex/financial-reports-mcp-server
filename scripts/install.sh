#!/bin/bash

set -e

clear

echo "============================================="
echo " Financial Reports MCP - Modern Installer   "
echo "============================================="
echo

echo "Choose installation method:"
echo "  1. Docker (recommended, easiest)"
echo "  2. Python Virtual Environment (venv)"
echo
read -p "Enter 1 or 2 and press Enter: " install_choice

if [[ "$install_choice" == "1" ]]; then
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not found in your PATH."
        echo "Please install Docker or choose Python venv."
        read -p "Press Enter to exit..."
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null; then
        echo "Error: docker-compose is not found in your PATH."
        echo "Please install docker-compose or choose Python venv."
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "Building Docker image..."
    docker-compose build
    if [ $? -ne 0 ]; then
        echo "Docker build failed."
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "To run the server: docker-compose up"
    read -p "Press Enter to exit..."
    exit 0
elif [[ "$install_choice" == "2" ]]; then
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not found in your PATH."
        read -p "Press Enter to exit..."
        exit 1
    fi
    python3 install.py
    if [ $? -ne 0 ]; then
        echo "There was an error during Python venv installation."
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "Installation completed!"
    read -p "Press Enter to exit..."
    exit 0
else
    echo "Invalid choice. Exiting."
    read -p "Press Enter to exit..."
    exit 1
fi
