# Generated by Django 3.2.4 on 2021-06-28 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210628_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcart',
            name='products',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.shopcart'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
