from django.shortcuts import render

def about(request):
    """Страница О бренде"""
    return render(request, 'about.html')