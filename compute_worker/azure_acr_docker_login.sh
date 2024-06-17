# We performed these steps:

# 1. Deploy Azure Container Registry  
# 2. Create Private Endpoint For The Container Registry  
#     * Go to your container registry in the Azure portal.
#     * Under the "Networking" section, select "Private endpoint connections".
#     * Click "+ Private endpoint" to create a new private endpoint.
#     * Fill in the required details such as name, region, and resource group.
#     * In the "Resource" section, select "Microsoft.ContainerRegistry/registries" and choose your registry.
#     * For "Target sub-resource," select "Registry".
#     * Choose the virtual network and subnet where the private endpoint will be deployed.
#     * Select or create a private DNS zone and link it to the virtual network.
# 3. Create and Link Private DNS Zone:  
#     * If not already created, go to "Private DNS zones" in the Azure portal.
#     * Click "+ Create" to create a new private DNS zone, e.g., privatelink.azurecr.io.
#     * Once created, go to the private DNS zone and add a virtual network link to your virtual network.
# 4. Configure VM to Use Azure DNS:  
#     * Ensure that your VM's network settings are configured to use Azure DNS.
#         - This is usually the default setting if the VM is within an Azure virtual network.
#     * Check the DNS settings of your VM’s virtual network. It should typically be set to "Default (Azure-provided)" DNS.

# 5. Assign Permissions:
#     * If not using managed identities, use admin credentials for **simplicity**.
#     * Go to the container registry, enable the admin user (under "Access keys"), and note down the username and password.


# From root of ./codabench
ACR=
USERNAME=""
PASSWORD=""
COMMAND="docker login $ACR.azure.cr -u $USERNAME -p $PASSWORD" 
# Login to the Azure Container Registry using admin credentials
docker compose exec compute_worker $COMMAND