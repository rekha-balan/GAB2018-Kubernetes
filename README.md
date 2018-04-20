# Global Azure Bootcamp Bogota 2018 - "Delivering modern web applications with Kubernetes and OpenSource Technologies"

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

## Kubernetes - AKS Demo

If it's possible, do these steps using Azure Cloud Shell, this shell is preconfigured with all the software you need to complete this process. If you are an advanced user, consider to install azure-cli and kubectl on your machine to complete the steps from your computer directly.

More info: https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough

Tip: Use the same Resource Group created on ACR steps to create the AKS cluster

### Create an AKS cluster

Use the az aks create command to create an AKS cluster. The following example creates a cluster named myAKSCluster with one node.

``` az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1 --generate-ssh-keys ```

### Connect to the Cluster and get info

To manage a Kubernetes cluster, use kubectl, the Kubernetes command-line client.

If you're using Azure Cloud Shell, kubectl is already installed. If you want to install it locally, use the az aks install-cli command from azure-cli

```az aks install-cli ```

To configure kubectl to connect to your Kubernetes cluster, use the az aks get-credentials command. This step downloads credentials and configures the Kubernetes CLI to use them

``` az aks get-credentials --resource-group myResourceGroup --name myAKSCluster ```

To verify the connection to your cluster, use the kubectl get command to return a list of the cluster nodes. Note that this can take a few minutes to appear

```kubectl get nodes ```

Also you can run the kubectl cluster info command to see more details about your cluster

``` kubectl cluster-info ```

### Kubernetes Dashboard UI

The Azure CLI can be used to start the Kubernetes Dashboard. Use the "az aks browse" command to start the Kubernetes dashboard. When running this command, replace the resource group and cluster name

``` az aks browse --resource-group myResourceGroup --name myAKSCluster ```

This command creates a proxy between your development system and the Kubernetes API, and opens a web browser to the Kubernetes dashboard.



