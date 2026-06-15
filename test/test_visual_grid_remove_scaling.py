import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import vgkit as vgk


def test_visual_grid_remove_scaling():
    # Create root window
    root = vgk.Window()
    root.title("Grid Remove Scaling Test")
    root.geometry("500x400")

    # Status label
    status_label = vgk.Label(root, text="Status: Label is visible", font=("Arial", 14))
    status_label.grid(row=0, column=0, pady=10)

    # Test label
    test_label = vgk.Label(
        root,
        text="Test Label - I should disappear and stay hidden!",
        fg_color="blue",
        text_color="white",
    )
    test_label.grid(row=1, column=0, pady=20)

    def update_status():
        if test_label.winfo_ismapped():
            status_label.configure(text="Status: Label is visible")
        else:
            status_label.configure(text="Status: Label is hidden")

    def grid_remove_label():
        test_label.grid_remove()
        root.update()
        update_status()

    def change_scaling():
        current = vgk.get_widget_scaling()
        new_scaling = 1.5 if current == 1.0 else 1.0
        vgk.set_widget_scaling(new_scaling)
        scaling_button.configure(text=f"Change Scaling (current: {new_scaling})")
        root.update()
        update_status()

    def regrid_label():
        test_label.grid(row=1, column=0, pady=20)  # Re-grid it
        root.update()
        update_status()

    # Buttons
    remove_button = vgk.Button(root, text="Grid Remove Label", command=grid_remove_label)
    remove_button.grid(row=2, column=0, pady=10)

    scaling_button = vgk.Button(root, text="Change Scaling (current: 1.0)", command=change_scaling)
    scaling_button.grid(row=3, column=0, pady=10)

    regrid_button = vgk.Button(root, text="Re-grid Label", command=regrid_label)
    regrid_button.grid(row=4, column=0, pady=10)

    # Instructions
    instructions = vgk.Label(
        root,
        text="Instructions:\n1. Click 'Grid Remove Label' - label should disappear\n2. Click 'Change Scaling' - label should stay hidden\n3. Click 'Re-grid Label' - label should reappear",
        justify="left",
    )
    instructions.grid(row=5, column=0, pady=20)

    # Initial status
    update_status()

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    test_visual_grid_remove_scaling()
