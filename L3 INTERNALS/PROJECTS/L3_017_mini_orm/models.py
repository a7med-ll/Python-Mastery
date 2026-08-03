from fields import L3_017Field
from orm import L3_017Model


#-------------------------------------------------------------------------
# User ORM Model
#-------------------------------------------------------------------------

class L3_017User(L3_017Model):
    """User ORM model."""

    username = L3_017Field(str, required=True)  # --> Required username field.
    age = L3_017Field(int, required=True)       # --> Required age field.
    email = L3_017Field(str, required=False)    # --> Optional email field.


#-------------------------------------------------------------------------
# Product ORM Model
#-------------------------------------------------------------------------

class L3_017Product(L3_017Model):
    """Product ORM model."""

    name = L3_017Field(str, required=True)      # --> Required product name.
    price = L3_017Field(float, required=True)   # --> Required product price.
    stock = L3_017Field(int, required=True)     # --> Required product stock.