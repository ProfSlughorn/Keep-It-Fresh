import requests


def get_access_token(client_id, client_secret):
    """
    Fetches an access token from FatSecret API.

    Args:
        client_id (str): Your FatSecret API Client ID.
        client_secret (str): Your FatSecret API Client Secret.

    Returns:
        str: The access token.
    """
    url = "https://oauth.fatsecret.com/connect/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "image-recognition",  # Ensure this scope is correct
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get access token: {response.text}")


# Replace these with your actual Client ID and Client Secret
CLIENT_ID = "4e3672bde10043e4b3f0b89b33f408a6"
CLIENT_SECRET = "44b56dd7199e4d2286807ca4aa787774"

ACCESS_TOKEN = get_access_token(CLIENT_ID, CLIENT_SECRET)
print(f"Access Token: {ACCESS_TOKEN}")
