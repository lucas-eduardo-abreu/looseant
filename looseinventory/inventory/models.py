from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q
from looseinventory.core.models import AbstractBaseModel

User = settings.AUTH_USER_MODEL


class Item(AbstractBaseModel):
    """Item base (somente nome)."""

    name = models.CharField(max_length=120, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SpecifiedItem(AbstractBaseModel):
    """
    Item + flags (mh/sd/dd/ref/dsr/zen).

    Regra de match "have cobre want":
      - Se WANT.flag=True => HAVE.flag tem que ser True
      - Se WANT.flag=False => indiferente (HAVE pode ser True/False)
    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="specified_items")

    mh = models.BooleanField(default=False)
    sd = models.BooleanField(default=False)
    dd = models.BooleanField(default=False)
    ref = models.BooleanField(default=False)
    dsr = models.BooleanField(default=False)
    zen = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Item Part'

        constraints = [
            models.UniqueConstraint(
                fields=["item", "mh", "sd", "dd", "ref", "dsr", "zen"],
                name="uniq_specified_item_by_flags",
            )
        ]
        indexes = [
            models.Index(fields=["item"]),
            models.Index(fields=["item", "mh", "sd", "dd", "ref", "dsr", "zen"]),
        ]

    def __str__(self) -> str:
        flags = [k.upper() for k in ("mh", "sd", "dd", "ref", "dsr", "zen") if getattr(self, k)]
        return f"{self.item.name} [{' '.join(flags) if flags else 'NO-FLAGS'}]"

    def want_covered_by_have_q(self) -> Q:
        """
        Retorna um Q() que seleciona HAVEs que cobrem este WANT.
        """
        q = Q(item=self.item)
        for flag in ("mh", "sd", "dd", "ref", "dsr", "zen"):
            if getattr(self, flag):
                q &= Q(**{flag: True})
        return q


class WantListItem(AbstractBaseModel):
    """Usuário PRECISA de um SpecifiedItem (requisitos mínimos)."""

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        DONE = "DONE", "Done"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="want_items")
    specified_item = models.ForeignKey(
        SpecifiedItem, on_delete=models.PROTECT, related_name="wanted_by"
    )

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["specified_item"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "specified_item", "status"],
                name="uniq_user_want_specified_item_status",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} wants {self.specified_item} ({self.status})"


class HaveListItem(AbstractBaseModel):
    """Usuário TEM um SpecifiedItem (atributos reais)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="have_items")
    specified_item = models.ForeignKey(
        SpecifiedItem, on_delete=models.PROTECT, related_name="owned_by"
    )


    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["specified_item"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "specified_item"],
                name="uniq_user_have_specified_item",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} has {self.specified_item}"
