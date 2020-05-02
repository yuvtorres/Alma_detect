class APIError(Exception):
    statusCode = 500

class Error404(APIError):
    statusCode = 404


def errorHandler(fn):
    def wrapper(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except APIError as e:
            print(e)
            return {
                "status":"error",
                "message":str(e)
            }, e.statusCode
    wrapper.__name__ = fn.__name__
    return wrapper 
