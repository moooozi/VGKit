
![PyPI](https://img.shields.io/pypi/v/vgkit)



# VGKit
VGKit is a fork of [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky. It has simpler and performance oriented widgets, Treeview implementation and improved DPI change handling.

*Note: This is a fork tailored to my specific needs. It's not well documented or maintained for everyone else.*

## Installation

Iinstall from source with [uv](https://docs.astral.sh/uv/):
```bash
git clone https://github.com/moooozi/vgkit.git
cd vgkit
uv sync
uv run python examples/complex_example.py
```

**Update existing installation:** `pip install vgkit --upgrade`

## Development

```bash
uv sync --group dev    # install package + dev tools
uv run ruff check .    # lint
uv run ruff format .   # format
uv build               # build wheel + sdist
```

## Usage
```python
import vgkit as vgk

# Create a window
app = vgk.Window()

# Add widgets
button = vgk.Button(app, text="Click me!")
label = vgk.Label(app, text="Hello, VGKit!")

# Run the app
app.mainloop()
```
