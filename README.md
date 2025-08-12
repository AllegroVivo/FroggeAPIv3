# FroggeAPI

Version `3.0.0` 

Version `3.0.0` of FroggeAPI is a complete rewrite of the original FroggeAPI, 
which is based on the [FastAPI](https://fastapi.tiangolo.com/) framework. The 
following are instructions on how to connect to the secure endpoints of the API.

## Registration
To register a new user with the API, send a POST request to the `/auth/register` 
endpoint with the following JSON payload:

```json
{
    "user_id": <discord_user_id>,
    "password": <your_password>,
    "frogge":<Allegro-provided secret key>
}
```

This should only be necessary once per client.

## Authentication
To authenticate with the API, send a POST request to the `/auth/login` endpoint
with the following form data:

```plaintext
username=<discord_user_id>
password=<your_password>
```

Note that the `username` field should contain the Discord user ID.

Upon successful authentication, the API will return a JSON response containing
an `access_token` and a `token_type`. The `access_token` is a JWT (JSON Web Token)
that you will use to authenticate subsequent requests to the API.