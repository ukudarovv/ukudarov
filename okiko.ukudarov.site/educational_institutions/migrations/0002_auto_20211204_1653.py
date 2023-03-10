# Generated by Django 3.1.6 on 2021-12-04 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('educational_institutions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='administrator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.universityadministrator', verbose_name='Администратор'),
        ),
        migrations.AddField(
            model_name='university',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.categoryuniversity', verbose_name='Категория ВУЗа'),
        ),
        migrations.AddField(
            model_name='university',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.city', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='university',
            name='scientific_degrees_educational_programs',
            field=models.ManyToManyField(blank=True, related_name='related_scientific_degrees', to='educational_institutions.ScientificDegrees', verbose_name='Академические степени для образовательных программ'),
        ),
        migrations.AddField(
            model_name='university',
            name='scientific_degrees_specializations',
            field=models.ManyToManyField(blank=True, related_name='related_specializations', to='educational_institutions.ScientificDegrees', verbose_name='Академические степени для специальности'),
        ),
        migrations.AddField(
            model_name='university',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.typeuniversity', verbose_name='Тип ВУЗа'),
        ),
        migrations.AddField(
            model_name='specializations',
            name='groups_of_educational_programs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.groupsofeducationalprograms', verbose_name='Группа образовательных программ'),
        ),
        migrations.AddField(
            model_name='specializations',
            name='scientific_degrees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.scientificdegrees', verbose_name='Академическая степень'),
        ),
        migrations.AddField(
            model_name='specializations',
            name='unt_subjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.untsubjects', verbose_name='Профильные предметы на ЕНТ'),
        ),
        migrations.AddField(
            model_name='region',
            name='city',
            field=models.ManyToManyField(blank=True, related_name='related_city', to='educational_institutions.City', verbose_name='Города'),
        ),
        migrations.AddField(
            model_name='groupsofeducationalprograms',
            name='areas_of_education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.areasofeducation', verbose_name='Область образования'),
        ),
        migrations.AddField(
            model_name='groupsofeducationalprograms',
            name='areas_of_training',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.areasoftraining', verbose_name='Направление подготовки'),
        ),
        migrations.AddField(
            model_name='groupsofeducationalprograms',
            name='scientific_degrees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.scientificdegrees', verbose_name='Академическая степень'),
        ),
        migrations.AddField(
            model_name='groupsofeducationalprograms',
            name='unt_subjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.untsubjects', verbose_name='Профильные предметы на ЕНТ'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='areas_of_education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.areasofeducation', verbose_name='Область образования'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='areas_of_training',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.areasoftraining', verbose_name='Направление подготовки'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='groups_of_educational_programs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.groupsofeducationalprograms', verbose_name='Группа образовательных программ'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='scientific_degrees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.scientificdegrees', verbose_name='Академическая степень'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.university', verbose_name='ВУЗ'),
        ),
        migrations.AddField(
            model_name='educationalprograms',
            name='unt_subjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.untsubjects', verbose_name='Профильные предметы на ЕНТ'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_region', to='educational_institutions.region', verbose_name='Область'),
        ),
        migrations.AddField(
            model_name='areasoftraining',
            name='areas_of_education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.areasofeducation', verbose_name='Область образования'),
        ),
        migrations.AddField(
            model_name='areasoftraining',
            name='scientific_degrees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.scientificdegrees', verbose_name='Академическая степень'),
        ),
        migrations.AddField(
            model_name='areasofeducation',
            name='scientific_degrees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational_institutions.scientificdegrees', verbose_name='Академическая степень'),
        ),
    ]
