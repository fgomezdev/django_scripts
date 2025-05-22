"""
Importar usuarios a Django desde un archivo CSV
(Este caso es puntualmente para Geonode ya que contempla los campos de perfil)
"""

import csv
import os

from django.contrib.auth import get_user_model

# Valid fields for a Geonode user profile:
# first_name, last_name, email, username, password, is_staff,
# organization, profile, position, voice, fax, delivery,
# city, area, zipcode, country, keywords, language, timezone


def clear_string(s):
    chars = ["\t", "\n", "\r", "\x0b", "\x0c", "\u00a0", "\u200b", "\ufeff", "ï»¿"]

    for c in chars:
        s = s.replace(c, "")

    return s.strip()


def create_user(**kwargs):
    replace_user = kwargs.pop("replace_user", False)

    User = get_user_model()

    for k in kwargs.keys():
        if k not in [f.name for f in User._meta.get_fields()]:
            raise ValueError(f"El campo '{k}' no es válido para el modelo User.")

    username = clear_string(kwargs.get("username"))
    if not username:
        raise ValueError("El campo 'username' es obligatorio.")

    for k, v in kwargs.items():
        if v and isinstance(v, str):
            v = clear_string(v)

        if k == "username":
            # if not v.isalnum():
            #     raise ValueError(
            #         "El campo 'username' solo puede contener caracteres alfanuméricos."
            #     )
            if len(v) < 3:
                raise ValueError(
                    "El campo 'username' debe tener al menos 3 caracteres."
                )

            v = v.lower()

        if k in ["first_name", "last_name"]:
            v = v.title()

        if k == "email":
            if v and "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("El campo 'email' no es válido.")
            v = v.lower()

        kwargs[k] = v

    if not kwargs.get("password"):
        raise ValueError("El campo 'password' es obligatorio.")

    user_exists = User.objects.filter(username=username).exists()
    user = None
    if user_exists:
        if replace_user:
            user = User.objects.get(username=username)
            user.delete()
        else:
            print(f"El usuario '{username}' ya existe.")
            return

    user = User.objects.create_user(**kwargs)

    message = ""
    if user_exists:
        message = f"Usuario '{username}' {'reemplazado' if user else 'eliminado'} exitosamente."
    else:
        message = f"Usuario '{username}' {'creado exitosamente' if user else 'no pudo ser creado'}."

    print(message)


def import_from_csv(filename, delimiter=";", replace_users=True):
    if not os.path.isfile(filename):
        print(f"El archivo '{filename}' no existe.")
        return

    with open(
        filename,
        mode="r",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            create_user(**row, replace_user=True)


import_from_csv("usuarios.csv")
