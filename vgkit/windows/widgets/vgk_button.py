import math
import sys
import tkinter
from collections.abc import Callable
from typing import Any

from .core_rendering import CTkCanvas, DrawEngine
from .core_widget_classes import CTkBaseClass
from .font import CTkFont
from .theme import ThemeManager
from .utility import check_kwargs_empty, pop_from_dict_by_set


class VGkButton(CTkBaseClass):
    """
    Lightweight button with two visual modes:

    - **simple** (default): No canvas or DrawEngine. A direct tkinter.Label styled
      with theme colours, hover feedback, and click handling.  Absolute minimum
      widget overhead.

    - **round**: Pill-shaped button drawn on a CTkCanvas with only 2 AA-circle
      font text items (left and right semicircles) plus 1 centre rectangle.
      Total: 3 shape items + 1 canvas text = 4 canvas items, compared with
      CTkButton's 10-20+.
    """

    _valid_tk_label_attributes = {
        "cursor",
        "justify",
        "padx",
        "pady",
        "takefocus",
        "underline",
    }

    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        mode: str = "simple",
        bg_color: str | tuple[str, str] = "transparent",
        fg_color: str | tuple[str, str] | None = None,
        hover_color: str | tuple[str, str] | None = None,
        text_color: str | tuple[str, str] | None = None,
        text_color_disabled: str | tuple[str, str] | None = None,
        text: str = "VGkButton",
        font: tuple | CTkFont | None = None,
        textvariable: tkinter.Variable | None = None,
        state: str = "normal",
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        anchor: str = "center",
        style: str = "primary",
        **kwargs,
    ):
        super().__init__(master=master, bg_color=bg_color, width=width, height=height)

        # ---- style ----
        self._style: str = style

        # ---- mode ----
        if mode not in ("simple", "round"):
            raise ValueError(f"mode must be 'simple' or 'round', got '{mode}'")
        self._mode: str = mode

        # ---- colours (shared CTkButton theme keys) ----
        theme_key = self._get_theme_key_for_style()
        self._fg_color = (
            ThemeManager.theme[theme_key]["fg_color"]
            if fg_color is None
            else self._check_color_type(fg_color, transparency=True)
        )
        self._hover_color = (
            ThemeManager.theme[theme_key]["hover_color"]
            if hover_color is None
            else self._check_color_type(hover_color)
        )
        self._text_color = (
            ThemeManager.theme[theme_key]["text_color"]
            if text_color is None
            else self._check_color_type(text_color)
        )
        self._text_color_disabled = (
            ThemeManager.theme[theme_key]["text_color_disabled"]
            if text_color_disabled is None
            else self._check_color_type(text_color_disabled)
        )

        # ---- text / font ----
        self._text = text
        self._textvariable: tkinter.Variable | None = textvariable
        self._font: tuple | CTkFont = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # ---- interaction ----
        self._state: str = state
        self._hover: bool = hover
        self._command: Callable | None = command
        self._anchor: str = anchor
        self._click_animation_running: bool = False

        # ---- build ----
        if self._mode == "simple":
            self._build_simple(kwargs)
        else:
            self._build_round(kwargs)

        self._set_cursor()
        self._draw()

    # ------------------------------------------------------------------
    #  Theme utilities
    # ------------------------------------------------------------------

    def _get_theme_key_for_style(self) -> str:
        """Get the theme key based on button style"""
        if self._style == "secondary":
            # Use CTkSecondaryButton theme if it exists, otherwise fallback to CTkButton
            if "CTkSecondaryButton" in ThemeManager.theme:
                return "CTkSecondaryButton"
        return "CTkButton"

    # ------------------------------------------------------------------
    #  Construction helpers
    # ------------------------------------------------------------------

    def _build_simple(self, extra_kwargs: dict):
        """No canvas — a single tkinter.Label acting as the button surface."""
        self._canvas = None
        self._label = tkinter.Label(
            master=self,
            highlightthickness=0,
            padx=0,
            pady=0,
            borderwidth=0,
            anchor=self._anchor,
            text=self._text,
            font=self._apply_font_scaling(self._font),
            textvariable=self._textvariable,
        )
        self._label.configure(**pop_from_dict_by_set(extra_kwargs, self._valid_tk_label_attributes))
        check_kwargs_empty(extra_kwargs, raise_error=True)
        # Use place instead of pack to respect the parent frame's fixed dimensions
        self._label.place(x=0, y=0, relwidth=1, relheight=1)

        self._label.bind("<Enter>", self._on_enter)
        self._label.bind("<Leave>", self._on_leave)
        self._label.bind("<Button-1>", self._clicked)

    def _build_round(self, extra_kwargs: dict):
        """CTkCanvas with DrawEngine managing pill-shaped button rendering."""
        check_kwargs_empty(extra_kwargs, raise_error=True)
        self._label = None

        self._canvas = CTkCanvas(
            master=self,
            highlightthickness=0,
            width=self._apply_widget_scaling(self._desired_width),
            height=self._apply_widget_scaling(self._desired_height),
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # DrawEngine handles shape rendering
        self._draw_engine = DrawEngine(self._canvas)
        self._draw_engine.set_round_to_even_numbers(True, True)

        # Text item id — created lazily in _draw_round
        self._text_id: int | None = None

        # textvariable trace for round mode (canvas text has no textvariable)
        self._textvariable_trace_id: str | None = None
        if self._textvariable is not None:
            self._textvariable_trace_id = self._textvariable.trace_add(
                "write", self._on_textvariable_write
            )

        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)
        self._canvas.bind("<Button-1>", self._clicked)

    # ------------------------------------------------------------------
    #  Drawing
    # ------------------------------------------------------------------

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        if self._mode == "simple":
            self._draw_simple(no_color_updates)
        else:
            self._draw_round(no_color_updates)

    def _draw_simple(self, no_color_updates: bool):
        if no_color_updates:
            return
        fg = self._resolve_fg_color()
        tc = self._resolve_text_color()
        self._label.configure(bg=fg, fg=tc)
        tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self._bg_color))

    def _draw_round(self, no_color_updates: bool):
        w = self._apply_widget_scaling(self._current_width)
        h = self._apply_widget_scaling(self._current_height)

        # DrawEngine creates a pill shape when corner_radius = height / 2
        # It handles even/odd dimension adjustments internally
        corner_radius = self._apply_widget_scaling(self._current_height / 2)

        # DrawEngine creates canvas items with "inner_parts" and "border_parts" tags
        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(
            w, h, corner_radius, border_width=0
        )

        # Apply the same dimension rounding that DrawEngine uses internally
        # to ensure text is centered on the actual drawn shape
        w_rounded = math.floor(w / 2) * 2
        h_rounded = math.floor(h / 2) * 2

        # --- text ---
        display_text = self._current_text()
        if self._text_id is None:
            self._text_id = self._canvas.create_text(
                0,
                0,
                text=display_text,
                font=self._apply_font_scaling(self._font),
                anchor=tkinter.CENTER,
                tags=("text_part",),
            )
            requires_recoloring = True

        # Update text position using rounded dimensions for perfect centering
        self._canvas.coords(self._text_id, w_rounded / 2, h_rounded / 2)
        self._canvas.itemconfigure(
            self._text_id,
            font=self._apply_font_scaling(self._font),
            text=display_text,
        )

        # --- colours ---
        if not no_color_updates or requires_recoloring:
            bg = self._apply_appearance_mode(self._bg_color)
            fg = self._resolve_fg_color()
            tc = self._resolve_text_color()

            self._canvas.configure(bg=bg)
            tkinter.Frame.configure(self, bg=bg)

            # Color the shape using DrawEngine's standard tags
            self._canvas.itemconfig("inner_parts", fill=fg, outline=fg)
            self._canvas.itemconfig("text_part", fill=tc)

        if requires_recoloring:
            self._canvas.tag_raise("text_part")

    # ------------------------------------------------------------------
    #  Colour helpers
    # ------------------------------------------------------------------

    def _resolve_fg_color(self) -> str:
        fg = self._apply_appearance_mode(self._fg_color)
        if fg == "transparent":
            fg = self._apply_appearance_mode(self._bg_color)
        return fg

    def _resolve_text_color(self) -> str:
        if self._state == tkinter.DISABLED:
            return self._apply_appearance_mode(self._text_color_disabled)
        return self._apply_appearance_mode(self._text_color)

    def _current_text(self) -> str:
        if self._textvariable is not None:
            return self._textvariable.get()
        return self._text

    # ------------------------------------------------------------------
    #  Scaling / Appearance callbacks
    # ------------------------------------------------------------------

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        if self._mode == "simple":
            self._label.configure(font=self._apply_font_scaling(self._font))
        elif self._canvas is not None:
            self._canvas.configure(
                width=self._apply_widget_scaling(self._desired_width),
                height=self._apply_widget_scaling(self._desired_height),
            )
        self._draw(no_color_updates=True)

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self._draw()

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)
        if self._mode == "round" and self._canvas is not None:
            self._canvas.configure(
                width=self._apply_widget_scaling(self._desired_width),
                height=self._apply_widget_scaling(self._desired_height),
            )
        self._draw()

    def _update_font(self):
        if self._mode == "simple":
            self._label.configure(font=self._apply_font_scaling(self._font))
        elif self._mode == "round" and self._text_id is not None:
            self._canvas.itemconfigure(self._text_id, font=self._apply_font_scaling(self._font))

    def _on_textvariable_write(self, *_args):
        """Trace callback — update canvas text when textvariable changes (round mode)."""
        if self._text_id is not None:
            self._canvas.itemconfigure(self._text_id, text=self._textvariable.get())

    # ------------------------------------------------------------------
    #  Cursor
    # ------------------------------------------------------------------

    def _set_cursor(self):
        if self._cursor_manipulation_enabled:
            if self._state == tkinter.DISABLED:
                if self._command is not None:
                    self.configure(cursor="arrow")
            elif self._state == tkinter.NORMAL:
                if self._command is not None:
                    if sys.platform == "darwin":
                        self.configure(cursor="pointinghand")
                    else:
                        self.configure(cursor="hand2")

    # ------------------------------------------------------------------
    #  Hover / Click
    # ------------------------------------------------------------------

    def _on_enter(self, event=None):
        if not self._hover or self._state != "normal":
            return
        color = self._apply_appearance_mode(
            self._hover_color if self._hover_color is not None else self._fg_color
        )
        if self._mode == "simple":
            self._label.configure(bg=color)
        elif self._canvas is not None:
            self._canvas.itemconfig("inner_parts", fill=color, outline=color)

    def _on_leave(self, event=None):
        self._click_animation_running = False
        fg = self._resolve_fg_color()
        if self._mode == "simple":
            self._label.configure(bg=fg)
        elif self._canvas is not None:
            self._canvas.itemconfig("inner_parts", fill=fg, outline=fg)

    def _click_animation(self):
        if self._click_animation_running:
            self._on_enter()

    def _clicked(self, event=None):
        if self._state == tkinter.DISABLED:
            return
        self._on_leave()
        self._click_animation_running = True
        self.after(100, self._click_animation)
        if self._command is not None:
            self._command()

    def invoke(self):
        """Call the command callback if the button is not disabled."""
        if self._state != tkinter.DISABLED and self._command is not None:
            return self._command()

    # ------------------------------------------------------------------
    #  configure / cget
    # ------------------------------------------------------------------

    def configure(self, require_redraw=False, **kwargs):
        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"), transparency=True)
            require_redraw = True

        if "hover_color" in kwargs:
            self._hover_color = self._check_color_type(kwargs.pop("hover_color"))

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True

        if "text_color_disabled" in kwargs:
            self._text_color_disabled = self._check_color_type(kwargs.pop("text_color_disabled"))
            require_redraw = True

        if "text" in kwargs:
            self._text = kwargs.pop("text")
            if self._mode == "simple":
                self._label.configure(text=self._text)
            else:
                require_redraw = True

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)
            self._update_font()

        if "textvariable" in kwargs:
            new_var = kwargs.pop("textvariable")
            # remove old trace (round mode)
            if (
                self._mode == "round"
                and self._textvariable is not None
                and self._textvariable_trace_id is not None
            ):
                self._textvariable.trace_remove("write", self._textvariable_trace_id)
                self._textvariable_trace_id = None
            self._textvariable = new_var
            if self._mode == "simple":
                self._label.configure(textvariable=self._textvariable)
            elif self._mode == "round" and self._textvariable is not None:
                self._textvariable_trace_id = self._textvariable.trace_add(
                    "write", self._on_textvariable_write
                )
                require_redraw = True

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "command" in kwargs:
            self._command = kwargs.pop("command")
            self._set_cursor()

        if "anchor" in kwargs:
            self._anchor = kwargs.pop("anchor")
            if self._mode == "simple":
                self._label.configure(anchor=self._anchor)
            else:
                require_redraw = True

        if self._mode == "simple":
            self._label.configure(**pop_from_dict_by_set(kwargs, self._valid_tk_label_attributes))

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> Any:
        if attribute_name == "mode":
            return self._mode
        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "hover_color":
            return self._hover_color
        elif attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text_color_disabled":
            return self._text_color_disabled
        elif attribute_name == "text":
            return self._text
        elif attribute_name == "font":
            return self._font
        elif attribute_name == "textvariable":
            return self._textvariable
        elif attribute_name == "state":
            return self._state
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "anchor":
            return self._anchor
        elif attribute_name in self._valid_tk_label_attributes and self._mode == "simple":
            return self._label.cget(attribute_name)
        else:
            return super().cget(attribute_name)

    # ------------------------------------------------------------------
    #  Cleanup
    # ------------------------------------------------------------------

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)
        if (
            self._mode == "round"
            and self._textvariable is not None
            and self._textvariable_trace_id is not None
        ):
            try:
                self._textvariable.trace_remove("write", self._textvariable_trace_id)
            except Exception:
                pass
        super().destroy()

    # ------------------------------------------------------------------
    #  Event delegation
    # ------------------------------------------------------------------

    def bind(self, sequence=None, command=None, add=True):
        if not (add == "+" or add is True):
            raise ValueError(
                "'add' argument can only be '+' or True to preserve internal callbacks"
            )
        if self._mode == "simple":
            self._label.bind(sequence, command, add=True)
        elif self._canvas is not None:
            self._canvas.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None")
        if self._mode == "simple":
            self._label.unbind(sequence, None)
        elif self._canvas is not None:
            self._canvas.unbind(sequence, None)

    def focus(self):
        if self._mode == "simple":
            return self._label.focus()
        elif self._canvas is not None:
            return self._canvas.focus_set()

    def focus_set(self):
        return self.focus()

    def focus_force(self):
        if self._mode == "simple":
            return self._label.focus_force()
        elif self._canvas is not None:
            return self._canvas.focus_force()
