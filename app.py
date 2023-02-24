import app_config
import model

import sys
import logging
import json
import os

import msal
from fastapi import FastAPI
import requests
import uvicorn

#"RD3@daltontofoli1gmail.onmicrosoft.com"
#"RD#D1g1t4l"

api = FastAPI()


app = msal.ClientApplication(
    os.getenv("CLIENT_ID"), authority=os.getenv("AUTHORITY"),
    client_credential=os.getenv("CLIENT_SECRET")
)

@api.post("/auth/")
async def auth_user(user : model.Logon):
    #print(user.username)
    #print(user.pw)

    result = None

    accounts = app.get_accounts(user.username)

    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Lets try.")
        result = app.acquire_token_silent(app_config.SCOPE, account=accounts[0])

    if not result:
        logging.info("No suitable token exists in cache, getting a new one from AAD.")
        result = app.acquire_token_by_username_password(
            user.username, user.pw, app_config.SCOPE
        )

    if "access_token" in result:
        graph_data = requests.get(app_config.ENDPOINT, headers={'Authorization': 'Bearer ' + result['access_token']},).json()
        print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
        return graph_data
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
    if 65001 in result.get("error_codes", []):
        print("Visit this to consent: ", app.get_authorization_request_url(app_config.SCOPE))