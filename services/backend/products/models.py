from django.db import models

class Category(models.Model):
    """Разделы каталога (меню)"""
    name = models.CharField("Название раздела", max_length=100)
    slug = models.SlugField("URL (ссылка)", unique=True, help_text="Например: face, body, sets")
    order = models.PositiveIntegerField("Порядок вывода", default=0, help_text="Чем меньше число, тем левее в меню")

    class Meta:
        verbose_name = "Раздел (Категория)"
        verbose_name_plural = "Разделы (Категории)"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class FilterGroup(models.Model):
    name = models.CharField("Название группы", max_length=100) # Например "Объем", "Тип кожи"
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Группа фильтров"
        verbose_name_plural = "Группы фильтров"

class FilterValue(models.Model):
    group = models.ForeignKey(FilterGroup, on_delete=models.CASCADE, related_name='values')
    value = models.CharField("Значение", max_length=100) # Например "50 мл", "Сухая"

    def __str__(self):
        return f"{self.group.name}: {self.value}"
    class Meta:
        verbose_name = "Значение фильтра"
        verbose_name_plural = "Значения фильтров"

class Product(models.Model):
    # Добавили связь с категорией
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products',
        verbose_name="Раздел"
    )
    
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    price_retail = models.DecimalField("Цена (Розница)", max_digits=10, decimal_places=2)
    price_pro = models.DecimalField("Цена (ПРО)", max_digits=10, decimal_places=2)
    
    image = models.ImageField("Фото товара", upload_to='products/', blank=True, null=True)
    
    is_new = models.BooleanField("Новинка", default=True)
    
    filters = models.ManyToManyField(FilterValue, blank=True, verbose_name="Характеристики")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class CarouselItem(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Картинка слайда", upload_to='carousel/')
    link = models.CharField("Ссылка при клике", max_length=200, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Слайд карусели"
        verbose_name_plural = "Слайды карусели"
        ordering = ['order']