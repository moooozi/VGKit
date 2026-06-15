import tkinter
from typing import Any

from .core_widget_classes import CTkBaseClass


class VGkFrame(CTkBaseClass):
    """
    A simple container widget optimized for performance by skipping canvas creation.
    Supports scaling and dark-light mode decorations.
    """

    def __init__(
        self,
        master: Any,
        width: int = 200,
        height: int = 200,
        bg_color: str | tuple[str, str] = "transparent",
        **kwargs,
    ):
        # Initialize as a simple frame without canvas
        super().__init__(master=master, width=width, height=height, bg_color=bg_color, **kwargs)

        # Set fg_color to transparent to avoid any drawing
        self._fg_color = "transparent"

    def cget(self, attribute_name: str) -> Any:
        if attribute_name == "fg_color":
            return self._fg_color
        return super().cget(attribute_name)

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if no_color_updates is False:
            tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self._bg_color))
