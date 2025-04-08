import subprocess
import sys

def install_requirements():
    try:
        print("📦 Installing required packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Installation complete!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please try manually using:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    install_requirements()
