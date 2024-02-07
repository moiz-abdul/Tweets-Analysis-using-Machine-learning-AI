# Generated by Django 4.2.4 on 2023-09-01 12:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OTP', models.IntegerField()),
                ('OTP_create', models.DateTimeField(default=django.utils.timezone.now)),
                ('User_login', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Myapp.uzerlogin')),
            ],
        ),
    ]
