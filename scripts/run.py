#!/usr/bin/env python3
"""
Universal runner for NotebookLM skill scripts
Handles virtual environment setup and script execution
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def setup_console_utf8():
    """
    Set console to UTF-8 mode on Windows.
    This configures both the current process and subprocesses.
    """
    if os.name != 'nt':
        return

    try:
        import ctypes
        import io

        # Set console code page to UTF-8 (CP 65001)
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)

        # Reconfigure stdout/stderr to use UTF-8
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding='utf-8', errors='replace'
            )
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding='utf-8', errors='replace'
            )

        # Set environment variable for subprocesses
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    except Exception:
        pass


class SkillEnvironment:
    """Manages skill-specific virtual environment"""

    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.venv_dir = self.skill_dir / ".venv"
        self.requirements_file = self.skill_dir / "requirements.txt"

        if os.name == 'nt':
            self.venv_python = self.venv_dir / "Scripts" / "python.exe"
            self.venv_pip = self.venv_dir / "Scripts" / "pip.exe"
        else:
            self.venv_python = self.venv_dir / "bin" / "python"
            self.venv_pip = self.venv_dir / "bin" / "pip"

    def ensure_venv(self) -> bool:
        """Ensure virtual environment exists and is set up"""
        if self.venv_dir.exists():
            return True

        print("🔧 First-time setup: Creating virtual environment...")
        print("   This may take a minute...")

        # Create venv
        print(f"🔧 Creating virtual environment in {self.venv_dir.name}/")
        try:
            venv.create(self.venv_dir, with_pip=True)
            print("✅ Virtual environment created")
        except Exception as e:
            print(f"❌ Failed to create venv: {e}")
            return False

        # Install dependencies
        if self.requirements_file.exists():
            print("📦 Installing dependencies...")
            try:
                subprocess.run(
                    [str(self.venv_pip), "install", "--upgrade", "pip"],
                    check=True, capture_output=True, text=True,
                    encoding='utf-8', errors='replace'
                )

                subprocess.run(
                    [str(self.venv_pip), "install", "-r", str(self.requirements_file)],
                    check=True, capture_output=True, text=True,
                    encoding='utf-8', errors='replace'
                )
                print("✅ Dependencies installed")

                # Install Chrome for Patchright
                print("🌐 Installing Google Chrome for Patchright...")
                try:
                    subprocess.run(
                        [str(self.venv_python), "-m", "patchright", "install", "chrome"],
                        check=True, capture_output=True, text=True,
                        encoding='utf-8', errors='replace'
                    )
                    print("✅ Chrome installed")
                except subprocess.CalledProcessError:
                    print("⚠️ Chrome install failed. Run manually: python -m patchright install chrome")

            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False

        print("\n✅ Environment ready!")
        print(f"   Virtual env: {self.venv_dir}")
        print(f"   Python: {self.venv_python}")
        return True


def main():
    """Main runner"""
    setup_console_utf8()

    if len(sys.argv) < 2:
        print("Usage: python run.py <script_name> [args...]")
        print("\nAvailable scripts:")
        print("  ask_question.py     - Query NotebookLM")
        print("  notebook_manager.py - Manage notebook library")
        print("  auth_manager.py     - Handle authentication")
        print("  cleanup_manager.py  - Clean up skill data")
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    # Handle "scripts/script.py" format
    if script_name.startswith('scripts/'):
        script_name = script_name[8:]

    if not script_name.endswith('.py'):
        script_name += '.py'

    # Get paths
    env = SkillEnvironment()
    script_path = env.skill_dir / "scripts" / script_name

    if not script_path.exists():
        print(f"❌ Script not found: {script_name}")
        sys.exit(1)

    # Ensure venv exists
    if not env.ensure_venv():
        print("❌ Failed to set up environment")
        sys.exit(1)

    # Run the script
    cmd = [str(env.venv_python), str(script_path)] + script_args
    # Environment variables (PYTHONIOENCODING already set by setup_console_utf8)
    env_vars = os.environ.copy()
    try:
        result = subprocess.run(cmd, env=env_vars)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()