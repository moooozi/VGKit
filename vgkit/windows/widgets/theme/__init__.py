from .theme_manager import ThemeManager

# load default blue theme
try:
    ThemeManager.load_theme("blue")
except FileNotFoundError as err:
    raise FileNotFoundError(
        f"{err}\nThe .json theme file for vgkit could not be found.\n"
        + "If packaging with pyinstaller was used, have a look at the wiki:\n"
        + "https://github.com/moooozi/vgkit/wiki/Packaging#windows-pyinstaller-auto-py-to-exe"
    )
