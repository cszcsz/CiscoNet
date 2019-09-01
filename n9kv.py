from flask import Flask, request
import requests
import json
from flask_cors import *
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, ContextData, ObjectIdentity, ObjectType

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


@app.route('/')
def index():
    return 'index page'


@app.route('/peizhi', methods=['POST', 'OPTIONS'])
def peizhi():
    data = request.json
    hostname = ""
    interface = ""
    status = ""
    ipv4 = ""
    ipv6 = ""
    vlan = ""
    try:
        print(data)
        hostname = data['hostname']
        interface = data['interface']
        status = data['status']
        print(hostname + " " + interface + " " + status + " " + ipv4 + " " + ipv6 + " " + vlan)

        # hostname非空则执配置主机名
        if hostname != "":
            send_command('hostname ' + hostname)
        if interface != "":
            cmd2 = ""
            if status == "up":
                cmd2 = "no shutdown"
            if status == "down":
                cmd2 = "shutdown"
            send_command_complex(interface  , cmd2)
    except:
        print("有异常")
    res = {
        "status": "OK"
    }
    return json.dumps(res)


@app.route('/show', methods=['POST'])
def show():
    data = request.json
    command = ""
    try:
        if data:
            command = data
            print(command)
    except:
        print("有异常")
    res = send_command(command)
    return json.dumps(res)


@app.route('/m0')
def get_m0():
    switchuser = 'admin'
    switchpassword = 'eve'
    url = 'http://180.201.158.167:8080/ins'
    myheaders = {'content-type': 'application/json-rpc'}
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "show int m0",
                "version": 1
            },
            "id": 1
        }
    ]
    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()
    response = response['result']['body']['TABLE_interface']['ROW_interface']
    list = {}
    list.update({'vdc_lvl_in_bytes': float(response['vdc_lvl_in_bytes']) / 1024})
    list.update({'vdc_lvl_out_bytes': float(response['vdc_lvl_out_bytes']) / 1024})
    return json.dumps(list)


@app.route('/showr/<number>')
def showr(number):
    '''
    data = request.json
    command = ""
    try:
        if data:
            command = data
            print(command)
    except:
        print("有异常")
    res = send_command(command)
    return json.dumps(res)
    '''
    if(number=='R2'):
        portnumber=8092
    elif(number=='R1'):
        portnumber=8090
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', portnumber)),
               ContextData(),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 1)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 2)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 3)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 4)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 5)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 1)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 2)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 3)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 4)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 5)))
    )
    list = {}
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        sumin = 0.0
        sumout = 0.0
        for varBind in varBinds:
            temp = (str(varBind)).split('=')
            if temp[0].strip()[10] == 'I':
                sumin = sumin + float(temp[1].strip()) / 1024
            elif temp[0].strip()[10] == 'O':
                sumout = sumout + float(temp[1].strip()) / 1024
            # list.update({temp1:float(temp[1].strip())/1024})
        list.update({'sumin': sumin})
        list.update({'sumout': sumout})
    return json.dumps(list)


@app.route('/showPType/<number>')
def showPacketType(number):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', number)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.3.0')),  # ipin
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.10.0')),  # ipout
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.5.1.0')),  # icmpin
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.5.14.0')),  # icmpout
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.6.10.0')),  # tcpin
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.6.11.0')),  # tcpout
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.7.1.0')),  # udpin
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.7.4.0')),  # udpout
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.1.0')),  # snmpin
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.2.0')))  # snmpout
    )
    list1 = {}
    list2 = {}
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        sumin = 0.0
        sumout = 0.0
        t = 0
        for varBind in varBinds:
            temp = (str(varBind)).split('=')
            if t == 0:
                list1.update({'ipin': float(temp[1].strip())})
            elif t == 1:
                list2.update({'ipout': float(temp[1].strip())})
            elif t == 2:
                list1.update({'icmpin': float(temp[1].strip())})
            elif t == 3:
                list2.update({'icmpout': float(temp[1].strip())})
            elif t == 4:
                list1.update({'tcpin': float(temp[1].strip())})
            elif t == 5:
                list2.update({'tcpout': float(temp[1].strip())})
            elif t == 6:
                list1.update({'udpin': float(temp[1].strip())})
            elif t == 7:
                list2.update({'udpout': float(temp[1].strip())})
            elif t == 8:
                list1.update({'snmpin': float(temp[1].strip())})
            elif t == 9:
                list2.update({'snmpout': float(temp[1].strip())})
            '''
            if temp[0].strip()[10]=='I':
                sumin=sumin+float(temp[1].strip())/1024
            elif temp[0].strip()[10]=='O':
                sumout=sumout+float(temp[1].strip())/1024
            '''
            t = t + 1
            # list.update({temp1:float(temp[1].strip())/1024})
            mylist = {"in" : list1, "out" : list2}
    return json.dumps(mylist)

