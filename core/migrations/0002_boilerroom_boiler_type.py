

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boilerroom',
            name='boiler_type',
            field=models.CharField(choices=[('scheme_1', 'Scheme 1 (a-d)'), ('scheme_2', 'Scheme 2 (a-d)'), ('scheme_9', 'Scheme 9 (a-d)'), ('scheme_10', 'Scheme 10 / 10c')], default='scheme_1', max_length=20),
        ),
    ]
