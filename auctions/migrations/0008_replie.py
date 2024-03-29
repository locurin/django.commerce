# Generated by Django 3.1.7 on 2021-03-16 03:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210316_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='replie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='replies_to_comments', to='auctions.listing')),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_replied', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='auctions.comment')),
            ],
        ),
    ]
