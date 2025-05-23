# Important note on uploading new content

🔁 Code Update → Live on Azure Flow
Make your code changes locally.

Rebuild your Docker image:

## Copy
```
docker build -t tomtullyacr987.azurecr.io/myapp:latest .
az acr login --name tomtullyacr987
docker push tomtullyacr987.azurecr.io/myapp:latest
az webapp restart --name Tully-ISE-Recidency-Solution --resource-group myResourceGroup
```