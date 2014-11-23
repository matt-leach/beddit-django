from django.shortcuts import redirect




def requires_token(func):
    """
    Decorator that ensures a view has both:
        a token 
        a user logged in
    
    Redirects to home page if not
    """
    def wrapper(request, *args, **kwargs):
        try:
            if "token" in request.session and request.user.id is not None:
                return func(request, *args, **kwargs)
            else:
                return redirect("home")
            
        # User may be None
        except AttributeError:
            return redirect("home")
        
        
    return wrapper