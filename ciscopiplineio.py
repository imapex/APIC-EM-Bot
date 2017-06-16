
# Welcome!  Ready to get going?  You can just hit save and 
# this code should work all by itself.  

# Want to learn more?  Well, here's the first thing to know: 

# YOU MUST define a function named 'spark_handler' or nothing will
# happen.  

# currently the default libraries are enabled as well:
# - requests==2.11.1
# - Flask==0.11.1
# - ciscosparkapi==0.3.1

# you can import another library here as well:
# we already import the following libs: 
#from flask import Flask, request
#from ciscosparkapi import CiscoSparkAPI
#import os
#import sys
#import json 
import requests
# here's code that will work right away and echo the comments of a 
# Step 1
# Change apic-em IP to the one you are using
#ip = "devnetapi.cisco.com/sandbox/apic_em"
ip = "devnetapi.cisco.com/sandbox/apic_em"

# Step 2
# Eneter user name and password to get a service ticket
# If you assign username, password and version here you don't need to pass parameter when calling
username = "devnetuser"
password = "Cisco123!"
version = "v1"
commands = """Hi my name is **APIC-EM BOT** and I am here to help. These are the current commands I know but I am getting smarter everyday. Don't forget if you add me to a group you must first mention me before sending any command for example @APIC_EM@sparkbot.io apic:help.

https://sandboxapic.cisco.com
username = devnetuser
password = Cisco123!
version = v1

##########################################
**Commands Available**
##########################################

1. **apic:device-list**	(list of network devices by device ID)
2. **apic:device-unreachable**		(list of uncreachable network devices)
3. **apic:device-detail-id __**		(I send all the details of the network device)
4. **apic:host-list**		(list of hosts)
5. **apic:host-detail ______**		(details of host by IP address)
6. **apic:host-count**		(count of all hosts)
7. **apic:feedback ______**		(Send me feedback)
"""
device = ""

# received message:
def spark_handler(post_data, message):
    # get the room id: 
    room_id = post_data["data"]["roomId"]
    person_Email = post_data["data"]["personEmail"]
    # we already include the ciscospark API
    # https://pypi.python.org/pypi/ciscosparkapi
    # and have already initialized the client for you.  You just
    # need to run it now.
    spark_msg = message.text
    if (spark_msg == "apic:host-count"):
        host = get_host_count()
        spark.messages.create(roomId=room_id, markdown="**Host count is:** " + host)
    elif (spark_msg == "apic:host-list"):
        host_list = get_host_list()
        spark.messages.create(roomId=room_id, markdown="**Host IP - Type - PoA**")
        spark.messages.create(roomId=room_id, text=host_list)
    elif (spark_msg.startswith ("apic:host-detail")):
        host = spark_msg.replace("apic:host-detail ", "")
        spark.messages.create(roomId=room_id, markdown="**Detail of host: **" + host)
        host_detail = get_host_detail(host)
        spark.messages.create(roomId=room_id, text=host_detail)
    elif (spark_msg == "apic:device-list"):
        device_list = get_network_device_list()
        spark.messages.create(roomId=room_id, markdown="**ID - Hostname - Location - Type**")
        spark.messages.create(roomId=room_id, text=device_list)
    elif (spark_msg.startswith ("apic:device-detail-id")):
        host = spark_msg.replace("apic:device-detail-id ", "")
        spark.messages.create(roomId=room_id, markdown="**Detail of device: **" + host)
        host_detail = get_network_device_id(host)
        spark.messages.create(roomId=room_id, text=host_detail)
    elif (spark_msg == "apic:device-unreachable"):
        device_status = get_network_device_status()
        spark.messages.create(roomId=room_id, markdown="**Device Status**")
        spark.messages.create(roomId=room_id, text=device_status)
    elif (spark_msg.startswith ("apic:feedback")):
        spark.messages.create(toPersonEmail="gsheppar@cisco.com", text=spark_msg + " from " + person_Email)
    elif (spark_msg == "apic:help"):
        spark.messages.create(roomId=room_id, markdown=commands)
    else:
        spark.messages.create(roomId=room_id, markdown="Sorry I did not understand that type **apic:help** to see a list of what I can do")

############################
# APIC-EM Tokens
############################

