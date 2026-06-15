import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import vgkit as vgk


def test_grid_remove_scaling():
    # Create root window
    root = vgk.Window()
    root.geometry("400x300")

    # Create a label
    label = vgk.Label(root, text="Test Label")
    label.grid(row=0, column=0, padx=20, pady=20)
    root.update()  # Update to make it mapped

    # Check that it's mapped
    assert label.winfo_ismapped(), "Label should be mapped initially"

    # Remove it
    label.grid_remove()
    root.update()

    # Check that it's not mapped
    assert not label.winfo_ismapped(), "Label should not be mapped after grid_remove"

    # Change scaling
    vgk.set_widget_scaling(1.5)
    root.update()

    # Check that it's still not mapped
    assert not label.winfo_ismapped(), "Label should still not be mapped after scaling change"

    # Re-grid it
    label.grid(row=0, column=0, padx=20, pady=20)
    root.update()

    # Check that it's mapped again
    assert label.winfo_ismapped(), "Label should be mapped after re-gridding"

    print("Test passed!")


if __name__ == "__main__":
    test_grid_remove_scaling()
