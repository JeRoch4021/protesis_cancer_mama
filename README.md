# protesis_cancer_mama

## Comandos para ejecutar el contenedor de docker

#### Ejecutar una imagen para el contenedor
```
docker build --platform=linux/amd64 -t jeshuarocha/canma:{VERSION!} .
```

#### Respaldar la imagen en la nube de DockerHub

```
docker push jeshuarocha/canma:{VERSION!}
```

#### Correr el contenedor de docker

```
docker run -d --name canma_container -e DISPLAY=host.docker.internal:0 -v "$(pwd)":/app jeshuarocha/canma:{VERSION!} tail -f /dev/null
```

#### Ingresar dentro del contenedor de docker

```
docker exec -it canma_container /bin/bash
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