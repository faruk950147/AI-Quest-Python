from urllib import response

def first_middleware(get_response):
    print("One time initialization")

    def first_func(request):
        print("this is before view")
        response = get_response(request)
        print("this is after view")
        return response

    return first_func


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print("this is before view")
        response = self.get_response(request)
        print("this is after view")
        return response