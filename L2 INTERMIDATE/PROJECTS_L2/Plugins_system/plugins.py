from register import plugin

@plugin("greet")
def greet_user(name):

    return f"Hello {name} How are you doing?"

@plugin("multiply")
def multiply(a,b):

    return a*b

