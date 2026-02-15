__version__ = "0.1.0"

import os
import sys
from tkinter import Variable, StringVar, IntVar, DoubleVar, BooleanVar
from tkinter.constants import *
import tkinter.filedialog as filedialog

# import manager classes
from .windows.widgets.appearance_mode import AppearanceModeTracker
from .windows.widgets.font import FontManager
from .windows.widgets.scaling import ScalingTracker
from .windows.widgets.theme import ThemeManager
from .windows.widgets.core_rendering import DrawEngine

# import base widgets
from .windows.widgets.core_rendering import CTkCanvas
from .windows.widgets.core_widget_classes import CTkBaseClass

# import widgets with new names
from .windows.widgets import CTkButton
from .windows.widgets import VGkButton as Button
from .windows.widgets import CTkCheckBox as CheckBox
from .windows.widgets import CTkComboBox as ComboBox
from .windows.widgets import CTkEntry as Entry
from .windows.widgets import CTkFrame as Container
from .windows.widgets import VGkFrame as Frame
from .windows.widgets import VGkLabel as Label
from .windows.widgets import CTkOptionMenu as OptionMenu
from .windows.widgets import CTkProgressBar as ProgressBar
from .windows.widgets import CTkRadioButton as RadioButton
from .windows.widgets import CTkScrollbar as Scrollbar
from .windows.widgets import CTkSegmentedButton as SegmentedButton
from .windows.widgets import CTkSlider as Slider
from .windows.widgets import CTkSwitch as Switch
from .windows.widgets import CTkTabview as Tabview
from .windows.widgets import CTkTextbox as Textbox
from .windows.widgets import CTkScrollableFrame as ScrollableFrame
from .windows.widgets import TreeView

# import windows
from .windows import CTk as Window
from .windows import CTkToplevel as Toplevel
from .windows import CTkInputDialog as InputDialog

# import font classes
from .windows.widgets.font import CTkFont as Font

# import image classes
from .windows.widgets.image import CTkImage as Image

from .windows import ctk_tk


_ = (
    Variable,
    StringVar,
    IntVar,
    DoubleVar,
    BooleanVar,
    CENTER,
    filedialog,
)  # prevent IDE from removing unused imports

__all__ = [
    "Button",
    "CTkButton",
    "CheckBox",
    "ComboBox",
    "Entry",
    "Container",
    "Frame",
    "Label",
    "OptionMenu",
    "ProgressBar",
    "RadioButton",
    "Scrollbar",
    "SegmentedButton",
    "Slider",
    "Switch",
    "Tabview",
    "Textbox",
    "ScrollableFrame",
    "TreeView",
    "Window",
    "Toplevel",
    "InputDialog",
    "Font",
    "Image",
    "CTkCanvas",
    "CTkBaseClass",
    "set_appearance_mode",
    "get_appearance_mode",
    "set_default_color_theme",
    "set_widget_scaling",
    "set_window_scaling",
    "deactivate_automatic_dpi_awareness",
    "set_ctk_parent_class",
    "Variable",
    "StringVar",
    "IntVar",
    "DoubleVar",
    "BooleanVar",
    "CENTER",
    "filedialog",
]


def set_appearance_mode(mode_string: str):
    """possible values: light, dark, system"""
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode() -> str:
    """get current state of the appearance mode (light or dark)"""
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string: str):
    """set color theme or load custom theme file by passing the path"""
    ThemeManager.load_theme(color_string)


def set_widget_scaling(scaling_value: float):
    """set scaling for the widget dimensions"""
    ScalingTracker.set_widget_scaling(scaling_value)


def set_window_scaling(scaling_value: float):
    """set scaling for window dimensions"""
    ScalingTracker.set_window_scaling(scaling_value)


def deactivate_automatic_dpi_awareness():
    """deactivate DPI awareness of current process (windll.shcore.SetProcessDpiAwareness(0))"""
    ScalingTracker.deactivate_automatic_dpi_awareness = True


def set_ctk_parent_class(ctk_parent_class):
    ctk_tk.CTK_PARENT_CLASS = ctk_parent_class
