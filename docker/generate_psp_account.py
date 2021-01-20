#!/usr/bin/python

# Example command: python3 generate_psp_account.py generated-psp-account-name

import requests
import sys
from string import Template

base_psp_url = 'http://crypto-payment-service-provider.lta.internal/psp/v1.1'


def get_token():
    url = "https://payment-service-provider.lta.intra-apps.com/psp/oauth/token"

    payload = "username=psp-qaa&password=bezk3z34g3Ywu8S&grant_type=password&scope=permissions"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'Cookie': "JSESSIONID=node07apw1d6rplrdspbhfaeem0o1966130.node0"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()['access_token']


def get_mnemonic(token):
    url = base_psp_url + "/mnemonic"

    headers = {
        'accept': "application/json",
        'authorization': "Bearer {token}".format(token=token)
    }

    response = requests.request("GET", url, data="", headers=headers)

    return response.json()["mnemonicCode"]


def create_account(token, account_name, mnemonics):
    url = base_psp_url + "/account"

    payload = Template('''{
        "accountName": "$account_name",
        "walletCreator": "treasury-qaa",
        "userNames": [
                "psp-qaa"
        ],
        "walletSpecifications": [
            {
                "currencyCode": "BTC",
                "mnemonic": "$btc_mnemonic"
            },
            {
                "currencyCode": "BCH",
                "mnemonic": "$bch_mnemonic"
            },
            {
                "currencyCode": "BSV",
                "mnemonic": "$bsv_mnemonic"
            }
        ]
    }''').substitute({
        'account_name': account_name,
        'btc_mnemonic': mnemonics[0],
        'bch_mnemonic': mnemonics[1],
        'bsv_mnemonic': mnemonics[2]
    })

    headers = {
        'accept': "application/json, text/plain, */*",
        'authorization': "Bearer {token}".format(token=token),
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    account_id = response.headers['Location'].split("/")[-1]

    return account_id


def get_account(token, account_id):
    url = base_psp_url + "/account/" + account_id

    payload = ""
    headers = {
        'accept': "application/json",
        'authorization': "Bearer {token}".format(token=token)
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.json()['apiKey']


def get_merchant(token, account_id):
    url = base_psp_url + "/account/{account_id}/merchants".format(account_id=account_id)

    payload = ""
    headers = {
        'accept': "application/json",
        'authorization': "Bearer {token}".format(token=token)
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.json()[0]['merchantId']


def generate_psp_account():
    if len(sys.argv) != 2:
        exit()

    account_name = sys.argv[1]
    token = get_token()

    mnemonics = []
    for x in range(3):
        mnemonics.append(get_mnemonic(token))

    if len(mnemonics) != 3:
        exit()

    account_id = create_account(token, account_name, mnemonics)
    merchant_id = get_merchant(token, account_id)
    api_key = get_account(token, account_id)

    print(merchant_id)
    print(api_key)

    print(Template('''
    PSP account was created:
        Account name: $account_name 
        Account ID: $account_id 
        Merchant ID: $merchant_id
        Api Key: $api_key
    ''').substitute({
        'account_name': account_name,
        'account_id': account_id,
        'merchant_id': merchant_id,
        'api_key': api_key,
    }))


generate_psp_account()