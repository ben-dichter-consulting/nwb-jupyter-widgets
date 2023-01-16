"""
Base class definition of all controllers.

Attempted to make the class abstract via `abc.ABC` to use `abc.abstractmethod` but ran into metaclass conflict
issues with `ipywidgets.Box`. Undefined methods instead raise NotImplementedErrors.
"""
from typing import Dict, Optional, Any

import ipywidgets


class BaseController(widgets.Box):
    """
    Base definition of all Controllers.

    A Controller is a container of objects such as widgets, including other controllers, that exposes all important
    components as non-private attributes at the outermost level for simplified reference.

    This is in constrast to defining an ipywidget.Box of other Boxes, where the only way to reference a particular
    sub-widget component is by navigating the children tree, knowing the set of levels and indices required to find
    a particular child.
    """

    def _check_attribute_name_collision(self, name: str):
        """Enforce string name references to sub-widget or sub-controller objects to be unique."""
        if hasattr(self, name):
            raise KeyError(
                f"This Controller already has an outer attribute with the name '{name}'! "
                "Please adjust the reference key to be unique."
            )

    def __init__(
        self, components: Optional[Dict[str, ipywidgets.Widget]] = None, states: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize this controller given the pre-initialized set of components.

        To align the children vertically, set the `layout.flex_flow = "column"` after initializing.

        Parameters
        ----------
        components: dictionary of ipywidgets.Widget objects
            The key/values pairs of this dictionary are set as attribute names and values to this class.
            This is to allow outer exposure for convenient access to the sub-widgets of this controller.
        states: dictionary
            The key/values pairs of this dictionary are set as attribute names and values to this class.
            This is to allow the definition of intermediate state trackers that may interact with multiple components.
        """
        super().__init__()  # Setup Box properties
        self.layout.display = "flex"
        self.layout.align_items = "stretch"

        self.setup_components(components=components)
        self.setup_states(states=states)
        self.setup_children()
        self.setup_observers()

    def setup_components(self, components: Optional[Dict[str, ipywidgets.Widget]] = None):
        """Define how to set the components given a dictionary of string mappings to arbitrary object types."""
        components = components or dict()
        for component_name, component in components.items():
            if isinstance(component, ipywidgets.Widget):
                self._check_attribute_name_collision(name=component_name)
                setattr(self, component_name, component)
            elif isinstance(component, BaseController):
                raise ValueError(
                    f"Component '{component_name}' is a type of Controller! "
                    "Please use a MultiController to unpack its components."
                )
            else:
                raise ValueError(
                    f"Component '{component_name}' is of type '{type(component)}'! "
                    "Please only set ipywidgets.Widget objects as 'components'. Set all other types as 'states'."
                )
        # Maintain sub-component structure for provenance; mostly for the MultiController sub-structures
        self.components = components

    def setup_children(self):
        """Define how to set the children using the internal components."""
        raise NotImplementedError("This Controller has not defined how to layout its children!")

    def setup_observers(self):
        """
        Define observation events specific to the interactions and values of components within the same Controller.
        """
        # Instead of raising NotImplementedError or being an abstractmethod,
        # a given widget may not need or want to use any local observers.
        pass

    def get_fields(self) -> Dict[str, object]:
        """
        Return the custom attributes set at the outer level for this Controller.

        Slightly more proper and better-looking than directly accessing the magic __dict__ attribute.

        Returns
        -------
        fields: dict
            The non-private attributes of this controller exposed at the outer-most level.
            These can be widgets, other controllers, or even mutable references.
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and k != "components" and k != "states"}
