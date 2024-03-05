from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin, SlugMixin
from mptt.models import MPTTModel, TreeForeignKey
from services.choices import WATCH_FILTER, STATUS, GENDER, ACCESS, RATING
from services.uploader import Uploader
from services.slugify import slugify
from account.models import UserBase
from django.db.models import Case, When, FloatField, F, Avg
from django.db.models.functions import Coalesce


Users = get_user_model()

class Category(DateMixin, MPTTModel):
    name = models.CharField(max_length=150)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def watch_count(self):
        return Watch.objects.filter(category_id=self.id).count()


class Choice(DateMixin):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=WATCH_FILTER, max_length=150)

    def __str__(self):
        return slugify(self.name)

    def get_short_name(self):
        return slugify(self.name)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'


def get_choice(type):
    try:
        return ((choice.name, choice.name) for choice in Choice.objects.filter(type=type))
    except:
        return None

class Watch(DateMixin, SlugMixin):
    user_admin = models.ForeignKey(UserBase, on_delete=models.CASCADE, null=True, blank=True, default=1)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    header_image = models.ImageField(upload_to=Uploader.upload_watch_header_photo, max_length=500, null=True)
    manufactured = models.CharField(max_length=150)
    style = models.CharField(choices=get_choice("Style"), max_length=150)
    year = models.IntegerField()
    material = models.CharField(choices=get_choice("Material"), max_length=150)
    dial_color = models.CharField(choices=get_choice("Color"), max_length=150)
    band_color = models.CharField(choices=get_choice("Color"), max_length=150)
    movement = models.CharField(choices=get_choice("Movement"), max_length=150)
    case_size = models.FloatField()
    functionality = models.CharField(choices=get_choice("Functionality"), max_length=150)
    gender = models.CharField(choices=GENDER, max_length=150)
    status = models.CharField(choices=STATUS, default="Active", max_length=50)
    wishlist = models.ManyToManyField(Users, blank=True, related_name="wishlist")
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Watch'
        verbose_name_plural = 'Watches'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.stock < 1:
            self.status = 'Deactivate'
        return super().save(*args, **kwargs)

    @classmethod
    def calculate_price(self):
        return Watch.objects.annotate(
            discount_percent=Coalesce(F("discount"), 0, output_field=FloatField())
        ).annotate(
            total_price=Case(
                When(discount_percent=0, then=F("price")),
                default=F("price") + F("tax") - (F("price") * F("discount_percent") / 100),
                output_field=FloatField()
            )
        ).annotate(tax_price=F("price") + F("tax"))

    @classmethod
    def total_price(self):
        return self.calculate_price().filter(status='Active', stock__gte=1)

    def get_total_price(self):
        return self.calculate_price().get(id=self.id).total_price

    def rating(self):
        get_reviews = WatchReview.objects.filter(watch_id=self.id)
        # Gets the average rating value of the watch
        average_rating = get_reviews.aggregate(rating=Avg("rating"))['rating']

        return round(average_rating, 2) if average_rating else 0


class WatchImage(DateMixin):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=Uploader.upload_watch_photo, max_length=500)

    def __str__(self):
        return self.watch.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Watch Image'
        verbose_name_plural = 'Watch Images'

class Coupon(DateMixin):
    user = models.OneToOneField(Users, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=30)
    discount_rate = models.PositiveIntegerField()
    access = models.CharField(max_length=15, choices=ACCESS, default='Accessible')
    status = models.CharField(max_length=10, choices=STATUS, default='Active')

    def __str__(self):
        return self.code

    class Meta:
        ordering = ('-created_at', )
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def coupon_discount(self, request):
        coupon_disc = 0

        from basket.basket import Basket_Proc

        if Coupon.objects.filter(user__username=request.user.username, access="Inaccessible").exists():
            get_coupon = Coupon.objects.get(user__username=request.user.username)
            basket = Basket_Proc(request)
            coupon_disc = round((get_coupon.discount_rate * basket.subtotal()) / 100, 2)

        return coupon_disc


class WatchReview(DateMixin):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    watch = models.ForeignKey(Watch, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices=RATING, default=None)
    review = models.TextField()

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Watch Review'
        verbose_name_plural = 'Watch Reviews'
