import ipywidgets as widgets

from .genericcontroller import GenericController


class RotationController(GenericController):
    controller_fields = ("rotation", "rotate_left", "rotate_right")

    def setup_components(self):
        components = dict(
            rotation=0,  # A hidden non-widget value counter to keep relative track of progression
            rotate_left=widgets.Button(icon="rotate-left", layout=widgets.Layout(width="35px")),
            rotate_right=widgets.Button(icon="rotate-right", layout=widgets.Layout(width="35px")),
        )

        super().setup_components(components=components)

    def _rotate_right(self, change):
        self.rotation += 1

    def _rotate_left(self, change):
        self.rotation -= 1

    def set_observers(self):
        self.rotate_right.on_click(self._rotate_right)
        self.rotate_left.on_click(self._rotate_left)


class ImShowController(GenericController):
    """Controller specifically for handling various options for the plot.express.imshow function."""

    def setup_components(self):
        components = dict(
            contrast_type_toggle=widgets.ToggleButtons(
                description="Constrast: ",
                options=[
                    ("Automatic", "Automatic"),
                    ("Manual", "Manual"),
                ],  # Values set to strings for external readability
            ),
            auto_contrast_method=widgets.Dropdown(description="Method: ", options=["minmax", "infer"]),
            manual_contrast_slider=widgets.IntRangeSlider(
                value=(0, 1),  # Actual value will depend on data selection
                min=0,  # Actual value will depend on data selection
                max=1,  # Actual value will depend on data selection
                orientation="horizontal",
                description="Range: ",
                continuous_update=False,
            ),
        )

        super().setup_components(components=components)

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
            lambda change: self.switch_contrast_modes(enable_manual_contrast=change.new), names="value"
        )
