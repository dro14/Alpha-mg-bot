# Generated by Django 4.2.6 on 2023-10-27 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alpha", "0005_alter_delivery_cargo_type_alter_delivery_receiver_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="cargo_type",
            field=models.CharField(max_length=255, verbose_name="тип груза"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="receiver",
            field=models.CharField(
                max_length=255, null=True, verbose_name="получатель"
            ),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="receiver_address",
            field=models.CharField(max_length=255, verbose_name="адрес доставки"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="sender",
            field=models.CharField(max_length=255, verbose_name="отправитель"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="sender_address",
            field=models.CharField(max_length=255, verbose_name="адрес отправки"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="status",
            field=models.CharField(max_length=255, verbose_name="статус"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="transport_number",
            field=models.CharField(max_length=255, verbose_name="номер транспорта"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="transport_type",
            field=models.CharField(max_length=255, verbose_name="тип транспорта"),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="weight",
            field=models.CharField(max_length=255, verbose_name="вес (кг)"),
        ),
    ]
