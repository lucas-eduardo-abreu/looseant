from django.core.exceptions import PermissionDenied

class SuperuserDeleteOnlyAdminMixin:
    """
    Bloqueia delete para não-superuser.
    """
    def has_delete_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)


class OwnUserOnlyAdminMixin:
    """
    Para modelos que têm campo `user`:
      - user comum só vê registros do próprio user
      - user comum só pode criar/editar para si mesmo
      - superuser pode tudo
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if "user" not in [f.name for f in self.model._meta.get_fields()]:
            return qs
        return qs.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        """
        Em user comum, o campo 'user' fica readonly (e a gente força no save_model).
        """
        ro = list(getattr(super(), "get_readonly_fields", lambda *_: [])(request, obj))
        if not request.user.is_superuser:
            ro.append("user")
        return ro

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Em user comum, no formulário, o dropdown de 'user' fica fixo no próprio usuário.
        """
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = type(request.user).objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Em user comum:
          - criação: força obj.user = request.user
          - edição: impede trocar obj.user
        """
        if not request.user.is_superuser:
            if change:
                # garante que não está tentando editar algo de outro user (defesa extra)
                if obj.user_id != request.user.id:
                    raise PermissionDenied("Você só pode editar registros do seu próprio usuário.")
            obj.user = request.user
        super().save_model(request, obj, form, change)