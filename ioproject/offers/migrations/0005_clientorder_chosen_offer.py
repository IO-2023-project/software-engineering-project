# Generated by Django 4.1.7 on 2023-05-22 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_offeritem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientorder',
            name='chosen_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.mechanicoffer'),
        ),
    ]