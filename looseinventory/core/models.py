from django.db import models
from uuid import uuid4

class AbstractBaseModel(models.Model):
    """Modelo Abstrato para ser usado em todos os nossos modelos posteriores."""

    uuid = models.UUIDField(verbose_name='UUID', default=uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True
