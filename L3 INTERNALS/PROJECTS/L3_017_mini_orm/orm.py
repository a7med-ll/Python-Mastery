#-------------------------------------------------------------------------
# Object-Relational Mapping
#-------------------------------------------------------------------------

class L3_017Model:
    """Base ORM model."""

    def __init__(self, **kwargs) -> None:
        """Initialize model fields."""

        # loop through the dictionary that means it will have keys and values
        for key, value in kwargs.items():
            setattr(self, key, value)     # --> then after the loop assign the key that is the field_name and value

    def __repr__(self) -> str:
        """Return object representation."""

        # Display model name and values.
        class_name = self.__class__.__name__     # --> gets model name
        values = self.__dict__                  # --> gets key/value data

        # format
        fields = ", ".join(
            f"{key}={value!r}"                   # --> With !r, name='Ahmed' without !r, name=Ahmed
            for key, value in values.items()
        )

        # return the class_name and fields
        return f"{class_name}({fields})"


