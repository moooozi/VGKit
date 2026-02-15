import enum
import tkinter
import sys
from typing import Callable, Dict, List, Set
import ctypes
from ctypes import wintypes, WINFUNCTYPE, pythonapi, py_object
import threading


# Win32 subclass setup
comctl32 = ctypes.WinDLL("comctl32.dll")
comctl32.DefSubclassProc.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
comctl32.DefSubclassProc.restype = wintypes.LPARAM
comctl32.SetWindowSubclass.argtypes = [
    wintypes.HWND,
    ctypes.c_void_p,
    wintypes.UINT,
    wintypes.LPARAM,
]
comctl32.SetWindowSubclass.restype = wintypes.BOOL
comctl32.RemoveWindowSubclass.argtypes = [wintypes.HWND, ctypes.c_void_p, wintypes.UINT]
comctl32.RemoveWindowSubclass.restype = wintypes.BOOL

SUBCLASSPROC = WINFUNCTYPE(
    wintypes.LPARAM,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
    wintypes.UINT,
    wintypes.LPARAM,
)

# Thread-safe set for pending DPI changes (accessed from subclass proc without GIL)
_pending_dpi_changes_lock = threading.Lock()
_pending_dpi_changes: Set[int] = set()


def subclass_proc(hwnd, msg, wparam, lparam, uid, refdata):
    WM_DPICHANGED_AFTERPARENT = 0x02E3

    try:
        if msg == WM_DPICHANGED_AFTERPARENT:
            # Store hwnd value without calling Python code that needs GIL
            hwnd_val = int(hwnd) if isinstance(hwnd, int) else hwnd
            with _pending_dpi_changes_lock:
                _pending_dpi_changes.add(hwnd_val)
            return 0
        return comctl32.DefSubclassProc(hwnd, msg, wparam, lparam)
    except Exception:
        return comctl32.DefSubclassProc(hwnd, msg, wparam, lparam)


class DPIAware(enum.Enum):
    SYSTEM_AWARE = ctypes.wintypes.HANDLE(-2)
    PER_MONITOR_AWARE = ctypes.wintypes.HANDLE(-3)
    PER_MONITOR_AWARE_V2 = ctypes.wintypes.HANDLE(-4)


class DPIUnaware(enum.Enum):
    UNAWARE = ctypes.wintypes.HANDLE(-1)
    UNAWARE_GDISCALED = ctypes.wintypes.HANDLE(-5)


class ProcessDPIAwareness(enum.Enum):
    UNAWARE = 0
    SYSTEM_AWARE = 1
    PER_MONITOR_AWARE = 2


class DeviceCapsIndex(enum.Enum):
    HORZSIZE = 4
    VERTSIZE = 6
    HORZRES = 8
    VERTRES = 10
    ASPECTX = 40
    ASPECTY = 42
    ASPECTXY = 44
    LOGPIXELSX = 88
    LOGPIXELSY = 90


