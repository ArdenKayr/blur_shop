from django.db import models

class FilterGroup(models.Model):
    """Группы фильтров, например: 'Тип кожи', 'Бренд'"""
    name = models.CharField(max_length=100, verbose_name="Название группы")

    class Meta:
        verbose_name = "Группа фильтров"
        verbose_name_plural = "Группы фильтров"

    def __str__(self):
        return self.name

class FilterValue(models.Model):
    """Значения фильтров, например: 'Сухая', 'Жирная'"""
    group = models.ForeignKey(FilterGroup, on_delete=models.CASCADE, related_name='values', verbose_name="Группа")
    value = models.CharField(max_length=100, verbose_name="Значение")

    class Meta:
        verbose_name = "Значение фильтра"
        verbose_name_plural = "Значения фильтров"

    def __str__(self):
        return f"{self.group.name}: {self.value}"

class Product(models.Model):
    """Модель товара с двумя типами цен"""
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    
    # Розничная цена и цена для косметологов
    price_retail = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (розница)")
    price_pro = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (для косметологов)")
    
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение товара")
    
    # Связь с фильтрами (Многие-ко-многим)
    filters = models.ManyToManyField(FilterValue, blank=True, related_name='products', verbose_name="Фильтры")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
class CarouselItem(models.Model):
    """Слайды для главной страницы"""
    title = models.CharField("Заголовок (для админки)", max_length=100, blank=True)
    image = models.ImageField("Изображение баннера", upload_to='carousel/')
    link = models.CharField("Ссылка", max_length=255, blank=True, help_text="Например: / или https://google.com")
    order = models.PositiveIntegerField("Порядок отображения", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Слайд карусели"
        verbose_name_plural = "Слайды карусели"
        ordering = ['order']

    def __str__(self):
        return self.title or f"Слайд {self.id}"