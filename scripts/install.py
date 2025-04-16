"""
Installation script for the Financial Reports MCP server in Claude Desktop.
"""

import subprocess
import os
import sys
import shutil
import platform

def main():
    """Install the Financial Reports MCP server in Claude Desktop."""
    print("Installing Financial Reports MCP server in Claude Desktop...")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if fastmcp is installed as a command
    fastmcp_cmd = shutil.which("fastmcp")
    
    if fastmcp_cmd:
        # Use the fastmcp command if it's in PATH
        cmd = [fastmcp_cmd, "install", "main.py", "--name", "Financial Reports API"]
    else:
        print("The 'fastmcp' command was not found in your PATH.")
        print("Attempting to install using Python module...")
        
        # Try using pip to check if fastmcp is installed
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "fastmcp"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # fastmcp is installed as a Python package
                # On Windows, we need to find the Scripts directory
                if platform.system() == "Windows":
                    python_path = os.path.dirname(sys.executable)
                    scripts_path = os.path.join(python_path, "Scripts")
                    fastmcp_path = os.path.join(scripts_path, "fastmcp.exe")
                    
                    if os.path.exists(fastmcp_path):
                        cmd = [fastmcp_path, "install", "main.py", "--name", "Financial Reports API"]
                    else:
                        show_manual_instructions(script_dir)
                        return
                else:
                    # On Unix-like systems, try to find fastmcp in the bin directory
                    bin_dir = os.path.join(os.path.dirname(sys.executable), "bin")
                    fastmcp_path = os.path.join(bin_dir, "fastmcp")
                    
                    if os.path.exists(fastmcp_path):
                        cmd = [fastmcp_path, "install", "main.py", "--name", "Financial Reports API"]
                    else:
                        show_manual_instructions(script_dir)
                        return
            else:
                print("The 'fastmcp' package is not installed.")
                print(f"Please install it with: {sys.executable} -m pip install fastmcp")
                show_manual_instructions(script_dir)
                return
        except Exception as e:
            print(f"Error checking fastmcp installation: {e}")
            show_manual_instructions(script_dir)
            return
    
    # Run the installation command
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, cwd=script_dir)
        print("\nInstallation successful!")
        print("The 'Financial Reports API' MCP server is now available in Claude Desktop.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        show_manual_instructions(script_dir)
    except Exception as e:
        print(f"Unexpected error: {e}")
        show_manual_instructions(script_dir)

def show_manual_instructions(script_dir):
    """Show manual installation instructions."""
    print("\nAlternative installation method:")
    print("1. Open Claude Desktop")
    print("2. Click on the + button next to 'MCP Servers'")
    print("3. Select 'Add Server'")
    print(f"4. Navigate to: {os.path.join(script_dir, 'main.py')}")
    print("5. Click 'Open'")

if __name__ == "__main__":
    main()
