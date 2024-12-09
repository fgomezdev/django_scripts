import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Usuarios
usuarios = User.objects.all()

print(f"Usuarios a exportar: {len(usuarios)}")
lst_usuarios = []
for user in usuarios:
    if user.username in ["admin", "super_admin", "AnonymousUser"]:
        continue

    user_data = user.__dict__
    user_data["groups"] = list(user.groups.values_list("name", flat=True))
    user_data["user_permissions"] = list(
        user.user_permissions.values_list("codename", flat=True)
    )

    user_data.pop("_state", None)
    user_data.pop("last_login", None)
    user_data.pop("date_joined", None)
    lst_usuarios.append(user_data)

with open("usuarios.json", "w") as resultado:
    json.dump(lst_usuarios, resultado)


# Grupos
groups = Group.objects.all()
print(f"Grupos a exportar: {len(groups)}")
lst_grupos = []
for group in groups:
    group_data = group.__dict__
    group_data["permissions"] = list(
        group.permissions.values_list("codename", flat=True)
    )

    group_data.pop("_state", None)
    group_data.pop("last_login", None)
    group_data.pop("date_joined", None)
    lst_grupos.append(group_data)

with open("grupos.json", "w") as resultado:
    json.dump(lst_grupos, resultado)

# # Permisos
# permissions = Permission.objects.all()
# print(f"Permisos a exportar: {len(permissions)}")
# lst_permisos = []
# for permission in permissions:
#     permission_data = permission.__dict__
#     permission_data.pop("_state", None)
#     permission_data.pop("last_login", None)
#     permission_data.pop("date_joined", None)
#     lst_permisos.append(permission_data)

# with open("permisos.json", "w") as resultado:
#     json.dump(lst_permisos, resultado)
