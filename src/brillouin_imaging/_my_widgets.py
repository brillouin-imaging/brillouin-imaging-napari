from magicgui.widgets import ComboBox

class CustomComboBox(ComboBox):
    """A custom ComboBox widget that sets the _default_choices attribute when setting the choices, to avoid a bug in visualization.

    This class extends the `ComboBox` widget from the `magicgui` library. 
    """

    def __init__(self, *args, **kwargs):
        """Initialize the CustomComboBox.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the parent ComboBox class.
        **kwargs : dict
            Keyword arguments to pass to the parent ComboBox class.
        """
        super().__init__(*args, **kwargs)

    @ComboBox.choices.setter
    def choices(self, choices):
        # keep _default_choices in sync so reset_choices() (fired on native_parent_changed) doesn't revert to the construction-time value
        ComboBox.choices.fset(self, choices)
        self._default_choices = choices