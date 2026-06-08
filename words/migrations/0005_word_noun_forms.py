from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_alter_userword_id_alter_word_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='feminine_form',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='word',
            name='is_noun',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='word',
            name='masculine_form',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='word',
            name='plural_form',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='word',
            name='singular_form',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
