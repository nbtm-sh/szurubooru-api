import base64

def generate_auth_token(username, api_token):
    raw = username + ":" + api_token
    b64 = base64.b64encode(bytes(raw, "ASCII")).decode("UTF-8")

    return b64
