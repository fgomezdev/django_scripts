import json
from django.contrib.auth.models import User

actualizar_si_existe = False  #OJO!

try:
    with open("usuarios.json") as json_file:
        json_data = json.load(json_file)

    for data in json_data:
        user_to_create_or_update = None

        try:
            user_to_create_or_update = User.objects.get(username=data['username'])            
        except:
            if actualizar_si_existe:
                print(f"El usuario {data['username']} no existe!")
                
        if user_to_create_or_update is not None:
            if actualizar_si_existe:
                print(f"Actualizando usuario: {data['username']}")
                user_to_create_or_update.is_superuser=data['is_superuser']
                user_to_create_or_update.first_name=data['first_name']            
                user_to_create_or_update.last_name=data['last_name']
                user_to_create_or_update.email=data['email']
                user_to_create_or_update.is_staff=data['is_staff']
                user_to_create_or_update.is_active=data['is_active']
                # En caso de querer guardar la contraseña
                # no guardar así -> user_to_create_or_update.password=data['password']
                # porque no se guarda como hash, sino como texto plano
                # así sí: -> user_to_create_or_update.set_password(data['password'])                
            else:
                print(f"El usuario {data['username']} existe, saltando...")
        else:
            print(f"Creando usuario: {data['username']}")
            user_to_create_or_update = User.objects.create(is_superuser=data['is_superuser'],first_name=data['first_name'],username=data['username'],last_name=data['last_name'],email=data['email'],is_staff=data['is_staff'],is_active=data['is_active'])
            
        if user_to_create_or_update is not None:
            user_to_create_or_update.save()
except Exception as ex:
    print(f"Error al crear usuarios: {ex}")
