# Important note on uploading new content

🔁 Code Update → Live on Azure Flow
Make your code changes locally.

Rebuild your Docker image:

## Copy
docker build -t tomtullyacr987.azurecr.io/myapp:latest .

Push the updated image to your Azure Container Registry (ACR):

## Copy
az acr login --name tomtullyacr987
docker push tomtullyacr987.azurecr.io/myapp:latest

Tell your Azure Web App to use the new image:
If it's already using :latest, then just restarting the Web App will pull the newest version:

az webapp restart --name Tully-ISE-Recidency-Solution --resource-group myResourceGroup