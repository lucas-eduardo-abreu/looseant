from __future__ import annotations

from itertools import combinations

from django.db import migrations


FLAGS = ("mh", "sd", "dd", "ref", "dsr", "zen")


def forwards(apps, schema_editor):
    Item = apps.get_model("inventory", "Item")
    SpecifiedItem = apps.get_model("inventory", "SpecifiedItem")

    base_flags = {f: False for f in FLAGS}

    for item in Item.objects.all().iterator(chunk_size=1000):
        to_create = []

        # exatamente 1, 2 e 3 flags True
        for r in (1, 2, 3):
            for combo in combinations(FLAGS, r):
                payload = base_flags.copy()
                for flag in combo:
                    payload[flag] = True

                to_create.append(
                    SpecifiedItem(
                        item=item,
                        **payload,
                    )
                )

        # ignore_conflicts respeita o UniqueConstraint
        SpecifiedItem.objects.bulk_create(
            to_create,
            ignore_conflicts=True,
            batch_size=1000,
        )


def backwards(apps, schema_editor):
    """
    Remove apenas combinações com 1, 2 ou 3 flags True.
    NÃO remove NO-FLAGS nem combinações > 3.
    """
    SpecifiedItem = apps.get_model("inventory", "SpecifiedItem")

    SpecifiedItem.objects.extra(
        where=[
            "(mh::int + sd::int + dd::int + ref::int + dsr::int + zen::int) BETWEEN 1 AND 3"
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_load_items"),  # ajuste aqui
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
