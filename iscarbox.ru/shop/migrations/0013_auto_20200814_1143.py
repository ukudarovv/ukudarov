# Generated by Django 3.1 on 2020-08-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_categoryproductaccessory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryproductaccessory',
            name='product',
            field=models.ManyToManyField(null=True, to='shop.Product', verbose_name='Товары где будут использоваться аксессуар'),
        ),
    ]