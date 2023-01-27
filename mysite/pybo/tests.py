import requests
import json
request_url = "https://api.github.com/repos/sjin110550/DevSecOpsToolChain/vulnerability-alerts"
headers = {"Authorization": "Bearer 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", "Accept": "application/vnd.github+json"}
api_response = requests.put(request_url, headers=headers)
print(api_response)





'''curl \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/vulnerability-alerts'''