PLUGIN_REGISTRY = {}

def plugin(name):

    def decorator(func):
        PLUGIN_REGISTRY[name] = func
        return func

    return decorator

def run_plugin(name, *args, **kwargs):

    if name not in PLUGIN_REGISTRY:
        raise KeyError(f"plugin {name} not registered")

    func = PLUGIN_REGISTRY[name]
    return func(*args, **kwargs)
