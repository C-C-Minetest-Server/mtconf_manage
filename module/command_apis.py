def debug(func):
    def wrapped(*args,**kwargs):
        print("Args: " + str(args))
        print("Kwargs: " + str(kwargs))
        return func(*args,**kwargs)
    return wrapped

def require_param(func):
    def wrapped(*args,**kwargs):
        if (len(kwargs["param"]) != 2):
            print("This command requires param in order to work.")
            return False
        return func(*args,**kwargs)
    return wrapped

def no_param(func):
    def wrapped(*args,**kwargs):
        if (len(kwargs["param"]) != 1):
            print("This command does not require any params.")
            return False
        return func(*args,**kwargs)
    return wrapped

api_args = {}

def set_api_arg(key,value):
    api_args[key] = value

class require_api_arg:
    def __init__(self,key):
        self.key = key
    def __call__(self,func):
        def wrapped(*args,**kwargs):
            kwargs[self.key] = (None if self.key not in api_args else api_args[self.key])
            return func(*args,**kwargs)
        return wrapped
