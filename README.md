# Scripts para shell de django

Los scripts deben ejecutarse desde el mismo directorio donde se encuentra el archivo manage.py de la siguiente manera:

* Importar usuarios desde un archivo CSV a la base de datos de Django.
```bash
python manage.py shell < crear_usuarios_csv.py
```

* Exportar usuarios desde la base de datos de Django a un archivo JSON (Servidor origen).
```bash
python manage.py shell < exportar_usuarios_json.py
```

* Importar usuarios desde un archivo JSON a la base de datos de Django (Servidor destino).
```bash
python manage.py shell < importar_usuarios_json.py
```
