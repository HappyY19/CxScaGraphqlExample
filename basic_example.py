import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


def get_new_token(token_url, request_data, timeout=120, verify_ssl_cert=False, cert=None):
    """

    Args:
        token_url (str): "http://localhost"
        request_data (dict):
        timeout (float, tuple, optional):
        verify_ssl_cert (bool, str):
        cert:

    Returns:
        Bear Token (str)
    """

    response = requests.post(url=token_url, data=request_data, timeout=timeout, verify=verify_ssl_cert, cert=cert)

    if response.status_code != 200:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


token_req_data = {
        "username": "***",
        "password": "***",
        "acr_values": "Tenant:" + "***",
        "grant_type": "password",
        "scope": "sca_api access_control_api",
        "client_id": "sca_resource_owner",
    }

token = get_new_token(token_url="https://platform.checkmarx.net/identity/connect/token", request_data=token_req_data)

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api-sca.checkmarx.net/graphql/graphql", headers={'Authorization': token})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=False)

# Provide a GraphQL query
query = gql(
    """
    query {
     privateDependencies {
         items {
             packageName
             packageManager
         }
     }
}
"""
)

# Execute the query on the transport
result = client.execute(query)
print(result)