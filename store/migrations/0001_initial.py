# Generated by Django 4.2.7 on 2024-03-05 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import services.uploader


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=150)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Style', 'Style'), ('Functionality', 'Functionality'), ('Material', 'Material'), ('Color', 'Color'), ('Movement', 'Movement')], max_length=150)),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('code', models.SlugField(editable=False, null=True, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('discount', models.FloatField(null=True)),
                ('tax', models.FloatField(null=True)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('description', models.TextField()),
                ('header_image', models.ImageField(max_length=500, null=True, upload_to=services.uploader.Uploader.upload_watch_header_photo)),
                ('manufactured', models.CharField(max_length=150)),
                ('style', models.CharField(choices=[('Casual', 'Casual'), ('Dress', 'Dress'), ('Wood', 'Wood'), ('Sport', 'Sport'), ('Nurse', 'Nurse'), ('Pocket', 'Pocket'), ('Field', 'Field'), ('Fitness', 'Fitness'), ('Smart', 'Smart'), ('Luxury', 'Luxury'), ('Fashion', 'Fashion'), ('Racing', 'Racing'), ('Military', 'Military'), ('Aviator', 'Aviator')], max_length=150)),
                ('year', models.IntegerField()),
                ('material', models.CharField(choices=[('Tungsten', 'Tungsten'), ('Ceramic', 'Ceramic'), ('Titanium', 'Titanium'), ('Carbon', 'Carbon'), ('Stainless Steel', 'Stainless Steel'), ('Gold', 'Gold')], max_length=150)),
                ('dial_color', models.CharField(choices=[('Yellow', 'Yellow'), ('Two Tone', 'Two Tone'), ('Silver Tone', 'Silver Tone'), ('Red', 'Red'), ('Purple', 'Purple'), ('Orange', 'Orange'), ('Gunmetal', 'Gunmetal'), ('Green', 'Green'), ('Brown', 'Brown'), ('Black', 'Black'), ('White', 'White'), ('Tortoise', 'Tortoise'), ('Rose Gold Tone', 'Rose Gold Tone'), ('Rainbow', 'Rainbow'), ('Mother Of Pearl', 'Mother Of Pearl'), ('Grey', 'Grey'), ('Gold Tone', 'Gold Tone'), ('Blue', 'Blue'), ('Beige', 'Beige')], max_length=150)),
                ('band_color', models.CharField(choices=[('Yellow', 'Yellow'), ('Two Tone', 'Two Tone'), ('Silver Tone', 'Silver Tone'), ('Red', 'Red'), ('Purple', 'Purple'), ('Orange', 'Orange'), ('Gunmetal', 'Gunmetal'), ('Green', 'Green'), ('Brown', 'Brown'), ('Black', 'Black'), ('White', 'White'), ('Tortoise', 'Tortoise'), ('Rose Gold Tone', 'Rose Gold Tone'), ('Rainbow', 'Rainbow'), ('Mother Of Pearl', 'Mother Of Pearl'), ('Grey', 'Grey'), ('Gold Tone', 'Gold Tone'), ('Blue', 'Blue'), ('Beige', 'Beige')], max_length=150)),
                ('movement', models.CharField(choices=[('Hand Wind', 'Hand Wind'), ('Solar', 'Solar'), ('Quartz', 'Quartz'), ('Automatic', 'Automatic'), ('Mechanical', 'Mechanical')], max_length=150)),
                ('case_size', models.FloatField()),
                ('functionality', models.CharField(choices=[('Hybrid', 'Hybrid'), ('Chronograph', 'Chronograph'), ('Digital', 'Digital'), ('Analogue', 'Analogue')], max_length=150)),
                ('gender', models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ('Unisex', 'unisex')], max_length=150)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Deactivate', 'Deactivate')], max_length=50)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
                ('user_admin', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wishlist', models.ManyToManyField(blank=True, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Watch',
                'verbose_name_plural': 'Watches',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='WatchReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '★✩✩✩✩'), (2, '★★✩✩✩'), (3, '★★★✩✩'), (4, '★★★★✩'), (5, '★★★★★')], default=None)),
                ('review', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('watch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.watch')),
            ],
            options={
                'verbose_name': 'Watch Review',
                'verbose_name_plural': 'Watch Reviews',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='WatchImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('image', models.ImageField(max_length=500, upload_to=services.uploader.Uploader.upload_watch_photo)),
                ('watch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.watch')),
            ],
            options={
                'verbose_name': 'Watch Image',
                'verbose_name_plural': 'Watch Images',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.CharField(max_length=30)),
                ('discount_rate', models.PositiveIntegerField()),
                ('access', models.CharField(choices=[('Accessible', 'Accessible'), ('Inaccessible', 'Inaccessible')], default='Accessible', max_length=15)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Deactivate', 'Deactivate')], default='Active', max_length=10)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'ordering': ('-created_at',),
            },
        ),
    ]
