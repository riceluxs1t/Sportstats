# Generated by Django 2.0.6 on 2018-06-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('team_one', models.CharField(max_length=128)),
                ('team_two', models.CharField(max_length=128)),
                ('team_one_score', models.IntegerField()),
                ('team_two_score', models.IntegerField()),
                ('location', models.CharField(max_length=128)),
                ('match_type', models.CharField(max_length=128)),
                ('home_team', models.CharField(max_length=128)),
                ('team_one_rating', models.IntegerField()),
                ('team_two_rating', models.IntegerField()),
                ('team_one_rating_change', models.IntegerField()),
                ('team_two_rating_change', models.IntegerField()),
                ('team_one_rank', models.IntegerField()),
                ('team_two_rank', models.IntegerField()),
                ('team_one_rank_change', models.IntegerField()),
                ('team_two_rank_change', models.IntegerField()),
            ],
        ),
    ]