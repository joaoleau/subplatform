import requests
import json
from .models import Subscription
from decouple import config


def get_access_token_paypal():
    data = {
        "grant_type": "client_credentials"
    }

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }

    client_id = config("CLIENT_ID")
    secret_id = config("SECRET_ID")

    url = "https://api.sandbox.paypal.com/v1/oauth2/token"

    response = requests.post(url, auth=(
        client_id, secret_id), headers=headers, data=data).json()

    access_token = response["access_token"]
    return access_token


def cancel_subscription_paypal(access_token, subID):
    bearer_token = "Bearer" + access_token
    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer_token
    }

    url = "https://api.sandbox.paypal.com/v1/billing/subscriptions/" + subID + "/cancel"
    response = requests.post(url, headers=headers)


def update_subscription_paypal(access_token, subID):
    bearer_token = "Bearer" + access_token
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "en_US",
        "Authorization": bearer_token
    }
    subscription = Subscription.objects.get(paypal_subscription_id=subID)
    current_sub_plan = subscription.plan

    new_sub_plan_id = None
    if current_sub_plan.name == "Standard":
        new_sub_plan_id = "P-79F92206JA736893VMXONXHI"

    elif current_sub_plan.name == "Premium":
        new_sub_plan_id = "P-37W71531BU030260RMXN7HKY"

    url = "https://api.sandbox.paypal.com/v1/billing/subscriptions/" + subID + "/revise"

    revision_data = {
        "plan_id": new_sub_plan_id
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(revision_data))
    response_data = response.json()

    approve_link = None
    for link in response_data.get("links", []):
        if link.get("rel") == "aprove":
            approve_link = link["href"]

    if response.status_code == 200:
        return approve_link

    # print(f"Error Request:'{response_data.get('name')}':'{response_data.get('message')}'")
    return None


def get_current_subscription(access_token, subID):
    bearer_token = "Bearer" + access_token
    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer_token
    }
    url = f"https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}"
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        subscription_data = r.json()
        current_plan_id = subscription_data.get("plan_id")
        return current_plan_id

    print("Failed")
    return
