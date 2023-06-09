# Generated by Django 4.1.7 on 2023-05-08 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MechanicOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_content', models.TextField()),
                ('offer_price', models.FloatField()),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offers.clientorder')),
            ],
        ),
        migrations.DeleteModel(
            name='MechanicsOffer',
        ),
    ]
