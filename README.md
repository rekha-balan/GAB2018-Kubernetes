# GAB2018- "Delivering modern web applications with Kubernetes and OpenSource Technologies"

Resources for GAB2018 Talk: Delivering modern web applications with Kubernetes and OpenSource Technologies

Files used for Demos of this talk

## Containers Demo

You can use the files on /ContainersDemo to build a Docker image with a Python flask application that displays a random cat gif each time that the web page is refreshed.

### Build the Docker Image

If you want to inspect the code, requirements and steps to build the image please look at the Dockerfile content.

``` docker build -t catgifapp https://github.com/vcach/GAB2018-Kubernetes.git#master:ContainersDemo ```

### Run Docker container locally

``` docker container run --name catgif01 -d -p 5000:5000 catgifapp ```

## Azure Container Registry Demo

### Create Azure Container Registry

Prerequisites: Install azure-cli on your OS and login to your account with ```az login ``` or use Cloud Shell from Azure portal
You can create an Azure Container Registry (ACR) to storage your Docker images in a private repository.

First you need to create a Resource Group

```az group create --name myResourceGroup --location eastus ```

Then create the Container Registry specifying the name of the Resource Group created

``` az acr create --resource-group myResourceGroup --name myContainerRegistryName --sku Basic ```

### Push the catgifapp Docker image to ACR

First you need to login to ACR 

``` az acr login --name <acrName> ```

Before you can push an image to your registry, you must tag it with the fully qualified name of your ACR login server. Run the following command to obtain the full login server name of the ACR instance

``` az acr list --resource-group myResourceGroup --query "[].{acrLoginServer:loginServer}" --output table ```

Tag the image using the Docker tag command. Replace <acrLoginServer> with the login server name of your ACR instance

``` docker tag catgifapp <acrLoginServer>/catgifapp:v1 ```

Finally, use docker push to push the image to the ACR instance

``` docker push <acrLoginServer>/catgifapp:v1 ```

Verify that the image was pushed to ACR by listing images in the repository

```az acr repository list --name <acrName> --output table ```




