from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

WRONG_CREDENTIALS = "wrong credentials"
INACTIVE_ACCOUNT = "inactive account"

def login_user(request):
    if request.method == 'GET' :
            return render(request, 'accounts/login.html')
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
    except KeyError:
        return render(request, 'accounts/login.html', {'error_msg':WRONG_CREDENTIALS}) 
    else:
        if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("backend:index"))
                else:
                    return render(request, 'accounts/login.html', {'error_msg':INACTIVE_ACCOUNT})
        else:
            return render(request, 'accounts/login.html', {'error_msg':WRONG_CREDENTIALS}) 
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("articles:index"))