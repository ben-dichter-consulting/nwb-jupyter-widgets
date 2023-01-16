"""A collection of frequently reused controllers for the ophys module."""
from typing import Optional, Dict, Union

import ipywidgets

from ..controllers import BaseController, MultiController, RotationController, ImShowController, ViewTypeController


class FrameController(BaseController):
    def setup_attributes(self):
        self.frame_slider = ipywidgets.IntSlider(
            value=0,  # Actual value will depend on data selection
            min=0,  # Actual value will depend on data selection
            max=1,  # Actual value will depend on data selection
            orientation="horizontal",
            description="Frame: ",
            continuous_update=False,
        )

    def setup_children(self):
        self.children = (self.frame_slider,)


class PlaneController(BaseController):
    def setup_attributes(self):
        self.plane_slider = ipywidgets.IntSlider(
            value=0,  # Actual value will depend on data selection
            min=0,  # Actual value will depend on data selection
            max=1,  # Actual value will depend on data selection
            orientation="horizontal",
            description="Plane: ",
            continuous_update=False,
        )

    def setup_children(self):
        self.children = (self.plane_slider,)


class SinglePlaneDataController(MultiController):
    def __init__(self, attributes: Optional[Dict[str, Union[BaseController, ipywidgets.Widget]]] = None):
        default_attributes = dict(rotation_controller=RotationController(), frame_controller=FrameController())
        if attributes is not None:
            default_attributes.update(attributes)
        super().__init__(attributes=default_attributes)

        # Align rotation buttons to center of sliders
        self.layout.align_items = "center"


class VolumetricDataController(SinglePlaneDataController):
    def __init__(self):
        super().__init__(attributes=dict(plane_controller=PlaneController()))


class BasePlaneSliceController(MultiController):
    def __init__(self, attributes: Optional[Dict[str, Union[BaseController, ipywidgets.Widget]]] = None):
        default_attributes = dict(view_type_controller=ViewTypeController(), imshow_controller=ImShowController())
        if attributes is not None:
            default_attributes.extend(attributes)
        super().__init__(attributes=default_attributes)

        self.setup_visibility()
        self.setup_observers()

    def set_detailed_visibility(self, visibile: bool):
        widget_visibility_type = "visible" if visibile else "hidden"

        self.contrast_type_toggle.layout.visibility = widget_visibility_type
        self.manual_contrast_slider.layout.visibility = widget_visibility_type
        self.auto_contrast_method.layout.visibility = widget_visibility_type

    def update_visibility(self):
        if self.view_type_toggle.value == "Simplified":
            self.set_detailed_visibility(visibile=False)
        elif self.view_type_toggle.value == "Detailed":
            self.set_detailed_visibility(visibile=True)

    def setup_visibility(self):
        self.set_detailed_visibility(visibile=False)

    def setup_observers(self):
        self.view_type_toggle.observe(lambda change: self.update_visibility(), names="value")


class SinglePlaneSliceController(BasePlaneSliceController):
    def __init__(self):
        super().__init__(attributes=dict(single_plane_data_controller=SinglePlaneDataController()))


class VolumetricPlaneSliceController(BasePlaneSliceController):
    def __init__(self):
        super().__init__(attributes=dict(volumetric_data_controller=VolumetricDataController()))
