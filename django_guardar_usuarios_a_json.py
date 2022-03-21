import json
from django.contrib.auth.models import User

usuarios = User.objects.all()
lst_usuarios = []
for user in usuarios:
    if user.username in ["super_admin", "AnonymousUser"]:
        continue

    user_data=user.__dict__
    user_data.pop("_state", None)
    user_data.pop("last_login", None)
    user_data.pop("date_joined", None)
    lst_usuarios.append(user_data)

with open("usuarios.json", "w") as resultado: 
    json.dump(lst_usuarios, resultado)
