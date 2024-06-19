from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "pymediainfo", "tkinter", "re"],
    "includes": [],
    "include_files": ["resources/"],
    "excludes": [
        "tkinter.test", "tkinter.tix", "unittest", "pydoc", "email",
        "http", "logging", "test", "distutils", "multiprocessing", "http.client", "profile",
        "turtle", "turtledemo", "unicodedata"
    ]
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="gerador-de-codigos",
    version="2.0.2",
    description="Gerador de codigos Making Off",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="resources/icon.ico")],
)
