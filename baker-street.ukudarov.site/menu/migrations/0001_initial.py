# Generated by Django 4.0.2 on 2022-04-16 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория ингредиента',
                'verbose_name_plural': 'Категории ингредиентов',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Название')),
                ('unit_of_measurement', models.CharField(blank=True, choices=[('kg', 'кг'), ('pc', 'шт'), ('l', 'л')], default='kg', max_length=100, verbose_name='Ед. измерения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingredient_category', to='menu.ingredientcategory', verbose_name='Категория ингредиента')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
    ]
