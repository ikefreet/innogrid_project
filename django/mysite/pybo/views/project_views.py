from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from ..forms import ProjectForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pymysql
from time import sleep
import jenkins
import requests
import json

host = "http://192.168.160.244:8080"
username = "admin" #jenkins username here
password = "admin" # Jenkins user password / api token here
server = jenkins.Jenkins(host, username=username, password=password)

argo_host = "http://argocd.xyz/"
admin = "admin"
request_url1 = """{}api/v1/session""".format(argo_host)
data1 = {'username':'admin','password':'python3.10'}
api_response = requests.post(request_url1, data=json.dumps(data1))
argocd_accesstoken = api_response.json()['token']

def project(request):
    project = Project.objects.all()
    if request.method == "POST":
        if Project.objects.filter(NAME=request.POST['NAME']):
            context = {'project': project, 'state' : '1 : 이미 존재하는 프로젝트명 입니다..'}
            return render(request, 'pybo/mainpage.html', context)
        if request.POST['KIND'] == 'Custom App':
            try:
                if "https://" and ".git" in request.POST['GIT']:
                    GITurl = requests.post(request.POST['GIT'])
                    Gitappurl = request.POST['GIT']
                    if GITurl.status_code // 100 != 2:
                        context = {'project': project, 'state' : 'Not 200'}
                        return render(request, 'pybo/mainpage.html', context) 
                else:
                    context = {'project': project, 'state' : '2 : 주소가 잘못 되었습니다.'}
                    return render(request, 'pybo/mainpage.html', context) 
            except:
                context = {'project': project, 'state' : '3 : 주소가 잘못 되었습니다.'}
                return render(request, 'pybo/mainpage.html', context) 
        if request.POST['KIND'] == 'GitHub App':
            # Git 레포 생성
            try:
                data = {
                    "name": "{}".format(request.POST['NAME']),
                    "description": "This Is Your First Repo",
                    "auto_init": True,
                }
                request_url = "https://api.github.com/user/repos"
                headers = {"Authorization": "Bearer {}".format(request.POST['GITTOKEN']), "Accept": "application/vnd.github+json"}
                api_response = requests.post(request_url, data=json.dumps(data), headers=headers)
                api_json = api_response.json()
                try:
                    error = api_json['errors'][0]['message']
                    context = {'project': project, 'state' : error}
                    return render(request, 'pybo/mainpage.html', context)
                except:
                    userid = api_json['owner']['login']
            except:
                context = {'project': project, 'state' : '4 : Git Hub Token이 잘못 되었습니다.'}
                return render(request, 'pybo/mainpage.html', context)

            Gitappurl = 'https://github.com/' + f'{userid}' + '/' f'{request.POST["NAME"]}' + '.git'

        # jenkins project 생성
        if request.POST['KIND'] != 'App' and request.POST['KIND'] != '0':
            init = open('./init_conf', 'r')
            f = init.read()
            if server.job_exists(request.POST["NAME"]) is not True:
                server.create_job(request.POST["NAME"], f)
                myConfig = server.get_job_config(request.POST["NAME"])
                # github 주소가 등록되어 있지 않으면
                if "<url>https://github.com/</url>" in myConfig:
                    new = myConfig.replace('<url>https://github.com/</url>', '<url>%s</url>' %(Gitappurl))
                    server.reconfig_job(request.POST["NAME"], new)
            init.close()

            # sonarqube token 생성
            request_url = "http://192.168.160.244:9000/api/user_tokens/generate"
            user = ("admin", "admin123")
            data = {"name": request.POST["NAME"]}
            api_response = requests.post(request_url, data=data, auth=user)
            api_json = api_response.json()
            print(api_json)
            sonar_token = api_json['token']

            # sonarqube project 생성
            request_url = "http://192.168.160.244:9000/api/projects/create"
            user = ("admin", "admin123")
            data = {
                "name": request.POST["NAME"],
                "project": request.POST["NAME"],
            }
            api_response = requests.post(request_url, data=data, auth=user)

        form = ProjectForm(request.POST)
        if form.is_valid():
            pj = form.save(commit=False)
            if request.POST['KIND'] == 'GitHub App':
                pj.GIT = Gitappurl
            if request.POST['KIND'] != 'App':
                pj.SONARTOKEN = sonar_token
            print(pj)
            pj.save()
            

            # ArgoCD Project 생성
            response = False

            try:              
                data = {
                    "project": {
                        "metadata": { 
                            "name": f"{request.POST['NAME']}" 
                        },
                        "spec": {
                            "destinations": [
                                {
                                "server": "https://kubernetes.default.svc",
                                "namespace": f"{request.POST['NAME']}"
                                }
                            ],
                            "clusterResourceWhitelist": [
                                {
                                    "group": "*",
                                    "kind": "*"
                                }
                            ],
                            "sourceRepos": ["*"]
                        }
                    }
                }
                request_url = """{}api/v1/projects""".format(argo_host)
                headers = {"Authorization": "Bearer {}".format(argocd_accesstoken)}
                api_response = requests.post(request_url, data=json.dumps(data), headers=headers)
                if api_response.ok:
                    response = True
                else:
                    print("api_response isn't ok")

                context = {'project' : project}
                return redirect('pybo:detail', project_id=pj.id)
            except Exception as e:
                print("try error")
                return redirect('pybo:index')
    else:
        form = ProjectForm()
    context = {'form' : form, 'state' : True}
    return render(request, 'pybo/project.html', context)


def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    print(project.NAME)
    if project.KIND == 'GitHub App':

        # Git hub userid 가져오기
        request_url = "https://api.github.com/user"
        headers = {"Accept": "application/vnd.github+json", "Authorization": "Bearer {}".format(project.GITTOKEN)}
        api_response = requests.get(request_url, headers=headers)
        api_json = api_response.json()
        userid = api_json['login']

        # Git hub 삭제
        request_url = "https://api.github.com/repos/{}/{}".format(userid, project.NAME)
        headers = {"Authorization": "Bearer {}".format(project.GITTOKEN), "Accept": "application/vnd.github+json"}
        api_response = requests.delete(request_url, headers=headers)
        print(api_response)
        
    # Jenkins Pipeline 삭제
    if server.job_exists(project.NAME):
        server.delete_job(project.NAME)

    if project.KIND != 'App':
        request_url = "http://192.168.160.244:9000/api/projects/delete"
        user = ("admin", "admin123")
        data = {"project": project.NAME}
        api_response = requests.post(request_url, data=data, auth=user)

        request_url = "http://192.168.160.244:9000/api/user_tokens/revoke"
        user = ("admin", "admin123")
        data = {"name": project.NAME}
        api_response = requests.post(request_url, data=data, auth=user)

    # ArgoCD Project 삭제
    argo_host = "http://argocd.xyz/"
    request_url = """{}api/v1/projects/{}""".format(argo_host, project.NAME)
    headers = {"Authorization": "Bearer {}".format(argocd_accesstoken)}
    api_response = requests.delete(request_url, headers=headers)
    print(api_response)
    
    return redirect('pybo:index')

