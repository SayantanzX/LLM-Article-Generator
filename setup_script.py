#!/usr/bin/env python3
"""
Setup script for LLM Article Generator
Run this script to set up the project environment
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def create_directory_structure():
    """Create necessary directories."""
    directories = [
        "models",
        "data",
        "logs",
        "exports"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def main():
    """Main setup function."""
    print("🚀 LLM Article Generator Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directory structure
    create_directory_structure()
    
    # Install/upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️  Warning: Could not upgrade pip")
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing required packages"):
        print("❌ Failed to install requirements. Please install manually.")
        sys.exit(1)
    
    # Check GPU availability
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🎮 GPU detected: {torch.cuda.get_device_name()}")
            print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            print("💻 Running on CPU (GPU not available)")
    except ImportError:
        print("⚠️  PyTorch not installed properly")
    
    # Create run script
    create_run_script()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\nTo run the application:")
    print("  • Windows: run.bat")
    print("  • Linux/Mac: ./run.sh")
    print("  • Manual: streamlit run app.py")
    print("\n📝 Note: First model loading will take time and require internet connection")

def create_run_script():
    """Create platform-specific run scripts."""
    
    # Windows batch file
    with open("run.bat", "w") as f:
        f.write("""@echo off
echo Starting LLM Article Generator...
echo.
echo Open your browser to: http://localhost:8501
echo.
streamlit run app.py
pause
""")
    
    # Unix shell script
    with open("run.sh", "w") as f:
        f.write("""#!/bin/bash
echo "Starting LLM Article Generator..."
echo ""
echo "Open your browser to: http://localhost:8501"
echo ""
streamlit run app.py
""")
    
    # Make shell script executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run.sh", 0o755)
    
    print("📜 Created run scripts (run.bat for Windows, run.sh for Unix)")

if __name__ == "__main__":
    main()