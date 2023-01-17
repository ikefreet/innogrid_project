import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


request_url = "https://10.0.0.79:6443/api/v1/namespaces/argocd/pods/"
headers = { "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1TYnB6THpzRnJMWTZGN3NZOHRsVjBMY1l4aFE0WWZOV3BLTnFMcDcxcTgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNXA1Z3EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImYwZDgxN2MzLWZhNDUtNGVlNy1iMmU3LTg1YTM2NTliNWE5OCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.J8cDAoqSEO1hlLtf58AC-aV-w0CMQA9oxNFm1KZp5B-p6fGJqCluv6EiOVcZaGklzr4nbrvgzWJVItUv3MrougFnTIX_JT82LKHD2BHY9tyWKLgUrjot69QM07jEnBykmzAi87WoUqzYcA14xFFHI48HJDaanFTzgt-1d_kwT2Em74DYWQXNU-Pz-zuOW-Vct9zv8squOiyTeTpiN3q2-Np7TVnarJXaBxqVWV79y5Ou6RA_ku83P6bMWeUK1lSj2hkL-mdhD4uj9RA70LAt21Y8KMVL8KNgfNeZKLhNE4q3bTnm0-H549wXImnY6fFfWm4L-JlJABimty-hh6SVGQ" }
api_response = requests.get(request_url, headers=headers, verify=False)
api_json = api_response.json()
api_items = api_json['items']
for api_item in api_items:
    print(api_item['metadata']['name'])
    print(api_item['metadata']['creationTimestamp'])
    print(api_item['metadata']['ownerReferences'][0]['kind'])
    for api_container in api_item['spec']['containers']:
        print(api_container['name'])
        print(api_container['image'])
        try:
            print(api_container['ports'][0])
        except:
            ...
    print(api_item['spec']['nodeName'])
    print(api_item['status']['phase'])
    for api_status in api_item['status']['conditions']:
        print(api_status['type'])
        print(api_status['status'])
    for api_condition in api_item['status']['containerStatuses']:
        print(api_condition['name'])   # 중복
        print(api_condition['state'])

request_url = "https://10.0.0.79:6443/api/v1/namespaces/argocd/services/"
headers = { "Authorization": "Bearer token" }
api_response = requests.get(request_url, headers=headers, verify=False)
api_json = api_response.json()
print(api_json)
api_items = api_json['items']
for api_item in api_items:
    print(api_item['metadata']['name'])
    print(api_item['metadata']['creationTimestamp'])
    for item_ports in api_item['spec']['ports']:
        print(item_ports)
    print(api_item['spec']['type'])
    print(api_item['status']['loadBalancer'])