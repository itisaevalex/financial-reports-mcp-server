"""
Installation script for the Financial Reports MCP server in Claude Desktop.
"""

import subprocess
import os
import sys

def main():
    """Install the Financial Reports MCP server in Claude Desktop."""
    print("Installing Financial Reports MCP server in Claude Desktop...")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if fastmcp is in PATH
    try:
        # Try to find fastmcp executable
        subprocess.run(["fastmcp", "--version"], 
                      capture_output=True, 
                      check=True)
        has_fastmcp = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        has_fastmcp = False
        
    if has_fastmcp:
        # Use the fastmcp command if it's in PATH
        cmd = ["fastmcp", "install", "main.py", "--name", "Financial Reports API"]
    else:
        # If fastmcp is not in PATH, try to use Python module
        cmd = [sys.executable, "-m", "fastmcp", "install", "main.py", "--name", "Financial Reports API"]
    
    # Run the installation command
    try:
        subprocess.run(cmd, check=True, cwd=script_dir)
        print("Installation successful!")
        print("The 'Financial Reports API' MCP server is now available in Claude Desktop.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        print("\nAlternative installation method:")
        print("1. Open Claude Desktop")
        print("2. Click on the + button next to 'MCP Servers'")
        print("3. Select 'Add Server'")
        print(f"4. Navigate to: {os.path.join(script_dir, 'main.py')}")
        print("5. Click 'Open'")

if __name__ == "__main__":
    main()
