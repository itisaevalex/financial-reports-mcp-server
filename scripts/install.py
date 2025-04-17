"""
Modern installation script for the Financial Reports MCP server.
Sets up a Python virtual environment and installs dependencies.
"""

import subprocess
import os
import sys
import venv

def main():
    print("\n=============================================")
    print(" Financial Reports MCP - Python venv Setup  ")
    print("=============================================\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    venv_dir = os.path.join(project_dir, "venv")

    # Step 1: Create virtual environment
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment at {venv_dir} ...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"Virtual environment already exists at {venv_dir}.")

    # Step 2: Install requirements
    pip_exe = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    req_file = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(req_file):
        print("ERROR: requirements.txt not found!")
        sys.exit(1)

    print("Installing dependencies from requirements.txt ...")
    result = subprocess.run([pip_exe, "install", "-r", req_file])
    if result.returncode != 0:
        print("ERROR: Failed to install dependencies.")
        sys.exit(1)

    print("\nInstallation completed successfully!")
    print("\nTo activate the virtual environment:")
    if os.name == "nt":
        print(f"  {venv_dir}\\Scripts\\activate.bat")
    else:
        print(f"  source {venv_dir}/bin/activate")
    print("\nTo run the server:")
    print("  python -m src.financial_reports_mcp")
    print("\nYou can also use Docker for an isolated install: docker-compose up\n")

if __name__ == "__main__":
    main()
