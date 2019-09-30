# Generated by Django 2.2.2 on 2019-09-30 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpinHamiltonian',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IsingModel',
            fields=[
                ('spinhamiltonian_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hamiltonian.SpinHamiltonian')),
                ('j', models.DecimalField(decimal_places=3, help_text='Interaction parameter of th the Ising Model. Implements uniform nearest neighbor interactions.', max_digits=5, verbose_name='Interaction')),
                ('n_sites', models.IntegerField(help_text='Number of sites in one spatial dimension', verbose_name='Number of sites')),
            ],
            options={
                'unique_together': {('j', 'n_sites')},
            },
            bases=('hamiltonian.spinhamiltonian',),
        ),
        migrations.CreateModel(
            name='ExteranlFieldIsingModel',
            fields=[
                ('spinhamiltonian_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hamiltonian.SpinHamiltonian')),
                ('j', models.DecimalField(decimal_places=3, help_text='Interaction parameter of th the Ising Model. Implements uniform nearest neighbor interactions.', max_digits=5, verbose_name='Interaction')),
                ('h', models.DecimalField(decimal_places=3, help_text='Implements uniform magnetic field: Implements uniform nearest neighbor interactions.', max_digits=5, verbose_name='External magnetic field')),
                ('n_sites', models.IntegerField(help_text='Number of sites in one spatial dimension', verbose_name='Number of sites')),
            ],
            options={
                'unique_together': {('j', 'h', 'n_sites')},
            },
            bases=('hamiltonian.spinhamiltonian',),
        ),
        migrations.CreateModel(
            name='Eigenvalue',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True)),
                ('n_level', models.PositiveIntegerField(help_text='The nth eigenvalue extracted in ascending order.')),
                ('value', models.FloatField(help_text='The value of the eigenvalue')),
                ('matrix', models.ForeignKey(help_text='Matrix for which the eigenvalue has been computed.', on_delete=django.db.models.deletion.CASCADE, to='hamiltonian.SpinHamiltonian')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('matrix', 'n_level')},
            },
        ),
    ]