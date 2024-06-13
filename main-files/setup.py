import sys
from cx_Freeze import setup, Executable

# The entry point of your application
main_script = "window.py"

# Additional modules that need to be included
includes = ["carplay_window", "mediaplayer", "reverse_window", "screens"]

# Additional files and folders to be included in the build
#include_files = [
    #("other_resources/resource1.txt", "resource1.txt"),
    #("other_resources/resource2.png", "resource2.png"),
    # Add more files or folders as needed
#]

# Base setup for GUI applications on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" for GUI applications, None for console applications

setup(
    name="MyApplication",
    version="0.1",
    description="My Application Description",
    options={
        "build_exe": {
            "packages": ["os", "sys", "kivy"],  # List of packages to include
            "includes": includes,
            #"include_files": include_files,
            "excludes": [],  # List of packages to exclude
            "optimize": 2,  # Optimization level (0, 1, 2)
        }
    },
    executables=[Executable(main_script, base=base)]
)
