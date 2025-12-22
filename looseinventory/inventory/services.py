# inventory/services.py
from __future__ import annotations

from typing import Any, Dict, List

from django.db.models import Q

from looseinventory.inventory.models import HaveListItem, SpecifiedItem, WantListItem


def get_matches() -> List[Dict[str, Any]]:
    """
    Para cada WANT aberto, lista todos os HAVEs que cobrem os requisitos.

    Regra:
      - mesmo Item
      - e para cada flag: se want.flag=True então have.flag=True
      - have pode ter flags extras
    """
    wants = (
        WantListItem.objects.select_related("user", "specified_item", "specified_item__item")
        .filter(status=WantListItem.Status.OPEN)
        .order_by("specified_item__item__name", "user__username", "created_at")
    )

    # Carrega todos os haves com join (evita N+1 no básico)
    haves = (
        HaveListItem.objects.select_related("user", "specified_item", "specified_item__item")
        .all()
    )

    results: List[Dict[str, Any]] = []

    # Obs: como o número de registros deve ser pequeno (guild), isso já voa.
    # Se crescer muito, a gente otimiza com SQL/annotate.
    for w in wants:
        want_spec: SpecifiedItem = w.specified_item
        # Q que garante que o HAVE tem pelo menos as flags exigidas
        q_cover = want_spec.want_covered_by_have_q()

        possible_haves = haves.filter(
            specified_item__in=SpecifiedItem.objects.filter(q_cover)
        ).exclude(user=w.user)

        results.append(
            {
                "want": w,
                "have_list": list(possible_haves),
            }
        )

    return results
