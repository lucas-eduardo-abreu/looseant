from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from looseinventory.inventory.services import get_matches


@login_required
def matches_view(request):
    data = get_matches()
    return render(request, "inventory/matches.html", {"rows": data})
