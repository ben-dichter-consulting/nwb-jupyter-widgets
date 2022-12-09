import ipywidgets as widgets
import plotly.express as px

from .multicontroller import MultiController


class RotationController(widgets.HBox):
    controller_fields = ("rotation", "rotate_left", "rotate_right")

    def __init__(self):
        super().__init__()

        self.rotation = 0  # A hidden non-widget value counter to keep relative track of progression
        self.rotate_left = widgets.Button(icon="rotate-left", layout=widgets.Layout(width="35px"))
        self.rotate_right = widgets.Button(icon="rotate-right", layout=widgets.Layout(width="35px"))

        self.set_observers()

        self.children = (self.rotate_left, self.rotate_right)

    def set_observers(self):
        def _rotate_right(change):
            self.rotation += 1

        def _rotate_left(change):
            self.rotation -= 1

        self.rotate_right.on_click(_rotate_right)
        self.rotate_left.on_click(_rotate_left)


class ContrastTypeController(widgets.VBox):
    """Controller specifically for handling contrastt options for the plotly.express.imshow function."""

    controller_fields = ("contrast_type_toggle", "auto_contrast_method", "manual_contrast_slider")
    
    def __init__(self):
        super().__init__()

        self.contrast_type_toggle = widgets.ToggleButtons(
            description="Constrast: ",
            options=[
                ("Automatic", "Automatic"),
                ("Manual", "Manual"),
            ],  # Values set to strings for external readability
        )
        self.auto_contrast_method = widgets.Dropdown(description="Method: ", options=["minmax", "infer"])
        self.manual_contrast_slider = widgets.IntRangeSlider(
            value=(0, 1),  # Actual value will depend on data selection
            min=0,  # Actual value will depend on data selection
            max=1,  # Actual value will depend on data selection
            orientation="horizontal",
            description="Range: ",
            continuous_update=False,
        )

        # Setup initial controller-specific layout
        self.children = (self.contrast_type_toggle, self.auto_contrast_method)

        # Setup controller-specific observer events
        self.setup_observers()

    def setup_observers(self):
        self.contrast_type_toggle.observe(
            lambda change: self.switch_contrast_modes(enable_manual_contrast=change.new), names="value"
        )

    def switch_contrast_modes(self, enable_manual_contrast: str):
        """When the manual contrast toggle is altered, adjust the manual vs. automatic visibility of the components."""
        if self.contrast_type_toggle.value == "Manual":
            self.children = (self.contrast_type_toggle, self.manual_contrast_slider)
        elif self.contrast_type_toggle.value == "Automatic":
            self.children = (self.contrast_type_toggle, self.auto_contrast_method)


class ColorModeController(widgets.VBox):
    controller_fields = ("color_mode_dropdown", "supported_colors", "color_mode_reverse_toggle")
    
    def __init__(self):
        super().__init__()

        self.supported_colors = {name.capitalize(): name for name in px.colors.named_colorscales()}

        # Remap name of 'greys' and denote as default
        # Also setting up the name map and linking it to controller just in case we ever want to customize it more
        default_color = ("Grayscale (default)", "greys")
        self.supported_colors.pop(default_color[1].capitalize())
        self.supported_colors.update({default_color[0]: default_color[1]})

        self.color_mode_dropdown = widgets.Dropdown(
            description="Color Mode: ",
            options=[(k,v) for k,v in self.supported_colors.items()],
            value="greys",
            layout=dict(width="max-content")
        )
        self.color_mode_reverse_toggle = widgets.ToggleButtons(
            options=[
                ("Normal", "Normal"),
                ("Reversed", "Reversed"),
            ],  # Values set to strings for external readability
        )
        
        # Ran into problems with race conditions with setting up observers for this one
        # Mostly because simultaneous modifications of options/values of a dropdown
        
        self.children = (self.color_mode_dropdown, self.color_mode_reverse_toggle)


class ImShowController(MultiController):
    """Controller specifically for handling various options for the plotly.express.imshow function."""

    controller_fields = ("contrast_type_toggle", "auto_contrast_method", "manual_contrast_slider")

    def __init__(self):
        super().__init__(components=[ContrastTypeController(), ColorModeController()])
