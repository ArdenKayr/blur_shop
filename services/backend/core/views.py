from django.shortcuts import render

def index(request):
    """Перенаправление на каталог (или главная)"""
    # Если у тебя главная сейчас в products, можно оставить просто pass или редирект
    # Но обычно index не нужен, если корневой URL ведет в products.urls
    pass 

def about(request):
    """Страница О бренде"""
    return render(request, 'about.html')