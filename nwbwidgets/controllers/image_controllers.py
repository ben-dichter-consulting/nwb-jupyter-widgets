"""Controllers specific to the inputs of the plotly.imshow function."""
import ipywidgets

from .basecontroller import BaseController


class RotationController(BaseController):
    """
    Controller specifically for tracking left/right rotation commands.

    The internal state attribute 'rotation' is an integer that tracks +1 for right and -1 for left on each button press.
    This can in turn be mapped in whatever way is needed by downstream data shaping.
    """

    def setup_attributes(self):
        self.rotate_left = ipywidgets.Button(icon="rotate-left", layout=ipywidgets.Layout(width="35px"))
        self.rotate_right = ipywidgets.Button(icon="rotate-right", layout=ipywidgets.Layout(width="35px"))

        self.rotation: int = 0  # A state value counter to keep relative track of rotation button presses

    def setup_children(self):
        self.children = (self.rotate_left, self.rotate_right)

    def _rotate_right(self, change):
        self.rotation += 1

    def _rotate_left(self, change):
        self.rotation -= 1

    def setup_observers(self):
        self.rotate_right.on_click(self._rotate_right)
        self.rotate_left.on_click(self._rotate_left)


class ImShowController(BaseController):
    """Controller specifically for handling various options for the plot.express.imshow function."""

    def setup_attributes(self):
        self.contrast_type_toggle = ipywidgets.ToggleButtons(
            description="Constrast: ",
            options=[
                ("Automatic", "Automatic"),
                ("Manual", "Manual"),
            ],  # Values set to strings for external readability
        )
        self.auto_contrast_method = ipywidgets.Dropdown(description="Method: ", options=["minmax", "infer"])
        self.manual_contrast_slider = ipywidgets.IntRangeSlider(
            value=(0, 1),  # Actual value will depend on data selection
            min=0,  # Actual value will depend on data selection
            max=1,  # Actual value will depend on data selection
            orientation="horizontal",
            description="Range: ",
            continuous_update=False,
        )

    def setup_children(self):
        self.children = (self.contrast_type_toggle, self.auto_contrast_method)

    def _switch_contrast_modes(self, enable_manual_contrast: bool):
        """When the manual contrast toggle is altered, adjust the manual vs. automatic visibility of the components."""
        if self.contrast_type_toggle.value == "Manual":
            self.children = (self.contrast_type_toggle, self.manual_contrast_slider)
        elif self.contrast_type_toggle.value == "Automatic":
            self.children = (self.contrast_type_toggle, self.auto_contrast_method)

    def setup_observers(self):
        self.contrast_type_toggle.observe(
            lambda change: self._switch_contrast_modes(enable_manual_contrast=change.new), names="value"
        )
