# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 20:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessStatus',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=50)),
                ('access_to_role', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationCompleted',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('info', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BankOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('period', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmedOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('confirmed_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('period_approved', models.IntegerField()),
                ('installment_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totall_credit_amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='ContractTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_start_of_employment', models.DateField()),
                ('end_of_employment', models.DateField(blank=True, null=True)),
                ('occupational_group', models.CharField(choices=[('el1', 'Parlamentarzyści, wyżsi urzędnicy i kierownicy'), ('el2', 'Specjaliści'), ('el3', 'Technicy i inni średni personel'), ('el4', 'Pracownicy biurowi'), ('el5', 'Pracownicy usług osobistych i sprzedawcy'), ('el6', 'Robotnik przemysłowy'), ('el7', 'Operator i monter maszyn'), ('el8', 'Siły zbrojne'), ('el9', 'Inne')], default='el2', max_length=50)),
                ('awerage_six_monthly_income', models.FloatField()),
                ('profession', models.CharField(max_length=50)),
                ('nip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CreditApplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('table_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PensionTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('pension_amount', models.FloatField()),
                ('card_number', models.CharField(max_length=50)),
                ('application', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CreditApplication')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pesel', models.CharField(max_length=11, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('identity_card', models.CharField(max_length=9)),
                ('telephon_number', models.CharField(blank=True, max_length=9)),
                ('mail', models.EmailField(max_length=100)),
                ('monthly_expenses', models.FloatField()),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=6)),
                ('street', models.CharField(blank=True, max_length=50)),
                ('house_number', models.IntegerField()),
                ('flat_number', models.CharField(blank=True, max_length=5)),
                ('education', models.CharField(choices=[('GIM', 'gimnazjalne'), ('POD', 'podstawowe'), ('ZAZ', 'zasadnicze zawodowe'), ('SRE', 'średnie'), ('WYZ', 'wyższe')], default='POD', max_length=20)),
                ('marital_status', models.CharField(choices=[('brak', 'brak'), ('kawaler', 'kawaler'), ('panna', 'panna'), ('wdowiec', 'wdowiec'), ('wdowa', 'wdowa'), ('rozwodnik', 'rozwodnik'), ('rozwódka', 'rozwódka')], default='brak', max_length=20)),
                ('iban_number', models.CharField(blank=True, max_length=26, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('role', models.CharField(max_length=20)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProposedOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('initial_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('maximal_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('minimum_load_period', models.IntegerField()),
                ('maximum_load_period', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RequiredDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('documents_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SentDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='documents/%Y/%m/%d//')),
                ('name', models.CharField(max_length=50)),
                ('reason_negativ_decision', models.CharField(blank=True, max_length=50)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='added_documents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.SentDocument'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='confirmed_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ConfirmedOffer'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='icome',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.IncomeName'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='personal_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PersonalData'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='proposed_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ProposedOffer'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='required_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.RequiredDocument'),
        ),
        migrations.AddField(
            model_name='creditapplication',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.AccessStatus'),
        ),
        migrations.AddField(
            model_name='contracttable',
            name='application',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CreditApplication'),
        ),
        migrations.AddField(
            model_name='applicationcompleted',
            name='application',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CreditApplication'),
        ),
    ]
