from .models import SiteSettings

def site_settings(request):
    """
    Возвращает последние настройки сайта во все шаблоны.
    Берет самый свежий объект SiteSettings.
    """
    settings = SiteSettings.objects.last()
    return {'site_settings': settings}