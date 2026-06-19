# protesis_cancer_mama

## Comandos para ejecutar el contenedor de docker

#### Crear una imagen para la aplicación de Python
```
docker build -f Dockerfile.app -t canma_app:{VERSION!} .
```

#### Crear una imagen para el motor COLMAP
```
docker build --target runtime -t colmap_worker:{VERSION!} .
```

#### Correr el contenedor de docker

```
docker compose up -d
```

#### Ingresar dentro del contenedor de docker

```
docker compose exec app bash
```

## Comandos para probar código dentro del contenedor en Mac

#### Darle permiso a tu IP local en la terminal de la Mac

```
xhost +localhost
```

#### Dentro del contenedor, para ejecutar archivos escribe el siguiente comando

```
python interfaz_grafica/main_pantalla.py
```

#### Actualiza la lista de paquetes disponibles de bash

```
apt-get update
```

#### Instala el editor nano

```
apt-get install -y nano
```

## Borrar el contenedor en caso de saturación de memoria

#### Detener el contenedor

```
docker stop canma_container
```

#### Remover el contenedor pero no la imagen

```
docker rm canma_container
```

#### Borrar todo definitivamente

```
docker system prune -a --volumes
```