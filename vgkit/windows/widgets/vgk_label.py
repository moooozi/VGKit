import tkinter
from typing import Any

from .core_widget_classes import CTkBaseClass
from .font import CTkFont
from .theme import ThemeManager
from .utility import check_kwargs_empty, pop_from_dict_by_set


class VGkLabel(CTkBaseClass):
    """
    A simple label widget optimized for performance, supporting only basic features.
    No canvas, no images, no rounded corners. Supports scaling and dark mode.
    """

    # attributes that are passed to and managed by the tkinter label only:
    _valid_tk_label_attributes = {
        "cursor",
        "justify",
        "padx",
        "pady",
        "textvariable",
        "state",
        "takefocus",
        "underline",
    }

    def __init__(
        self,
        master: Any,
        width: int = 0,
        height: int = 28,
        bg_color: str | tuple[str, str] = "transparent",
        text_color: str | tuple[str, str] | None = None,
        text: str = "CTkSimpleLabel",
        font: tuple | CTkFont | None = None,
        anchor: str = "center",
        wraplength: int | str = "master",
        **kwargs,
    ):

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height)

        # color
        self._text_color = (
            ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color is None
            else self._check_color_type(text_color)
        )

        # text
        self._anchor = anchor
        self._text = text
        self._wraplength = wraplength

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # create tkinter.Label directly
        self._label = tkinter.Label(
            master=self,
            highlightthickness=0,
            padx=0,
            pady=0,
            borderwidth=0,
            anchor=self._anchor,
            text=self._text,
            font=self._apply_font_scaling(self._font),
            fg=self._apply_appearance_mode(self._text_color),
            bg=self._apply_appearance_mode(self._bg_color),
        )
        self._label.configure(**pop_from_dict_by_set(kwargs, self._valid_tk_label_attributes))

        check_kwargs_empty(kwargs, raise_error=True)

        self._label.pack(fill="both", expand=True)

        self._label.bind("<Configure>", self._update_wraplength)
        self._master_configure_id = tkinter.Frame.bind(
            self.master, "<Configure>", self._update_wraplength, add="+"
        )
        self._update_wraplength()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        self._label.configure(font=self._apply_font_scaling(self._font))
        self._update_wraplength()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self._label.configure(
            fg=self._apply_appearance_mode(self._text_color),
            bg=self._apply_appearance_mode(self._bg_color),
        )

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)
        # No need for canvas resize

    def _update_font(self):
        self._label.configure(font=self._apply_font_scaling(self._font))

    def _update_wraplength(self, event=None):
        if isinstance(self._wraplength, str):
            if self._wraplength == "self":
                width = self.winfo_width()
            elif self._wraplength == "master":
                width = self.master.winfo_width()
            else:
                raise ValueError(f"Invalid wraplength: {self._wraplength}")
            self._label.configure(wraplength=width)
        else:
            self._label.configure(wraplength=self._apply_widget_scaling(self._wraplength))

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)
        try:
            tkinter.Frame.unbind(self.master, "<Configure>", self._master_configure_id)
        except Exception:
            pass
        super().destroy()

    def configure(self, require_redraw=False, **kwargs):
        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            self._label.configure(fg=self._apply_appearance_mode(self._text_color))

        if "bg_color" in kwargs:
            # Update bg_color in base class
            super().configure(bg_color=kwargs.pop("bg_color"))
            self._label.configure(bg=self._apply_appearance_mode(self._bg_color))

        if "text" in kwargs:
            self._text = kwargs.pop("text")
            self._label.configure(text=self._text)

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)
            self._update_font()

        if "anchor" in kwargs:
            self._anchor = kwargs.pop("anchor")
            self._label.configure(anchor=self._anchor)

        if "wraplength" in kwargs:
            wl = kwargs.pop("wraplength")
            if isinstance(wl, str) and wl not in ("self", "master"):
                raise ValueError("wraplength must be 'self', 'master', or an integer")
            elif not isinstance(wl, (str, int)):
                raise ValueError("wraplength must be 'self', 'master', or an integer")
            self._wraplength = wl
            self._update_wraplength()

        self._label.configure(**pop_from_dict_by_set(kwargs, self._valid_tk_label_attributes))
        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> Any:
        if attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text":
            return self._text
        elif attribute_name == "font":
            return self._font
        elif attribute_name == "anchor":
            return self._anchor
        elif attribute_name == "wraplength":
            return self._wraplength
        elif attribute_name in self._valid_tk_label_attributes:
            return self._label.cget(attribute_name)
        else:
            return super().cget(attribute_name)

    def bind(self, sequence: str = None, command=None, add: str = True):
        if not (add == "+" or add is True):
            raise ValueError(
                "'add' argument can only be '+' or True to preserve internal callbacks"
            )
        self._label.bind(sequence, command, add=True)

    def unbind(self, sequence: str = None, funcid: str | None = None):
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None")
        self._label.unbind(sequence, None)

    def focus(self):
        return self._label.focus()

    def focus_set(self):
        return self._label.focus_set()

    def focus_force(self):
        return self._label.focus_force()
