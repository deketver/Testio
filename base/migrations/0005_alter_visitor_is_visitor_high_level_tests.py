# Generated by Django 4.0.6 on 2022-07-20 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_delete_high_level_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='is_visitor',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='High_level_tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=400, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('sf_code', models.CharField(max_length=300)),
                ('family', models.CharField(max_length=200)),
                ('sf_sn', models.CharField(blank=True, max_length=200)),
                ('si_id_string', models.CharField(blank=True, max_length=200, null=True)),
                ('result', models.CharField(max_length=200)),
                ('fail_test_name', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('fail_group_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('test_total_time', models.IntegerField()),
                ('tester_info', models.CharField(blank=True, max_length=200)),
                ('user_name', models.CharField(blank=True, max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('ini_security', models.CharField(blank=True, max_length=300)),
                ('number_of_test', models.IntegerField(blank=True, default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.test_project')),
            ],
        ),
    ]
