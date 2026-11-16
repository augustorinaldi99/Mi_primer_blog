from django.db import migrations


# Copia los tags existentes en el orden en que se muestran actualmente.
def copiar_tags_orden(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    PostTag = apps.get_model("posts", "PostTag")
    base = schema_editor.connection.alias

    vinculos_antiguos = Post.tags.through
    ultimo_post_id = None
    posicion = 0

    for vinculo in vinculos_antiguos.objects.using(base).order_by(
        "post_id", "tag_id"
    ):
        if vinculo.post_id != ultimo_post_id:
            ultimo_post_id = vinculo.post_id
            posicion = 0

        PostTag.objects.using(base).create(
            post_id=vinculo.post_id,
            tag_id=vinculo.tag_id,
            posicion=posicion,
        )
        posicion += 1


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0006_posttag"),
    ]

    operations = [
        migrations.RunPython(copiar_tags_orden, migrations.RunPython.noop),
    ]