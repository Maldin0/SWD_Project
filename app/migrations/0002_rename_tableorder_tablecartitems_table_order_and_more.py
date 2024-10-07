# Generated by Django 5.1.1 on 2024-10-07 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tablecartitems',
            old_name='tableOrder',
            new_name='table_order',
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='status',
            field=models.CharField(choices=[('NOT_FINISH', 'Not Finish'), ('PENDING', 'Pending'), ('COOKING', 'Cooking'), ('SERVING', 'Serving'), ('FINISHED', 'Finished')], default='NOT_FINISH'),
        ),
    ]
