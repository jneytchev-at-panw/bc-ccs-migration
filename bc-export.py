"""
Export data from BC
1. List of repositories
2. Enforcement rules
3. Custom policies
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
    print('Exporting repositories.')
    url = f"{api}/v1/repositories"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not retrieve repositories.')
    with open('data/repos.json','w') as reposfile:
        reposfile.write(json.dumps(result.json()))

"""
Export all enforcement rules
"""
def export_enforcement_rules():
    print('Exporting enforcement rules.')
    url = f"{api}/v1/enforcement-rules"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get enforcement rules.')
    with open('data/enfRules.json', 'w') as enffile:
        enffile.write(json.dumps(result.json()))

"""
Export custom policies
"""
def export_custom_policies():
    print('Exporting custom policies table data.')
    url = f"{api}/v1/policies/table/data"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get custom policies data.')
    with open('data/customPolicies.json', 'w') as cpfile:
        cpfile.write(json.dumps(result.json()))

"""
Export suppressions
"""
def export_suppressions():
    print('Exporting suppressions.')
    url = f"{api}/v1/suppressions"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get suppressions.')
    with open('data/suppressions.json', 'w') as supfile:
        supfile.write(json.dumps(result.json()))

"""
Export running configuration
"""
def export_run_configuration():
    print('Exporting running configuration')
    url = f"{api}/v1/checkov/runConfiguration?module=bc"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not get running configuration.')
    with open('data/runConfiguration.json', 'w') as supfile:
        supfile.write(json.dumps(result.json()))    

if __name__ == '__main__':
    print('Export BC data 0.0.1')
    export_repos()
    export_enforcement_rules()
    export_custom_policies()
    export_suppressions()
    print('Done')
