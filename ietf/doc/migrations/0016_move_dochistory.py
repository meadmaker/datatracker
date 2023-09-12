# Generated by Django 4.2.5 on 2023-09-11 17:52

from django.db import migrations

from django.db.models import Subquery, OuterRef, F


def forward(apps, schema_editor):
    DocHistory = apps.get_model("doc", "DocHistory")
    RelatedDocument = apps.get_model("doc", "RelatedDocument")
    DocHistory.objects.filter(type_id="draft", doc__type_id="rfc").update(type_id="rfc")
    DocHistory.objects.filter(
        type_id="draft", doc__type_id="draft", name__startswith="rfc"
    ).annotate(
        rfc_id=Subquery(
            RelatedDocument.objects.filter(
                source_id=OuterRef("doc_id"), relationship_id="became_rfc"
            ).values_list("target_id", flat=True)[:1]
        )
    ).update(
        doc_id = F("rfc_id"),
        type_id = "rfc"
    )
    assert not DocHistory.objects.filter(name__startswith="rfc", type_id="draft").exists()


def reverse(apps, schema_editor):
    # there is no going back
    raise NotImplementedError


class Migration(migrations.Migration):
    dependencies = [
        ("doc", "0015_delete_docalias"),
    ]

    operations = [migrations.RunPython(forward, reverse)]
