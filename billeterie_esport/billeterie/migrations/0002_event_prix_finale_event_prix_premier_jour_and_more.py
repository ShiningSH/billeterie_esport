# Generated by Django 5.1.1 on 2024-09-04 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billeterie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='prix_finale',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='prix_premier_jour',
            field=models.DecimalField(decimal_places=2, default='2', max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='prix',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
