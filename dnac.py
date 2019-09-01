from flask import Flask, request
import requests
import json
from flask_cors import *

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/')
def helloWorld():
    return "Hello World!"


@app.route('/get_token')
def get_token():
    user_name = "devnetuser"
    pwd = "Cisco123!"
    url = "https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(user_name, pwd)).json()
    token = ""
    if(response):
        token = response['Token']
    return token


@app.route('/getDeviceFromDNAC')
def getDeviceFromDNAC():
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device"
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    response = response['response']
    print(response[0]['type'])
    my_id = 1
    result = []
    for item in response:
        dic = {}
        dic['id'] = my_id
        dic['hostname'] = item['hostname']
        dic['type'] = item['type']
        dic['ip'] = item['managementIpAddress']
        dic['time'] = item['lastUpdated']
        my_id = my_id+1
        result.append(dic)
    return json.dumps(result)

@app.route('/get_device_health')
def get_device_health():
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-health"
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    return json.dumps(response)

@app.route('/setup_proxy')
def setup_proxy():
    token = get_token()
    try:
        proxy_object = {
            "enableProxy" : "true",
            # "httpProxyHost" : "192.168.31.197",
            # "httpsProxyHost" : "192.168.31.197",
            # "httpProxyPort" : 5005,
            # "httpsProxyPort" : 5005,
            "httpNonProxyHosts" : "*.svc.cluster.local|<fqdnOrIpOfDNACHost>"
        }

        header_object = {
            "X-Auth-Token": token,
            "Content-type": "application/json",
        }

        response = requests.post(
            "https://sandboxdnac2.cisco.com/api/dnacaap/v1/dnacaap/management/proxysettings",
            data=json.dumps(proxy_object),
            headers=header_object,
            verify=False,
        ).json()
        # print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)