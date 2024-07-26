# EJECUTAR 

para construir el entorno:

```bash
docker compose build

```

levantar el entorno y abrir la url 0.0.0.0:8000
el usuario del admin de django es `oka`, password `Asdfg35$`
```bash
docker compose up
#apagar el entorno
docker compose down
```

levantar el entorno en segundo plano
```bash
docker compose up -d

``` 

ejecutar los tests(estan en la carpeta `tests/`)
```bash
pytest tests/
``` 




## DEVELOPMENT

congelar las dependencias del proyeto en local para despues generar el dockerfile
```bash
pip freeze > requirements.txt
```

crear docker (consola en debian):
```bash
sudo docker build -t django-app .
```

```bash

```


crearlo en background y ejecutar
```bash
sudo docker run -d -p 8000:8000 -v $(pwd):/app --name django-container django-app
sudo docker start django-container

#detener

sudo docker stop django-container

```

para ejecutarlo con autoreload sin ejecutarlo en background(crear volumen en el lugar actual del proyecto, almacena la db de sqlite)

```bash
sudo docker run -p 8000:8000 -v $(pwd):/app django-app
```

abrib consola en container para ejecutar migraciones 
```bash
docker exec -it django-container /bin/bash

```
