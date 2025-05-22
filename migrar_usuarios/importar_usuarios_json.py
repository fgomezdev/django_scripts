"""
Importar usuarios a Django desde un archivo JSON.
"""

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

actualizar_si_existe = False  # OJO!
usuarios_a_excluir = ["admin", "super_admin", "AnonymousUser"]
grupos_a_excluir = []
permisos_a_excluir = []

SET_PASSWORDS = True


def importar_usuarios():
    try:
        with open("usuarios.json") as json_file:
            json_data = json.load(json_file)

        for data in json_data:
            if data["username"] in usuarios_a_excluir:
                print(f"Saltando usuario: {data['username']}")
                continue

            user_to_create_or_update = None

            try:
                user_to_create_or_update = User.objects.get(username=data["username"])
            except:
                if actualizar_si_existe:
                    print(f"El usuario {data['username']} no existe!")

            user_permissions = Permission.objects.filter(
                codename__in=data["user_permissions"]
            ).values_list("id", flat=True)
            if user_to_create_or_update is not None:
                if actualizar_si_existe:
                    print(f"Actualizando usuario: {data['username']}")
                    user_to_create_or_update.is_superuser = data["is_superuser"]
                    user_to_create_or_update.first_name = data["first_name"]
                    user_to_create_or_update.last_name = data["last_name"]
                    user_to_create_or_update.email = data["email"]
                    user_to_create_or_update.is_staff = data["is_staff"]
                    user_to_create_or_update.is_active = data["is_active"]
                else:
                    print(f"El usuario {data['username']} existe, saltando...")
            else:
                print(f"Creando usuario: {data['username']}")
                user_to_create_or_update = User.objects.create(
                    is_superuser=data["is_superuser"],
                    first_name=data["first_name"],
                    username=data["username"],
                    last_name=data["last_name"],
                    email=data["email"],
                    is_staff=data["is_staff"],
                    is_active=data["is_active"],
                )

            user_to_create_or_update.groups.clear()
            user_to_create_or_update.user_permissions.clear()

            groups = Group.objects.filter(name__in=data["groups"])
            user_to_create_or_update.groups.set(groups)

            user_permissions = Permission.objects.filter(
                codename__in=data["user_permissions"]
            )
            user_to_create_or_update.user_permissions.set(user_permissions)

            # En caso de querer guardar la contraseña
            # no guardar así -> user_to_create_or_update.password=data['password']
            # porque no se guarda como hash, sino como texto plano
            # así sí: -> user_to_create_or_update.set_password(data['password'])
            if SET_PASSWORDS:
                user_to_create_or_update.set_password(data["password"])

            if user_to_create_or_update is not None:
                user_to_create_or_update.save()
    except Exception as ex:
        print(f"Error al crear usuarios: {ex}")


def importar_grupos():
    try:
        with open("grupos.json") as json_file:
            json_data = json.load(json_file)

        for data in json_data:
            if data["name"] in grupos_a_excluir:
                print(f"Saltando grupo: {data['name']}")
                continue

            group_to_create_or_update = None

            try:
                group_to_create_or_update = Group.objects.get(name=data["name"])
            except:
                if actualizar_si_existe:
                    print(f"El grupo {data['name']} no existe!")

            permissions = Permission.objects.filter(
                codename__in=data["permissions"]
            ).values_list("id", flat=True)
            if group_to_create_or_update is not None:
                if actualizar_si_existe:
                    print(f"Actualizando grupo: {data['name']}")
                else:
                    print(f"El grupo {data['name']} existe, saltando...")
            else:
                print(f"Creando grupo: {data['name']}")
                group_to_create_or_update = Group.objects.create(
                    name=data["name"],
                )

            group_to_create_or_update.permissions.clear()
            permissions = Permission.objects.filter(codename__in=data["permissions"])
            group_to_create_or_update.permissions.set(permissions)

            if group_to_create_or_update is not None:
                group_to_create_or_update.save()
    except Exception as ex:
        print(f"Error al crear grupos: {ex}")


importar_grupos()
importar_usuarios()
