# Start app with Docker locally

First we need to create folders for static files.
```bash
mkdir static && mkdir staticfiles
```

Now we can build the app image.
```bash
docker-compose build
```

When the build process is finished, we can launch the application.
```bash
docker-compose up
```

# Enter the container

```bash
docker-compose exec backend /bin/sh
```
```bash
docker-compose exec db /bin/sh
```

# Checking the logs

To view logs for all containers, use the command:
```bash
docker-compose logs -f
```

Add container name at the end to view logs of the specific container:
```bash
docker-compose logs -f backend
```

# Environment variables
| name              | value |
|-------------------|-------|
| NUTRITION_API_KEY |       |


