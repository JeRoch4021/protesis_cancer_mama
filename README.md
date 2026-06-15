# protesis_cancer_mama

## Comandos para ejecutar el contenedor de docker

#### Ejecutar una imagen para el contenedor
```
docker build --no-cache -t pipeline_canma .
```

#### Ingresar dentro del contenedor de docker

```
docker run -it --rm -v "${PWD}":/app pipeline_canma bash
```

## Borrar el contenedor en caso de saturación de memoria

#### Detener el contenedor

```
docker stop $(docker ps -aq)
```

#### Remover el contenedor pero no la imagen

```
docker rm $(docker ps -aq)
```

#### Borrar todo definitivamente

```
docker system prune -a --volumes
```