def send_command(cmd):
    print("exe "+cmd+" ...")
    switchuser = 'admin'
    switchpassword = 'eve'
    url = 'http://180.201.158.167:8080/ins'
    myheaders = {'content-type': 'application/json-rpc'}
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": cmd,
                "version": 1
            },
            "id": 1
        }
    ]
    return requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()


def send_command_complex(cmd1, cmd2):
    print("exe "+cmd1+" ....and "+cmd2+" ....")
    switchuser = 'admin'
    switchpassword = 'eve'
    url = 'http://180.201.158.167:8080/ins'
    myheaders = {'content-type': 'application/json-rpc'}
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": cmd1,
                "version": 1
            },
            "id": 1
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": cmd2,
                "version": 1
            },
            "id": 1
        }
    ]
    return requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser, switchpassword)).json()


@app.route('/getDeviceInfo')
def getDeviceInfo():
    DeviceList = list()
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', 8090)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
               )
    )

    if errorIndication is None:
        routerName = varBinds[0][1].prettyPrint()
        jsonData = {"dName": routerName}
        DeviceList.append(jsonData)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', 8092)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
               )
    )

    if errorIndication is None:
        routerName = varBinds[0][1].prettyPrint()
        jsonData = {"dName": routerName}
        DeviceList.append(jsonData)

    return json.dumps(DeviceList, indent=4, separators=(',', ': '))



preInRecv = 0
preInDiscard = 0
preOutReq = 0
preOutDiscard = 0
delta = 0.1
def getPacketException(ExceptionList):

    global preOutDiscard,preOutReq,preInDiscard,preInRecv

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', 8090)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.3.0')),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.8.0')),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.10.0')),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.11.0'))
               )
    )
    if errorIndication is None:
        curInRecv = int(varBinds[0][1].prettyPrint())
        curInDiscard  = int(varBinds[1][1].prettyPrint())
        curOutReq  = int(varBinds[2][1].prettyPrint())
        curOutDiscard  = int(varBinds[3][1].prettyPrint())

        if (curInDiscard-preInDiscard)/(curInRecv-preInRecv) > delta:
            jsonData = {"excType": "packetExc", "excContent": "input packet loss too big"}
            ExceptionList.append(jsonData)
        if (curOutDiscard-preOutDiscard)/(curOutReq-preOutReq) > delta:
            jsonData = {"excType": "packetExc", "excContent": "output packet loss too big"}
            ExceptionList.append(jsonData)

        preInRecv = curInRecv
        preInDiscard = curInDiscard
        preOutReq = curOutReq
        preOutDiscard = curOutDiscard

    return ExceptionList


@app.route('/getException')
def getException():
    excList = list()
    excList = getPortException(excList)
    excList = getPacketException(excList)
    jsonD = json.dumps(excList, indent=4, separators=(',', ': '))
    print(jsonD)
    return jsonD


def getPortException(ExceptionList):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', 8090)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
               )
    )

    if errorIndication:
        jsonData = {"excType": "deviceExc", "excContent": "R1 response timeout"}
        ExceptionList.append(jsonData)

    else:
        for i in range(1, 6):
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData('campus', mpModel=1),
                       UdpTransportTarget(('180.201.158.167', 8090)),
                       ContextData(),
                       ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
                       ObjectType(ObjectIdentity('IF-MIB', 'ifDescr', i)),
                       ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', i))
                       )
            )

            if varBinds[2][1].prettyPrint() == "down":
                routerName = varBinds[0][1].prettyPrint()
                intName = varBinds[1][1].prettyPrint()
                jsonData = {"excType": "portExc", "excContent": routerName + " int " + intName + " : down"}
                ExceptionList.append(jsonData)



    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('campus', mpModel=1),
               UdpTransportTarget(('180.201.158.167', 8092)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
               )
    )

    if errorIndication:
        jsonData = {"excType": "deviceExc", "excContent": "R2 response timeout"}
        ExceptionList.append(jsonData)
    else:
        for i in range(1, 6):
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData('campus', mpModel=1),
                       UdpTransportTarget(('180.201.158.167', 8092)),
                       ContextData(),
                       ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')),
                       ObjectType(ObjectIdentity('IF-MIB', 'ifDescr', i)),
                       ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', i))
                       )
            )
            if varBinds[2][1].prettyPrint() == "down":
                routerName = varBinds[0][1].prettyPrint()
                intName = varBinds[1][1].prettyPrint()
                jsonData = {"excType": "portExc",
                            "excContent": routerName + " int " + intName + " : down"}
                ExceptionList.append(jsonData)



    return ExceptionList


def printInfo(errorIndication, errorStatus, errorIndex, varBinds):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))






if __name__ == '__main__':
    app.run(debug=True)
