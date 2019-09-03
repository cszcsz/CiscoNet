from flask import Flask, request
import requests
import json
from flask_cors import *
import http.client

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/')
def helloWorld():
    return "Hello World!"

# 获取token
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

# 获取设备表头信息
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
        dic['family'] = item['family']
        dic['type'] = item['type']
        dic['ip'] = item['managementIpAddress']
        dic['time'] = item['lastUpdated']
        dic['role'] = item['role']
        dic['stat'] = item['reachabilityStatus']
        dic['uuid'] = item['id']
        dic['mac'] = item['macAddress']
        dic['hostname'] = item['hostname']
        dic['softwareType'] = item['softwareType']
        dic['softwareVersion'] = item['softwareVersion']
        dic['lastUpdated'] = item['lastUpdated']
        dic['serialNumber'] = item['serialNumber']
        dic['family'] = item['family']
        dic['memorySize'] = item['memorySize']
        my_id = my_id+1
        result.append(dic)
    return json.dumps(result)

# 获取设备详细信息
@app.route('/get_device_detail')
def get_device_detail():
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device"
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    response = response['response']
    print(response[0]['type'])

    return json.dumps(response)


# 获取设备接口信息
@app.route('/get_device_interface/<uuid>')
def get_device_interface(uuid):
    print(uuid)
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/interface/network-device/"+uuid
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    response = response['response']
    my_id = 1
    result = []
    for item in response:
        dic = {}
        dic['id'] = my_id
        dic['interfaceName'] = item['portName']
        dic['macAddress'] = item['macAddress']
        dic['mode'] = item['portMode']
        dic['status'] = item['status']
        my_id = my_id + 1
        result.append(dic)
    return json.dumps(result)


# 获取设备健康信息
@app.route('/get_device_health')
def get_device_health():
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-health"
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    return json.dumps(response)






@app.route('/discoveryTopo')
def discoveryTopo():
    linklist = []
    index1 = {}
    index2 = {}
    linklistf = []
    locatelist = {}
    listfinal = {}
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/topology/physical-topology"
    token = get_token()
    my_header = {'X-Auth-Token': token}
    response = requests.get(url, headers=my_header).json()
    link = response['response']['links']
    node = response['response']['nodes']
    for i in link:
        temp = []
        temp.append(i['source'])
        temp.append(i['target'])
        linklist.append(temp)
    wifi = 0
    for i in node:
        if (i['deviceType'] == 'Cisco 1140 Unified Access Point'):
            wifi = wifi + 1
        if (i['deviceType'] != 'wireless' and i['deviceType'] != 'wired'):
            index1.update({i['label']: i['deviceType']})
            index2.update({i['id']: i['label']})
    for i in linklist:
        temp = []
        if (i[0] in index2 and i[1] in index2):
            temp.append(index2[i[0]])
            temp.append(index2[i[1]])
            linklistf.append(temp)
    print(wifi)
    for i in linklistf:
        if (index1[i[1]] == 'cloud node'):
            t = i[0]
            i[0] = i[1]
            i[1] = t
        elif (index1[i[1]] == 'Cisco Catalyst38xx stack-able ethernet switch' and index1[i[0]] != 'cloud node'):
            t = i[0]
            i[0] = i[1]
            i[1] = t
        elif (index1[i[1]] == 'Cisco Catalyst 9300 Switch' and index1[i[0]] != 'cloud node' and index1[
            i[0]] != 'Cisco Catalyst38xx stack-able ethernet switch'):
            t = i[0]
            i[0] = i[1]
            i[1] = t
    for i in range(len(linklistf) - 1):
        for j in range(i + 1, len(linklistf)):
            if (index1[linklistf[i][0]] == 'cloud node'):
                continue
            elif (index1[linklistf[i][0]] == 'Cisco Catalyst38xx stack-able ethernet switch' and index1[
                linklistf[j][0]] == 'Cisco Catalyst 9300 Switch'):
                continue
            elif (index1[linklistf[i][0]] == 'Cisco Catalyst38xx stack-able ethernet switch' and index1[
                linklistf[j][0]] == 'Cisco 3504 Wireless LAN Controller'):
                continue
            elif (index1[linklistf[i][0]] == 'Cisco Catalyst 9300 Switch' and index1[
                linklistf[j][0]] == 'Cisco 3504 Wireless LAN Controller'):
                continue
            else:
                t = linklistf[i]
                linklistf[i] = linklistf[j]
                linklistf[j] = t
    for i in linklistf:
        listfinal.update({i[0]: []})
        listfinal.update({i[1]: []})
        locatelist.update({i[0]: []})
        locatelist.update({i[1]: []})
    for i in linklistf:
        listfinal[i[0]].append(i[1])
    x = 50
    y = 50
    start = 'cloud node'
    locatelist['cloud node'].append(x)
    locatelist['cloud node'].append(y)
    locate(listfinal, start,locatelist)
    result = []
    for item, value in locatelist.items():
        temp = []
        temp.append(item)
        temp.append(index1[item])
        temp.append(value[0])
        temp.append(value[1])
        result.append(temp)
    # finalResult={}
    # finalResult['nodeInfo']=result
    # finalResult['edge']=listfinal
    my_map = {}
    nodes = []
    links = []
    my_id = 0
    for item in result:
        node = {}
        node['id'] = my_id
        if my_id==0:
            node['x'] = item[2]
            node['y'] = 600 - item[3]-200
        elif my_id==1:
            node['x'] = item[2]
            node['y'] = 600 - item[3]-100
        elif my_id==2:
            node['x'] = item[2]-200
            node['y'] = 600 - item[3]
        elif my_id==3:
            node['x'] = item[2]+200
            node['y'] = 600 - item[3]
        elif my_id==4:
            node['x'] = item[2]+200
            node['y'] = 600 - item[3]+170
        node['name'] = item[0]
        my_map[item[0]] = my_id
        my_id = my_id + 1
        nodes.append(node)

    for item in nodes:
        hostname = item['name']
        tempList = listfinal[hostname]
        if len(tempList) > 0:
            for tmp in tempList:
                edge = {}
                edge['source'] = my_map[hostname]
                edge['target'] = my_map[tmp]
                links.append(edge)

    # 最后再单独添加无线接入点
    wifiPoint = {}
    wifiPoint['id'] = 5
    wifiPoint['x'] = 140
    wifiPoint['y'] = 860
    wifiPoint['name'] = "Unified AP"
    nodes.append(wifiPoint)



    topologyData = {}
    topologyData['nodes'] = nodes
    topologyData['links'] = links

    return json.dumps(topologyData)


def locate(listfinal,start,locatelist):
    x=locatelist[start][0]
    y=locatelist[start][1]
    number=0
    for i in listfinal[start]:
        number=number+1
    if(number%2==0):
        x=x-(number/2-1)*8-4
    else:
        x=x-(number-1)/2*8
    y=y-10
    for i in listfinal[start]:
        locatelist[i].append(x)
        locatelist[i].append(y)
        locate(listfinal,i,locatelist)
        x=x+8


# 此接口为设置webhook代理接口
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