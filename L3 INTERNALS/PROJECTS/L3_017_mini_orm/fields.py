#-------------------------------------------------------------------------
# Object-Relational Mapping Fields
#-------------------------------------------------------------------------

class L3_017Field:
    """Descriptor representing a database field."""

    def __init__(self, field_type: type, required: bool = True) -> None:

        # fields needs to remember the expected type therefore we store field_type and required
        self.field_type = field_type
        self.required = required

    def __set_name__(self, owner, name: str) -> None:   # --> __set_name__ will give us "name", "age"
        """Store the attribute name."""

        self.name = name   # --> therefore we need a place to store self.name

    def __get__(self, instance, owner):
        """Return stored value."""

        if instance is None:
            return self         # --> no instance exists (accessing from the class), return the descriptor itself

        return instance.__dict__.get(self.name)  # --> return the stored value from the instance

    def __set__(self, instance, value) -> None:
        """Validate and store value."""

        # Handle required fields.
        if value is None and self.required: # if field is required and someone gives None raise error.
            raise ValueError("Field value cannot be None")

        # Validate the value type.
        if not isinstance(value, self.field_type):  # if the field value does not match the field type raise error and mention it
            raise TypeError("Field value must be of type %s" % self.field_type)

        # Store the value inside instance.__dict__
        instance.__dict__[self.name] = value