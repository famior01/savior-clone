# Generated by Django 4.1.3 on 2022-12-04 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_avatar'),
        ('zakat_posts', '0008_alter_downvote_user_alter_upvote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakatposts',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]