def get_X_auth_token(ip=ip,ver=version,uname=username,pword=password):
    """
    This function returns a new service ticket.
    Passing ip, version,username and password when use as standalone function
    to overwrite the configuration above.
    """

    # JSON input for the post ticket API request
    r_json = {
    "username": uname,
    "password": pword
    }
    # url for the post ticket API request
    post_url = "https://"+ip+"/api/"+ver+"/ticket"
    # All APIC-EM REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, data = json.dumps(r_json), headers=headers,verify=False)
        # remove '#' if need to print out response
        # print (r.text)

        # return service ticket
        return r.json()["response"]["serviceTicket"]
    except:
        # Something wrong, cannot get service ticket
        return ("Status: %s"%r.status_code)
        return ("Response: %s"%r.text)
        sys.exit ()

def get(ip=ip,ver=version,uname=username,pword=password,api='',params=''):
    """
    To simplify requests.get with default configuration.Return is the same as requests.get
    """
    ticket = get_X_auth_token()
    headers = {"X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting GET '%s'\n"%url)
    try:
    # The request and response of "GET /network-device" API
        resp= requests.get(url,headers=headers,params=params,verify = False)
        return(resp)
    except:
       return ("Something wrong to GET /",api)
       sys.exit()

def post(ip=ip,ver=version,uname=username,pword=password,api='',data=''):
    """
    To simplify requests.post with default configuration.Return is the same as requests.post
    """
    ticket = get_X_auth_token()
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting POST '%s'\n"%url)
    try:
    # The request and response of "POST /network-device" API
        resp= requests.post(url,json.dumps(data),headers=headers,verify = False)
        return(resp)
    except:
       return ("Something wrong to POST /",api)
       sys.exit()

def put(ip=ip,ver=version,uname=username,pword=password,api='',data=''):
    """
    To simplify requests.put with default configuration.Return is the same as requests.put
    """
    ticket = get_X_auth_token()
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting PUT '%s'\n"%url)
    try:
    # The request and response of "PUT /network-device" API
        resp= requests.put(url,json.dumps(data),headers=headers,verify = False)
        return(resp)
    except:
       return ("Something wrong to PUT /",api)
       sys.exit()

def delete(ip=ip,ver=version,uname=username,pword=password,api='',params=''):
    """
    To simplify requests.delete with default configuration.Return is the same as requests.delete
    """
    ticket = get_X_auth_token()
    headers = {"X-Auth-Token": ticket,'content-type': 'application/json'}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting DELETE '%s'\n"%url)
    try:
    # The request and response of "DELETE /network-device" API
        resp= requests.delete(url,headers=headers,params=params,verify = False)
        return(resp)
    except:
       return ("Something wrong to DELETE /",api)
       sys.exit()

############################
# APIC-EM Get Hosts
############################
def get_host_count():
    resp = get(api="host/count")
    response_json = resp.json() # Get the json-encoded content from response
    count = response_json['response']
    reply_count = json.dumps(count)
    return(reply_count)

def get_host_list():
    resp = get(api="host")
    response_json = resp.json() # Get the json-encoded content from response
    host_list=[]
#    host_list = (json.dumps(response_json,indent=4))
    for item in response_json["response"]:
        host_list.append([item["hostIp"],item["hostType"],item["connectedNetworkDeviceIpAddress"]])
    host_list_print = "\n".join(str(x) for x in host_list)
    host_list_print = host_list_print.replace("u'", "'")
    host_list_print = host_list_print.replace("[", "")
    host_list_print = host_list_print.replace("]", "")
    host_list_print = host_list_print.replace("'", "")
    return(host_list_print)

