"""
Import data into CCS
1. Import repositories
2. Import custom policies
3. Import suppressions
4. Import enforcement rules
"""
import json
import os
import requests as req
import sys
import time
from datetime import timedelta

api = os.getenv('PRISMA_API_URL')
username = os.getenv('PRISMA_ACCESS_KEY_ID')
password = os.getenv('PRISMA_SECRET_KEY')
if ( api is None or username is None or password is None):
    print('Missing environment variables')
    sys.exit(1)

"""
Check the result of a restful API call
"""
def result_ok(result, message):
    if ( not result.ok ):
        print(message)
        result.raise_for_status()

"""
Authenticate against Prisma cloud. Return authentication JWT token
"""
def auth_prisma():
    payload = { 'username': username, 'password': password }
    headers = { 
        'Content-Type': 'application/json; charset=UTF-8', 
        'Accept': 'application/json; charset=UTF-8' 
    }
    result = req.post(f"{api}/login", data=json.dumps(payload), headers=headers)
    result_ok(result,'Could not authenticate to Prisma.')
    return result.json()['token']

"""
Create headers for the RESTful API calls. Returns a headers object.
"""
def get_headers(token):
    return { 
        'Content-Type': 'application/json; charset=UTF-8', 
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }


"""
Import repos from repos.json
"""
def import_github_repos():
    print('Importing repos from repos.json')
    # Load repo list from repos.json
    all_repos = []
    with open('data/repos.json','r') as reposfile:
        all_repos = json.loads(reposfile.read())
    # Filter out non Github repos
    github_only = [ r for r in all_repos if r['source'] == 'Github' ]
    if len(github_only) == 0:
        print('No Github repos found.')
        sys.exit(1)
    repos = [ f"{r['owner']}/{r['repository']}" for r in github_only ]
    headers = get_headers(auth_prisma())

    url = f"{api}/code/api/v1/repositories"
    print('Posting to repositories API')
    # Post to repository API  
    payload = json.dumps({ "data": repos, "type": "github" })
    print(url)
    print(payload)
    result = req.post(url, headers=headers, data=payload)
    result_ok(result, 'Could not enroll repositories.')

"""
Get all currently integrated repositories. Returnss an array of repo objects
"""
def get_all_repos():
    print('Getting a list of integrated repos')
    headers = get_headers(auth_prisma())

    url = f"{api}/code/api/v1/repositories"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get repositories.')
    print(result.text)

"""
Import all custom rules from runConfiguration.json
"""
def import_custom_policies():
    print('Importing all custom policies for runConfiguration.json')
    headers = get_headers(auth_prisma())
    custom_policies = []
    with open('data/customPolicies.json', 'r') as rcfile:
        custom_policies = json.loads(rcfile.read())

    url = f"{api}/policy"

    for cp in custom_policies['data']:
        if(cp['code']):
            payload = json.dumps({            
                "cloudType": cp['provider'],
                "complianceMetadata": [],
                "description": cp['guideline'],
                "labels": [],
                "name": cp['title'],
                "policySubTypes": ['build'],
                "policyType": "config",
                "recommendation": "",
                "rule": {
                    "children": [
                        {
                            "metadata": {
                                "code": cp['code']
                            },
                            "type": "build",
                            "recommendation": ""
                        }
                    ],
                    "name": cp['title'],
                    "parameters": {
                        "savedSearch": "false",
                        "withIac": "true"
                    },
                    "type": "Config"
                },
                "severity": cp['severity'],
                "findingTypes": []
            })            
            result = req.post(url, headers=headers, data=payload)
            result_ok(result, f"Unable to import custom policy ID {cp['id']},\n payload: {payload}")
            print(cp['id'])
        else:            
            print(f"**{cp['id']}**")
        time.sleep(10)
        
    print('===')

"""
Import policy suppressions. Custom policies need to be imported first.
"""
def import_policy_suppressions():
    print('Importing policy type suppressions')
    headers = get_headers(auth_prisma())
    # Get all existing suppressions
    url = f"{api}/code/api/v1/suppressions"
    result = req.get(url, headers=headers)
    result_ok(result, 'Failed to get a list of suppressions.')
    ccs_supp = result.json()
    # Read from exported data
    with open('data/suppressions.json','r') as suppfile:
        bc_supp = json.loads(suppfile.read())
    # Filter by type of policy
    for ps in bc_supp:
        if ps['suppressionType'] == 'Policy':
            # Currently custom suppressions are not handled
            if ps['policyId'].startswith('BC_'):
                existing_supp = [cs for cs in ccs_supp if cs['policyId'] == ps['policyId']]
                if len(existing_supp) > 0:
                    print(f"Deleting policy suppression for {existing_supp[0]['policyId']}")
                    url = f"{api}/code/api/v1/suppressions/{existing_supp[0]['policyId']}/justifications/{existing_supp[0]['id']}"
                    result = req.delete(url, headers=json.dumps({'authorization': headers['x-redlock-auth']}))
                    result_ok(result, f"Failed to delete suppression {existing_supp[0]['id']}")

                url = f"{api}/code/api/v1/suppressions/{ps['policyId']}"
                payload = json.dumps({
                    'comment': ps['comment'],
                    'expirationTime': int(time.time() + timedelta(days=365).total_seconds()),
                    'origin': 'Platform',
                    'suppressionType': 'Policy'
                })
                result = req.post(url, headers=headers, data=payload)
                result_ok(result, f"Failed to create policy suppression for {ps['policyId']}")
            else:
                print(f"Suppression for custom policy {ps['policyId']} not imported.")

"""
Import enforcement rules
"""
def import_enforcement_rules():
    print('Import enforcement rules from enfRules.json')
    # Need export, then https://pan.dev/prisma-cloud/api/code/edit-rule/


if __name__ == '__main__':
    print('Import Bridgecrew data into Prisma Cloud Code Security module 0.0.1')
    #import_github_repos()
    #get_all_repos()
    #import_custom_policies()
    import_policy_suppressions()
    #import_enforcement_rules()
    print('Done')


