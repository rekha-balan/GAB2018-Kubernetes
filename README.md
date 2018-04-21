# Global Azure Bootcamp Bogota 2018 - "Delivering modern web applications with Kubernetes and OpenSource Technologies"

Resources for GAB2018 Talk: Delivering modern web applications with Kubernetes and OpenSource Technologies

Files used for Demos of this talk

***

## Containers Demo

You can use the files on /ContainersDemo to build a Docker image with a Python flask application that displays a random cat gif each time that the web page is refreshed.

### Build the Docker Image

If you want to inspect the code, requirements and steps to build the image please look at the Dockerfile content.

``` docker build -t catgifapp https://github.com/vcach/GAB2018-Kubernetes.git#master:ContainersDemo ```

### Run Docker container locally

``` docker container run --name catgif01 -d -p 5000:5000 catgifapp ```

***

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

***

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

More info on AKS Kubernetes Dashboard UI: https://docs.microsoft.com/en-us/azure/aks/kubernetes-dashboard

### Upgrade Kubernetes and Scale the Nodes

#### Upgradae an AKS Cluster

Before upgrading a cluster, use the az aks get-upgrades command to check which Kubernetes releases are available for upgrade.

``` az aks get-upgrades --name myAKSCluster --resource-group myResourceGroup --output table ```

Take note of the version you want to upgrade to use with the "az aks upgrade" command

During the upgrade process, nodes are carefully [cordoned and drained][kubernetes-drain] to minimize disruption to running applications. Before initiating a cluster upgrade, ensure that you have enough additional compute capacity to handle your workload as cluster nodes are added and removed.

``` az aks upgrade --name myAKSCluster --resource-group myResourceGroup --kubernetes-version 1.8.2 ```

You can now confirm the upgrade was successful with the az aks show command

``` az aks show --name myAKSCluster --resource-group myResourceGroup --output table ```

More info about AKS Upgrade: https://docs.microsoft.com/en-us/azure/aks/upgrade-cluster

#### Scaling your AKS Cluster

Imagine a scenario where your realize that your existing cluster is at capacity and you need to scale it out to add more nodes in order to increase capacity and be able to deploy more PODS.

Check to see number of current nodes running

``` kubectl get nodes ```

Scale out AKS cluster to accomodate the demand

``` az aks scale -g myResourceGroup -n myAKSCluster --node-count 4 ```

Note this may take some time. Good time to get some coffee

Check to see if the new nodes are deployed and "Ready"

``` kubectl get nodes ```

***

## Automation Tools - Helm & Draft Demo

### Helm

Helm is a tool for managing Kubernetes charts. Charts are packages of pre-configured Kubernetes resources.

Use Helm to:

    Find and use popular software packaged as Kubernetes charts
    Share your own applications as Kubernetes charts
    Create reproducible builds of your Kubernetes applications
    Intelligently manage your Kubernetes manifest files
    Manage releases of Helm packages
    
Helm is a tool that streamlines installing and managing Kubernetes applications. Think of it like apt/yum/homebrew for Kubernetes

Install Helm is not part of the Demo but you need to install it first in order to use Draft and deploy our application to AKS. Review the info of this link to install Helm and configure it with your AKS cluster:

https://docs.microsoft.com/en-us/azure/aks/kubernetes-helm

Once Helm is installed and configured with your AKS Cluster you can continue to Draft

### Draft

Draft makes it easy to build applications that run on Kubernetes. Draft targets the "inner loop" of a developer's workflow: as they hack on code, but before code is committed to version control.

Using two simple commands, developers can now begin hacking on container-based applications without requiring Docker or even installing Kubernetes themselves.

For this Demo you first need to install Draft and make some configurations to make it work with your Azure Container Registry. As these steps are not part of the Demo, review the info of this link to install Draft and configure it with your ACR:

https://docs.microsoft.com/en-us/azure/aks/kubernetes-draft

### Use Draft with our catgifapp application

Clone this repo

```https://github.com/vcach/GAB2018-Kubernetes.git ```

Go to the Folder Draft_Demo

```cd Draft_Demo ```

Use Draft to autogenerate a Dockerfile, a Helm chart, and a draft.toml file, which is the Draft configuration file.

```draft create ```

Verify the Output of the Dockerfile and compare it to the one in the ContainersDemo folder. 
As you can see, draft is not totally accurate in the Dockerfile generation but you can use this file as a template to modify and do the necessary changes that meet your application requirements. Copy the content from /ContainersDemo/Dockerfile to the Dockerfile generated from Draft, should look like this:

```
# our base image
FROM alpine:latest

# Install python and pip
RUN apk add --update py-pip

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/app/app.py"]

```
Once the Dockerfile is ready you can use Draft to deploy your app on Kubernetes with "draft up". This command builds the Dockerfile to create a container image, pushes the image to ACR, and finally installs the Helm chart to start the application in AKS.

The first time this is run, pushing and pulling the container image may take some time; once the base layers are cached, the time taken is dramatically reduced

``` draft up ```

### Test the Application

To test the application, use the "draft connect" command. This command proxies a connection to the Kubernetes pod allowing a secure local connection. When complete, the application can be accessed on the provided URL.

In some cases, it can take a few minutes for the container image to be downloaded and the application to start. If you receive an error when accessing the application, retry the connection

```draft connect ```

Output:

```
Connecting to your app...SUCCESS...Connect to your app on localhost:46143
Starting log streaming...
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
== Spark has ignited ...
>> Listening on 0.0.0.0:4567
```
Now test your application by browsing to http://localhost:46143 (for the preceding example; your port may be different). When finished testing the application use Control+C to stop the proxy connection

More info about how to use Draft: https://docs.microsoft.com/en-us/azure/aks/kubernetes-draft