def get_host_detail(device):
    resp = get(api="host")
    response_json = resp.json() # Get the json-encoded content from response
    for item in response_json["response"]:
        if item["hostIp"] == device and item["hostType"] == "wired":
            host_detail = "hostIp: " + item["hostIp"] + "\n"
            host_detail += "connectedNetworkDeviceId: " + item["connectedNetworkDeviceId"] + "\n"
            host_detail += "connectedInterfaceId: " + item["connectedInterfaceId"] + "\n"
            host_detail += "connectedInterfaceName: " + item["connectedInterfaceName"] + "\n"
            host_detail += "id: " + item["id"] + "\n"
            host_detail += "lastUpdated: " + item["lastUpdated"] + "\n"
            host_detail += "hostType: " + item["hostType"] + "\n"
            host_detail += "connectedNetworkDeviceIpAddress: " + item["connectedNetworkDeviceIpAddress"] + "\n"
            host_detail += "vlanId: " + item["vlanId"] + "\n"
            host_detail += "hostMac: " + item["hostMac"]
            host_detail = host_detail.replace("\"", "")
            return host_detail
    for item in response_json["response"]:
        if item["hostIp"] == device and item["hostType"] == "wireless":
            host_detail = "hostIp: " + item["hostIp"] + "\n"
            host_detail += "connectedAPName: " + item["connectedAPName"] + "\n"
            host_detail += "pointOfPresence: " + item["pointOfPresence"] + "\n"
            host_detail += "pointOfAttachment: " + item["pointOfAttachment"] + "\n"
            host_detail += "connectedAPMacAddress: " + item["connectedAPMacAddress"] + "\n"
            host_detail += "id: " + item["id"] + "\n"
            host_detail += "lastUpdated: " + item["lastUpdated"] + "\n"
            host_detail += "hostType: " + item["hostType"] + "\n"
            host_detail += "vlanId: " + item["vlanId"] + "\n"
            host_detail += "connectedNetworkDeviceId: " + item["connectedNetworkDeviceId"] + "\n"
            host_detail += "hostMac: " + item["hostMac"]
            host_detail = host_detail.replace("\"", "")
            return host_detail
def get_network_device_list():
    resp = get(api="network-device")
    status = resp.status_code
    # Get the json-encoded content from response
    response_json = resp.json()
    # all network-device detail is in "response"
    device = response_json["response"]
    device_list = []
    device_show_list = []
    for i, item in enumerate(device):
        device_list.append([item["hostname"],item["locationName"],item["type"],item["instanceUuid"]])
        #Not showing id to user, it's just a hex string
        device_show_list.append([i+1,item["hostname"],item["locationName"],item["type"]])
    network_list_print = "\n".join(str(x) for x in device_show_list)
    network_list_print = network_list_print.replace("u'", "'")
    network_list_print = network_list_print.replace("[", "")
    network_list_print = network_list_print.replace("]", "")
    network_list_print = network_list_print.replace("'", "")
    return(network_list_print)

def get_network_device_status():
    resp = get(api="network-device")
    status = resp.status_code
    # Get the json-encoded content from response
    response_json = resp.json()
    # all network-device detail is in "response"
    device = response_json["response"]
    device_list = []
    device_show_list = []
    for i, item in enumerate(device):
        if (item["reachabilityStatus"] == "reachable"):
            device_list.append([item["hostname"],item["locationName"],item["type"],item["instanceUuid"]])
            #Not showing id to user, it's just a hex string
            device_show_list.append([i+1,item["hostname"],item["locationName"],item["reachabilityFailureReason"]])
    if not device_show_list:
        device_status = "All devices are reachable!!!"
        return (device_status)
    else:
        network_status_print1 = "Number - Hostname - Location - Failure Reason \n"
        network_status_print2 = "\n".join(str(x) for x in device_show_list)
        network_status_print2 = network_status_print2.replace("u'", "'")
        network_status_print = network_status_print1 + network_status_print2
        return (network_status_print)

def get_network_device_id(user_input):
    resp = get(api="network-device")
    status = resp.status_code
    # Get the json-encoded content from response
    response_json = resp.json()
    # all network-device detail is in "response"
    device = response_json["response"]
    device_list = []
    device_show_list = []
    id = ""
    device_id_idx = 3
    device_ip_idx = 1
    for i, item in enumerate(device):
    	device_list.append([item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
    	#Not showing id to user, it's just a hex string
    	device_show_list.append([i+1,item["hostname"],item["managementIpAddress"],item["type"]])
    if user_input.lower() == 'exit': 
    	sys.exit()
    if user_input.isdigit():
    	if int(user_input) in range(1,len(device_show_list)+1):
    		id = device_list[int(user_input)-1][device_id_idx]
    		name_ip = device_list[int(user_input)-1][device_ip_idx]
    	else:
    		print ("Oops! number is out of range, please try again or enter 'exit'")
    		sys.exit()
    else:
    	print ("Oops! input is not a digit, please try again or enter 'exit'")
    	sys.exit()
    resp = get(api="network-device/ip-address/"+name_ip)
    status = resp.status_code
    response_json = resp.json()
    host_detail = json.dumps(response_json["response"], indent=4, sort_keys=True)
    host_detail = host_detail.replace("}", "")
    host_detail = host_detail.replace("{", "")
    host_detail = host_detail.replace("\"", "")
    return host_detail