import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1TYnB6THpzRnJMWTZGN3NZOHRsVjBMY1l4aFE0WWZOV3BLTnFMcDcxcTgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNXA1Z3EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImYwZDgxN2MzLWZhNDUtNGVlNy1iMmU3LTg1YTM2NTliNWE5OCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.J8cDAoqSEO1hlLtf58AC-aV-w0CMQA9oxNFm1KZp5B-p6fGJqCluv6EiOVcZaGklzr4nbrvgzWJVItUv3MrougFnTIX_JT82LKHD2BHY9tyWKLgUrjot69QM07jEnBykmzAi87WoUqzYcA14xFFHI48HJDaanFTzgt-1d_kwT2Em74DYWQXNU-Pz-zuOW-Vct9zv8squOiyTeTpiN3q2-Np7TVnarJXaBxqVWV79y5Ou6RA_ku83P6bMWeUK1lSj2hkL-mdhD4uj9RA70LAt21Y8KMVL8KNgfNeZKLhNE4q3bTnm0-H549wXImnY6fFfWm4L-JlJABimty-hh6SVGQ"

request_url = "https://10.0.0.79:6443/api/v1/namespaces/monitor/pods/"
headers = {"Authorization": "Bearer {}".format(token)}
api_response = requests.get(request_url, headers=headers, verify=False)
api_json = api_response.json()
number = 0
pod_items = api_json['items']
pod_dict = {}

for pod_item in pod_items:
    pods = []
    container_list = []
    num = 0
    pods.append(pod_item['metadata']['name'])
    pods.append(pod_item['metadata']['creationTimestamp'])
    pods.append(pod_item['metadata']['ownerReferences'][0]['kind'])
    pods.append(pod_item['spec']['nodeName'])
    pods.append(pod_item['status']['phase'])
    for pod_status in pod_item['status']['conditions']:
        # pods.append(pod_status['type'])
        pods.append(pod_status['status'])
    for pod_condition in pod_item['status']['containerStatuses']:
        pods.append(pod_condition['state'])
    
    for pod_container in pod_item['spec']['containers']:

        container = []
        container.append(pod_container['name'])
        container.append(pod_container['image'])
        try:
            container.append(pod_container['ports'][0])
        except:
            container.append({'containerPort': 'None', 'protocol': 'None'})
        container_list.append(container)
        num += 1
    pod_dict['container_{}'.format(number)] = container_list
    pod_dict['pod_{}'.format(number)] = pods
    number += 1
print(pod_dict[0])