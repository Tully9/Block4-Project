# StakeHolders
- ISE Industry lads
    - Mark & Ian
    - Future Industry Lads
- ISE partner companies
    - Companies that signed up
    - Companies for a student only
- ISE students
    - Passed students
    - Failed students
    - Linking-in students

# Data Requirements
- Students list companies

Refer to sheet of paper

# Important note on uploading new content

🔁 Code Update → Live on Azure Flow
Make your code changes locally.

Rebuild your Docker image:

docker build -t tomtullyacr987.azurecr.io/myapp:latest .

Push the updated image to your Azure Container Registry (ACR):

az acr login --name tomtullyacr987
docker push tomtullyacr987.azurecr.io/myapp:latest

Tell your Azure Web App to use the new image:
If it's already using :latest, then just restarting the Web App will pull the newest version:

az webapp restart --name Tully-ISE-Recidency-Solution --resource-group myResourceGroup