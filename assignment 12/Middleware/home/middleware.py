# Function-based middleware
def first_middleware(get_response):
    print("One time initialization")  # server start a one time print

    def middleware_func(request):
        print("Function Middleware: Before view")
        response = get_response(request)
        print("Function Middleware: After view")
        return response

    return middleware_func


# Class-based middleware
class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("Class Middleware Initialized")  # server start a one time print

    def __call__(self, request):
        print("Class Middleware: Before view")
        response = self.get_response(request)
        print("Class Middleware: After view")
        return response