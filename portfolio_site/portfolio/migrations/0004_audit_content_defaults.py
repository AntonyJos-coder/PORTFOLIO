from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0003_profile_learning_focus"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="skill",
            options={"ordering": ["order", "name"]},
        ),
        migrations.AlterField(
            model_name="education",
            name="degree",
            field=models.CharField(
                help_text="e.g. Diploma in Computer Engineering",
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="full_name",
            field=models.CharField(default="Antony Jos", max_length=100),
        ),
        migrations.AlterField(
            model_name="profile",
            name="tagline",
            field=models.CharField(
                default="Hi, I'm Antony Jos.",
                help_text='Big hero heading, e.g. "Hi, I\'m Antony Jos."',
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="title",
            field=models.CharField(
                default="Computer Engineer",
                help_text="e.g. Computer Engineer",
                max_length=100,
            ),
        ),
    ]
