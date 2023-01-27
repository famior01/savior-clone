##  Build Docker Image 

```
docker compose up --build
```

##  Rebuild Docker Image
```
docker compose build
```

##  Run Docker Image
```
docker compose up
```

##  Run Docker Image on background
```
docker compose up -d 
```

##  Stop Docker Image
```
docker compose stop
```

## Stop Docker Image on background
```
docker compose down
```

##  Run Docker Image with specific service
```
docker compose up -d web
```

##  Run Docker Image with specific service and rebuild
```
docker compose up -d --build web
```

## To watch the details of Image
```
docker images
```

- or for more details 

```
docker inspect <image_id>
``` 

## To watch the details of Container
```
docker ps
```

- or for all containers running or stopped

``` 
docker ps -a
```
