# Generated by Django 4.0 on 2022-10-16 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coefficient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.IntegerField()),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Katusa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('eng_name', models.CharField(blank=True, max_length=20, null=True)),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L')], max_length=20, null=True)),
                ('rank', models.IntegerField(choices=[(1, 'Pv2'), (2, 'Pv1'), (3, 'Cpl'), (4, 'Sgt')])),
                ('is_rso', models.IntegerField(blank=True, choices=[(0, 'Us'), (1, 'Rso')], null=True)),
                ('this_duty_dates_score', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['total_score'],
            },
        ),
        migrations.CreateModel(
            name='ThisDutyDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty_date', models.DateField()),
                ('date_score', models.IntegerField(choices=[(1, 'Weekday Has Ccpt'), (2, 'Weekday'), (4, 'Departure'), (3, 'Arrival'), (5, 'Pass')])),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='this_duty_dates', to='cq_roster.katusa')),
            ],
            options={
                'ordering': ['duty_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherDutyDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty_date', models.DateField()),
                ('duty_type', models.CharField(choices=[('KP', 'Headcount'), ('GG', 'Gymguard')], max_length=20)),
                ('date_type', models.IntegerField(choices=[(1, 'Weekday'), (2, 'Offday')])),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_duty_dates', to='cq_roster.katusa')),
            ],
        ),
        migrations.CreateModel(
            name='NextDutyDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty_date', models.DateField()),
                ('date_score', models.IntegerField(choices=[(1, 'Weekday Has Ccpt'), (2, 'Weekday'), (4, 'Departure'), (3, 'Arrival'), (5, 'Pass')])),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_duty_dates', to='cq_roster.katusa')),
            ],
            options={
                'ordering': ['duty_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='cq_roster.katusa')),
            ],
        ),
    ]