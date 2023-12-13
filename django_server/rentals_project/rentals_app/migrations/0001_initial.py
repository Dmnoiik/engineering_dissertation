# Generated by Django 4.2.8 on 2023-12-11 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.CharField(max_length=50)),
                ('link', models.URLField()),
                ('image_link', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rent', models.DecimalField(decimal_places=2, default=-1, max_digits=10)),
                ('address', models.CharField(max_length=255)),
                ('rooms', models.IntegerField()),
                ('surface', models.DecimalField(decimal_places=2, max_digits=6)),
                ('website', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
