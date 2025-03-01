import os
import sys
import subprocess

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"


def run_command(command):
    """Helper function to run shell commands"""
    subprocess.run(command, shell=True, check=True)


def create_virtualenv():
    """Create a virtual environment if it does not exist"""
    if not os.path.exists(VENV_DIR):
        print("🔹 Creating virtual environment with access to system packages...")
        run_command(f"{sys.executable} -m venv {VENV_DIR} --system-site-packages")
    else:
        print("✅ Virtual environment already exists.")


def install_dependencies():
    """Install dependencies from requirements.txt if it exists"""
    print("🔹 Installing dependencies...")
    python_exec = os.path.join(VENV_DIR, "bin", "python")
    run_command(f"{python_exec} -m pip install --upgrade pip")
    if os.path.exists(REQUIREMENTS_FILE):
        run_command(f"{python_exec} -m pip install -r {REQUIREMENTS_FILE}")
    else:
        print(f"⚠️ {REQUIREMENTS_FILE} not found. Skipping dependency installation.")


def set_alias():
    """Add alias for ros_launch_tree"""
    print("🔹 Setting up alias...")
    activate_file = os.path.join(VENV_DIR, "bin", "activate")
    main_script = os.path.abspath("main.py")
    alias_command = f"alias ros_launch_tree='python3 {main_script} $1'"

    with open(activate_file, "r") as f:
        content = f.read()

    if alias_command in content:
        print("✅ Alias for ros_launch_tree already set, skipping modification.")
    else:
        with open(activate_file, "a") as f:
            f.write(f"{alias_command}\n")
        print(f"✅ Alias added: ros_launch_tree -> python3 {main_script} $1")


def main():
    """Main setup function"""
    create_virtualenv()
    install_dependencies()
    set_alias()
    print("\n🎉 Setup complete! To activate the virtual environment, run:")
    print("   source venv/bin/activate")


if __name__ == "__main__":
    main()
