# Generated by Django 5.1.2 on 2024-10-16 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_bot', '0002_alter_tweets_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='id',
            field=models.CharField(default='1ae3ad39-b114-418e-b314-1ee478a7fc02', max_length=50, primary_key=True, serialize=False),
        ),
    ]
