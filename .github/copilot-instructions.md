# VGKit Copilot Instructions

## Architecture Overview
VGKit is a CustomTkinter fork focused on lightweight widgets, TreeView implementation, and improved DPI/scaling control. Key components:
- **Widgets**: Located in `vgkit.windows.widgets/` with shared subpackages (core_rendering, font, scaling, theme, utility)
- **Rendering**: `DrawEngine` handles cross-platform drawing (polygon_shapes on macOS, font_shapes elsewhere)
- **State Management**: `AppearanceModeTracker`, `ScalingTracker`, `ThemeManager` centralize theme/scaling state
- **API Export**: `vgkit/__init__.py` re-exports widgets with simplified names (e.g., `CTkButton` → `Button`)

## Naming Conventions
- **New VGKit widgets**: `vgk_` file prefix, `VGk` class prefix (e.g., `vgk_label.py`, `VGkLabel`)
- **Original CTk widgets**: `ctk_` prefix, `CTk` class prefix
- **Re-exports**: Both types exported with simple names; `CTkLabel` unused, replaced by `VGkLabel` as `Label`
- **Frames**: `CTkFrame` (complex borders/geometry) exported as `Container`; `VGkFrame` (simple) as `Frame`

## API Usage Patterns
```python
import vgkit as vgk

vgk.set_appearance_mode("dark")  # "Light", "Dark", "System"
vgk.set_default_color_theme("blue")  # "blue", "green", "dark-blue" or path to .json

app = vgk.Window()
button = vgk.Button(app, text="Click")
label = vgk.Label(app, text="Hello")
app.mainloop()
```

## Widget Development Workflow
1. Implement widget in `vgkit/windows/widgets/` (e.g., `vgk_newwidget.py` with `VGkNewWidget` class)
2. Add import/export in `vgkit/windows/widgets/__init__.py`
3. Add re-export in `vgkit/__init__.py` with simple name and `__all__`
4. Follow `DrawEngine` flow for rendering; inherit from `CTkBaseClass`

## Testing Patterns
- **Unit tests**: In `test/unit_tests/`, GUI-based tests that run in `mainloop()`
- **Run tests**: Instantiate test class and call `.main()` (e.g., `TestCTkButton().main()`)
- **Manual tests**: `test/manual_integration_tests/` for live UI validation
- Tests use `root.after()` to schedule test steps sequentially

## Build & Release Workflow
- **Dependencies**: Listed in `requirements.txt` and `setup.cfg`
- **Versioning**: Update `__version__` in `vgkit/__init__.py`, then run `tbump` (configured in `pyproject.toml`)
- **Packaging**: Uses setuptools; includes all subpackages in `setup.cfg`

## Theme & Assets
- **Themes**: JSON files in `vgkit/assets/themes/` with light/dark color arrays
- **Fonts**: Roboto in `vgkit/assets/fonts/`
- **Loading**: `ThemeManager.load_theme()` accepts theme name or file path

## Scaling & DPI
- **Automatic**: Enabled by default on Windows 8.1+; can be deactivated via `vgk.deactivate_automatic_dpi_awareness()`
- **Manual**: `vgk.set_widget_scaling()`, `vgk.set_window_scaling()`
- Handled centrally by `ScalingTracker`

## Key Files for Reference
- `vgkit/__init__.py`: Public API surface and re-exports
- `examples/simple_example.py`: Basic usage demonstration
- `vgkit/windows/widgets/core_rendering/draw_engine.py`: Core rendering logic
- `test/unit_tests/test_all.py`: Consolidated test runner</content>
<parameter name="filePath">d:\Repos\VGKit\.github\copilot-instructions.md