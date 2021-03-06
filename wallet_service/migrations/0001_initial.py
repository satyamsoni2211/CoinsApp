# Generated by Django 3.2.8 on 2021-10-12 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.CharField(
                    max_length=100,
                    primary_key=True, serialize=False)),
                ('balance', models.FloatField(default=0.0)),
                ('currency', models.CharField(
                    choices=[('USD', 'USD'),
                             ('EUR', 'EUR'),
                             ('INR', 'INR')],
                    default='USD', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('direction', models.CharField(choices=[
                    ('INCOMING', 'INCOMING'),
                    ('OUTGOING', 'OUTGOING')], max_length=20)),
                ('account', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payments',
                    related_query_name='payments',
                    to='wallet_service.useraccount')),
                ('from_account', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payments_from',
                    related_query_name='payments_from',
                    to='wallet_service.useraccount')),
                ('to_account', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payments_to',
                    related_query_name='payments_to',
                    to='wallet_service.useraccount')),
            ],
        ),
    ]
