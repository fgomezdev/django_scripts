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
    user_data.pop("last_login", None) 
    lst_usuarios.append(user.__dict__) 

with open("usuarios.json", "w") as resultado: 
    json.dump(lst_usuarios, resultado)
