import threading
import tkinter
from collections.abc import Callable

import darkdetect


class AppearanceModeTracker:
    callback_list = []
    app_list = []

    appearance_mode_set_by = "system"
    appearance_mode = 0  # Light (standard)

    _listener_thread: threading.Thread = None
    _listener_started = False

    @classmethod
    def init_appearance_mode(cls):
        if cls.appearance_mode_set_by == "system":
            new_appearance_mode = cls.detect_appearance_mode()

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

    @classmethod
    def _start_listener(cls):
        """Start the darkdetect listener thread (once) to receive OS theme change callbacks."""
        if cls._listener_started:
            return
        cls._listener_started = True

        def _on_theme_change(theme_str: str):
            """Called from darkdetect listener thread when OS theme changes."""
            if cls.appearance_mode_set_by != "system":
                return

            new_mode = 1 if theme_str == "Dark" else 0
            if new_mode != cls.appearance_mode:
                cls.appearance_mode = new_mode
                cls._schedule_update_on_main_thread()

        cls._listener_thread = threading.Thread(
            target=darkdetect.listener,
            args=(_on_theme_change,),
            daemon=True,
        )
        cls._listener_thread.start()

    @classmethod
    def _schedule_update_on_main_thread(cls):
        """Use any available Tk root to schedule update_callbacks on the main thread."""
        for app in cls.app_list:
            try:
                app.after(0, cls.update_callbacks)
                return
            except Exception:
                continue

    @classmethod
    def add(cls, callback: Callable, widget=None):
        cls.callback_list.append(callback)

        if widget is not None:
            app = cls.get_tk_root_of_widget(widget)
            if app not in cls.app_list:
                cls.app_list.append(app)
            cls._start_listener()

    @classmethod
    def remove(cls, callback: Callable):
        try:
            cls.callback_list.remove(callback)
        except ValueError:
            return

    @staticmethod
    def detect_appearance_mode() -> int:
        try:
            if darkdetect.theme() == "Dark":
                return 1  # Dark
            else:
                return 0  # Light
        except NameError:
            return 0  # Light

    @classmethod
    def get_tk_root_of_widget(cls, widget):
        current_widget = widget

        while isinstance(current_widget, tkinter.Tk) is False:
            current_widget = current_widget.master

        return current_widget

    @classmethod
    def update_callbacks(cls):
        if cls.appearance_mode == 0:
            for callback in cls.callback_list:
                try:
                    callback("Light")
                except Exception:
                    continue

        elif cls.appearance_mode == 1:
            for callback in cls.callback_list:
                try:
                    callback("Dark")
                except Exception:
                    continue

    @classmethod
    def get_mode(cls) -> int:
        return cls.appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode_string: str):
        if mode_string.lower() == "dark":
            cls.appearance_mode_set_by = "user"
            new_appearance_mode = 1

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

        elif mode_string.lower() == "light":
            cls.appearance_mode_set_by = "user"
            new_appearance_mode = 0

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

        elif mode_string.lower() == "system":
            cls.appearance_mode_set_by = "system"
            new_appearance_mode = cls.detect_appearance_mode()
            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()
