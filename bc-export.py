"""
Export data from BC
1. List of repositories
2. Enforcement rules
"""
import json
import os
import requests as req

api = 'https://www.bridgecrew.cloud/api'
key = os.getenv('BC_API_KEY')
headers = {
    "accept": "application/json",
    "authorization": key
}

"""
Check the result of a restful API call
"""
def result_ok(result, message):
    if ( not result.ok ):
        print(message)
        result.raise_for_status()

"""
Get all repos. Writes repos.json
"""
def export_repos():
    url = f"{api}/v1/repositories"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not retrieve repositories.')
    with open('data/repos.json','w') as reposfile:
        reposfile.write(json.dumps(result.json()))

"""
Export all enforcement rules
"""
def export_enforcement_rules():
    print('Export enforcement rules')
    url = f"{api}/v1/enforcement-rules"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get enforcement rules.')
    with open('data/enfRules.json', 'w') as enffile:
        enffile.write(json.dumps(result.json()))


if __name__ == '__main__':
    print('Export BC data 0.0.1')
    #export_repos()
    export_enforcement_rules()
    print('Done')
