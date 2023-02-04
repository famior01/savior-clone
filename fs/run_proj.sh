docker build -t registry.digitalocean.com/savior/savior:latest -f Dockerfile .
docker push registry.digitalocean.com/savior/savior --all-tags
