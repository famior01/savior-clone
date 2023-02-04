## to run the nginx container, run the following command:
  - kubectl apply -f k8s/nginx/deployment.yaml

* check deployment 
  - kubectl get deployments 
  - kubectl get deployment `name`

* check pods (It will show us the running instance of the deployment)
  - kubectl get pods
  - kubectl delete pod `name` (to delete a pod)

* to get into that pods
  - kubectl exec -it `pod-name` -- /bin/bash (to get into the pod, into the container)

# Deployment of the container

* to get stared the deployment
  - kubectl apply -f .\k8s\nginx\deployment.yaml

* to get down the deployment
  - kubectl delete -f .\k8s\nginx\deployment.yaml

* to get started the service
  - kubectl apply -f .\k8s\nginx\service.yaml

* to get down the service
  - kubectl delete -f .\k8s\nginx\service.yaml

* to get the details of the service
  - kubectl describe service <LB-NAME>
  - kubectl describe service nginx-service


* to get the service
  - kubectl get services
  - kubectl get service `name`
  - kubectl get service `name` -o yaml/json (to get the yaml or json file of the service)

* to get the logs
  - kubectl logs `pod-name`


# To Put Container to docker hub as private repo with digital ocean
- make container registry in digital ocean
- docker login registry.digitalocean.com
- generate token from digital ocean
- username / password will be this token

# to push the image to the registry
- cd fs
- docker build -t registry.digitalocean.com/`image-name`:`tag` -f Dockerfile .
   * docker build -t registry.digitalocean.com/savior-test/savior:latest -f Dockerfile .

- *now push the image to the registry* 
- docker push registry.digitalocean.com/`image-name`:`tag`
   * docker push registry.digitalocean.com/savior-test/savior --all-tags

# kubernetes secrets in Environment variables
- kubectl get secrets

# to create a secret
- kubectl create secret generic savior-fs-prod-env --from-env-file=fs/.env.prod
  - it will convert the .env.prod file to a secret file (base64 encoded)

# to see the secret
- kubectl get secret savior-fs-prod-env -o yaml

# to delete the secret for updating the secret
- kubectl delete secret savior-fs-prod-env

# to create a secret for app
<!-- https://docs.digitalocean.com/products/container-registry/how-to/use-registry-docker-kubernetes/#add-secret-control-panel -->
- download the secret from digital ocean container registry panel
-  kubectl create secret generic savior-registry --from-file=.dockerconfigjson=docker-config.json --type=kubernetes.io/dockerconfigjson

# to see the Service Account
- kubectl get serviceaccount

# Start deployment 
- kubectl apply -f k8s/apps/savior-pod.yaml

# to get the pods
- kubectl get pods

# active venv in the pod
- kubectl exec -it `pod-name` -- /bin/bash
- source /opt/venv/bin/activate