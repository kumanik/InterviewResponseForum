# Generated by Django 3.0.4 on 2020-03-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responseForum', '0003_interviewresponse_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewresponse',
            name='review',
            field=models.CharField(max_length=1000000),
        ),
    ]