class ScalingTracker:
    deactivate_automatic_dpi_awareness = False

    window_widgets_dict: Dict[object, List[Callable]] = (
        {}
    )  # contains window objects as keys with list of widget callbacks as elements
    window_dpi_scaling_dict: Dict[object, float] = (
        {}
    )  # contains window objects as keys and corresponding scaling factors

    widget_scaling = 1.0  # user values which multiply to detected window scaling factor
    window_scaling = 1.0

    dpi_awareness_activated = False
    hwnd_to_window: Dict[int, object] = {}
    subclass_procs: Dict[int, object] = {}
    _dpi_poll_running = False

    @classmethod
    def get_widget_scaling(cls, widget) -> float:
        window_root = cls.get_window_root_of_widget(widget)
        return cls.window_dpi_scaling_dict[window_root] * cls.widget_scaling

    @classmethod
    def get_window_scaling(cls, window) -> float:
        window_root = cls.get_window_root_of_widget(window)
        return cls.window_dpi_scaling_dict[window_root] * cls.window_scaling

    @classmethod
    def set_widget_scaling(cls, widget_scaling_factor: float):
        cls.widget_scaling = max(widget_scaling_factor, 0.4)
        cls.update_scaling_callbacks_all()

    @classmethod
    def set_window_scaling(cls, window_scaling_factor: float):
        cls.window_scaling = max(window_scaling_factor, 0.4)
        cls.update_scaling_callbacks_all()

    @classmethod
    def get_window_root_of_widget(cls, widget):
        current_widget = widget

        while (
            isinstance(current_widget, tkinter.Tk) is False
            and isinstance(current_widget, tkinter.Toplevel) is False
        ):
            current_widget = current_widget.master

        return current_widget

    @classmethod
    def setup_dpi_hook(cls, window):
        """Register Win32 subclass to receive WM_DPICHANGED_AFTERPARENT."""
        if sys.platform.startswith("win"):
            try:
                hwnd = wintypes.HWND(window.winfo_id())
                hwnd_val = int(hwnd) if hasattr(hwnd, '__int__') else (hwnd.value if hasattr(hwnd, 'value') else hwnd)
                if hwnd_val not in cls.subclass_procs:
                    cls.hwnd_to_window[hwnd_val] = window
                    proc = SUBCLASSPROC(subclass_proc)
                    cls.subclass_procs[hwnd_val] = proc
                    comctl32.SetWindowSubclass(hwnd, proc, 1, 0)
                    # Start periodic poll if not already running
                    if not cls._dpi_poll_running:
                        cls._dpi_poll_running = True
                        window.after(50, cls._poll_dpi_changes)
            except Exception:
                pass

    @classmethod
    def update_scaling_callbacks_all(cls):
        for window, callback_list in cls.window_widgets_dict.items():
            for set_scaling_callback in callback_list:
                if not cls.deactivate_automatic_dpi_awareness:
                    set_scaling_callback(
                        cls.window_dpi_scaling_dict[window] * cls.widget_scaling,
                        cls.window_dpi_scaling_dict[window] * cls.window_scaling,
                    )
                else:
                    set_scaling_callback(cls.widget_scaling, cls.window_scaling)

    @classmethod
    def update_scaling_callbacks_for_window(cls, window):
        for set_scaling_callback in cls.window_widgets_dict[window]:
            if not cls.deactivate_automatic_dpi_awareness:
                set_scaling_callback(
                    cls.window_dpi_scaling_dict[window] * cls.widget_scaling,
                    cls.window_dpi_scaling_dict[window] * cls.window_scaling,
                )
            else:
                set_scaling_callback(cls.widget_scaling, cls.window_scaling)

    @classmethod
    def _poll_dpi_changes(cls):
        """Periodic poll to process DPI changes signaled by subclass proc. Runs on main thread with GIL."""
        global _pending_dpi_changes, _pending_dpi_changes_lock
        
        if not cls._dpi_poll_running:
            return
        
        # Get pending changes in a thread-safe way
        pending_hwnds = []
        with _pending_dpi_changes_lock:
            if _pending_dpi_changes:
                pending_hwnds = list(_pending_dpi_changes)
                _pending_dpi_changes.clear()
        
        # Process each pending DPI change
        for hwnd_val in pending_hwnds:
            window = cls.hwnd_to_window.get(hwnd_val)
            if window:
                try:
                    new_dpi = ctypes.windll.user32.GetDpiForWindow(wintypes.HWND(hwnd_val))
                    if new_dpi > 0:
                        new_scaling = new_dpi / 96.0
                        cls._apply_dpi_scaling(window, new_scaling)
                except Exception:
                    pass
        
        # Schedule next poll if we still have windows
        if cls.window_widgets_dict:
            # Get any window to schedule on
            any_window = next(iter(cls.window_widgets_dict.keys()))
            any_window.after(50, cls._poll_dpi_changes)
        else:
            cls._dpi_poll_running = False

    @classmethod
    def _apply_dpi_scaling(cls, window, new_scaling: float):
        """Apply new DPI scaling if it differs from the stored value."""
        stored_value = cls.window_dpi_scaling_dict.get(window)
        if stored_value is not None and abs(new_scaling - stored_value) > 0.01:
            cls.window_dpi_scaling_dict[window] = new_scaling
            if sys.platform.startswith("win"):
                window.attributes("-alpha", 0.15)
            window.block_update_dimensions_event()
            cls.update_scaling_callbacks_for_window(window)
            window.unblock_update_dimensions_event()
            if sys.platform.startswith("win"):
                window.attributes("-alpha", 1)

    @classmethod
    def add_widget(cls, widget_callback: Callable, widget):
        window_root = cls.get_window_root_of_widget(widget)

        if window_root not in cls.window_widgets_dict:
            cls.window_widgets_dict[window_root] = [widget_callback]
            cls.setup_dpi_hook(window_root)
        else:
            cls.window_widgets_dict[window_root].append(widget_callback)

        if window_root not in cls.window_dpi_scaling_dict:
            cls.window_dpi_scaling_dict[window_root] = cls.get_window_dpi_scaling(
                window_root
            )

    @classmethod
    def remove_widget(cls, widget_callback, widget):
        window_root = cls.get_window_root_of_widget(widget)
        try:
            cls.window_widgets_dict[window_root].remove(widget_callback)
        except Exception:
            pass

    @classmethod
    def remove_window(cls, window_callback, window):
        try:
            del cls.window_widgets_dict[window]
        except Exception:
            pass
        if sys.platform.startswith("win"):
            try:
                hwnd = wintypes.HWND(window.winfo_id())
                hwnd_val = int(hwnd) if hasattr(hwnd, '__int__') else (hwnd.value if hasattr(hwnd, 'value') else hwnd)
                if hwnd_val in cls.subclass_procs:
                    comctl32.RemoveWindowSubclass(hwnd, cls.subclass_procs[hwnd_val], 1)
                    del cls.subclass_procs[hwnd_val]
                    del cls.hwnd_to_window[hwnd_val]
            except Exception:
                pass

    @classmethod
    def add_window(cls, window_callback, window):
        if window not in cls.window_widgets_dict:
            cls.window_widgets_dict[window] = [window_callback]
        else:
            cls.window_widgets_dict[window].append(window_callback)

        if window not in cls.window_dpi_scaling_dict:
            cls.window_dpi_scaling_dict[window] = cls.get_window_dpi_scaling(window)
            cls.setup_dpi_hook(window)

    @classmethod
    def activate_high_dpi_awareness(cls):
        """make process DPI aware, vgkit elements will get scaled automatically,
        only gets activated when CTk object is created"""

        if not cls.dpi_awareness_activated:
            if not cls.deactivate_automatic_dpi_awareness:
                if sys.platform == "darwin":
                    pass  # high DPI scaling works automatically on macOS

                elif sys.platform.startswith("win"):
                    import ctypes

                    # Values for SetProcessDpiAwareness and SetProcessDpiAwarenessContext:
                    # internal enum PROCESS_DPI_AWARENESS
                    # {
                    #     Process_DPI_Unaware = 0,
                    #     Process_System_DPI_Aware = 1,
                    #     Process_Per_Monitor_DPI_Aware = 2
                    # }
                    #
                    # internal enum DPI_AWARENESS_CONTEXT
                    # {
                    #     DPI_AWARENESS_CONTEXT_UNAWARE = 16,
                    #     DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = 17,
                    #     DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE = 18,
                    #     DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = 34
                    # }

                    ctypes.windll.user32.SetProcessDpiAwarenessContext(
                        34
                    )  # Non client area scaling at runtime (titlebar)
                    # does not work with resizable(False, False), window starts growing on monitor with different scaling (weird tkinter bug...)
                    # Get the current foreground window handle for DPI scaling

                    # It's too bad, that these Windows API methods don't work properly with tkinter. But I tested days with multiple monitor setups,
                    # and I don't think there is anything left to do. So this is the best option at the moment:

                    ctypes.windll.shcore.SetProcessDpiAwareness(
                        2
                    )  # Titlebar does not scale at runtime
                else:
                    pass  # DPI awareness on Linux not implemented
            cls.dpi_awareness_activated = True

    @classmethod
    def get_window_dpi_scaling(cls, window) -> float:
        if not cls.deactivate_automatic_dpi_awareness:
            if sys.platform == "darwin":
                return 1  # scaling works automatically on macOS

            elif sys.platform.startswith("win"):
                from ctypes import windll, pointer, wintypes

                DPI100pc = 96  # DPI 96 is 100% scaling
                DPI_type = (
                    0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
                )
                window_hwnd = wintypes.HWND(window.winfo_id())
                monitor_handle = windll.user32.MonitorFromWindow(
                    window_hwnd, wintypes.DWORD(2)
                )  # MONITOR_DEFAULTTONEAREST = 2
                x_dpi, y_dpi = wintypes.UINT(), wintypes.UINT()
                windll.shcore.GetDpiForMonitor(
                    monitor_handle, DPI_type, pointer(x_dpi), pointer(y_dpi)
                )
                return (x_dpi.value + y_dpi.value) / (2 * DPI100pc)

            else:
                return 1  # DPI awareness on Linux not implemented
        else:
            return 1
