#!/bin/bash

echo "Installing Financial Reports MCP Server in Claude Desktop..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not found in your PATH."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Run the installation script
python3 install.py

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo ""
    echo "There was an error during installation."
    echo "Please check the messages above for more information."
else
    echo ""
    echo "Installation completed!"
fi

# Wait for user to press enter
read -p "Press Enter to exit..."
