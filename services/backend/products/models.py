from django.db import models
from django.conf import settings
from decimal import Decimal

class Category(models.Model):
    name = models.CharField("Название раздела", max_length=100)
    slug = models.SlugField("URL (ссылка)", unique=True, help_text="Например: face, body, sets")
    order = models.PositiveIntegerField("Порядок вывода", default=0)

    class Meta:
        verbose_name = "Раздел (Категория)"
        verbose_name_plural = "Разделы (Категории)"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class FilterGroup(models.Model):
    name = models.CharField("Название группы", max_length=100)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Группа фильтров"
        verbose_name_plural = "Группы фильтров"

class FilterValue(models.Model):
    group = models.ForeignKey(FilterGroup, on_delete=models.CASCADE, related_name='values')
    value = models.CharField("Значение", max_length=100)

    def __str__(self):
        return f"{self.group.name}: {self.value}"
    class Meta:
        verbose_name = "Значение фильтра"
        verbose_name_plural = "Значения фильтров"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Раздел")
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    
    # --- ЦЕНЫ ---
    price_retail = models.DecimalField("Цена (Розничная)", max_digits=10, decimal_places=2, help_text="Обязательная цена для всех")
    # blank=True означает, что в админке можно оставить пустым (тогда подставится розничная)
    price_cosmetology = models.DecimalField("Цена (Косметолог)", max_digits=10, decimal_places=2, blank=True, null=True)
    price_manicure = models.DecimalField("Цена (Маникюр/Педикюр)", max_digits=10, decimal_places=2, blank=True, null=True)
    
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

    def save(self, *args, **kwargs):
        # Если спец. цены не заполнены, берем розничную
        if not self.price_cosmetology:
            self.price_cosmetology = self.price_retail
        if not self.price_manicure:
            self.price_manicure = self.price_retail
        super().save(*args, **kwargs)

    def get_price_for_user(self, user):
        """
        Возвращает наименьшую доступную цену.
        """
        # По умолчанию доступна только розница
        available_prices = [self.price_retail]
        
        if user.is_authenticated:
            if user.is_cosmetologist:
                available_prices.append(self.price_cosmetology)
            if user.is_manicurist:
                available_prices.append(self.price_manicure)
        
        # Возвращаем самую низкую (клиент всегда видит лучшее предложение)
        # filter(None) на случай если вдруг попадет null
        valid_prices = [p for p in available_prices if p is not None]
        return min(valid_prices)

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

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f"{self.user} -> {self.product}"