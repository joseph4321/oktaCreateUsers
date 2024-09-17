#!/usr/bin/python

import csv
import requests
import json

# Okta URL and API token

okta_url = 'https://okta.com'
api_token = '$token'



# Function to create a user in Okta
def create_user(email, first_name, last_name, groups=[]):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_token}'
    }

    data = {
        'profile': {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'login': email,
        }
    }

    url = f'{okta_url}/users'

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 or (response.status_code == 400 and "An object with this field already exists in the current organization" in response.text):
        user_id = response.json().get('id')
        if(response.status_code == 200):
            print(f"[+] User {email} successfully created with ID: {user_id}")
        else:
            print(f"[+] User {email} already exists, attempting to add to groups")
            for group_id in groups:
                all_users = get_all_users()
                for u in all_users:
                    if( u['profile']['email'] == email):
                        user_id = u['id']

        # Add user to groups
        for group_id in groups:
            add_user_to_group(user_id, group_id, email)
    else:
        print(f"[-] Failed to create user {email}. Status code: {response.status_code}")
        print(response.text)

# Function to get all users
def get_all_users():
    url = f"{okta_url}/users"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


# Function to add user to a group
#def add_user_to_group(user_id, group_id):
def add_user_to_group(user_id, group_id, em):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_token}'
    }

    url = f'{okta_url}/groups/{group_id}/users/{user_id}'

    response = requests.put(url, headers=headers)

    gm = ""
    for item in groups:
        if( group_id == item['id']):
            gm = item['profile']['name']

    if response.status_code == 204:
        print(f"[+] User {em} ({user_id}) added to group {gm} ({group_id})")
    else:
        print(f"[-] Failed to add user {user_id} to group {group_id}. Status code: {response.status_code}")
        print(response.text)

def get_all_groups():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_token}'
    }

    url = f'{okta_url}/groups?limit=200'

    response = requests.get(url, headers=headers)

    return response.json()


def get_group(group_id):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_token}'
    }

    url = f'{okta_url}/groups/{groupId}'

    response = requests.get(url, headers=headers)

    return response.json()

# Example usage:
if __name__ == '__main__':

    rows = []
    # Open the CSV file in read mode
    with open('oktaUsers.csv', 'r') as csvfile:
        # Create a reader object
        csv_reader = csv.reader(csvfile)
  
        # Iterate through the rows in the CSV file
        for row in csv_reader:
            rows.append(row)


    groups = get_all_groups()
    for user in rows:
        tokens = user[3].split("|")
        for t in tokens:
            found=0
            for item in groups:
                if( t == item['profile']['name']):
                    found=1
            if(found == 0):
                print(f"[-] Unable to find group in {user[0]} - {t}.  Cowardly refusing to continue...")
                exit()

    for user in rows:
        ids = []
        tokens = user[3].split("|")
        for t in tokens:
            for item in groups:
                if( t == item['profile']['name']):
                    ids.append(item['id'])
        print(f"[+] Attempting to create user {user[0]},{user[1]},{user[2]},{ids}")
        create_user(user[0],user[1],user[2],ids)
        print("")















