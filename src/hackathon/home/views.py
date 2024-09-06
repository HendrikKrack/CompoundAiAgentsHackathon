from django.contrib import messages
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_user(request):
    email = request.POST.get('inputEmail')
    password = request.POST.get('inputPassword')
    print(email, password)
    if email == "a@b.com" and password == "123":
        return render(request, 'success_page_1.html')
    else:
        messages.error(request, "Invalid Credentials")
        return render(request, 'index.html')
    
def goto_final_page(request):
    return render(request, 'success_page_2.html')
