# Generated by Django 3.2.7 on 2021-09-18 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_productfeatures_productfeaturevalidators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartProduct',
        ),
    ]
