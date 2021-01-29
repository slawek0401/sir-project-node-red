import wiotp.sdk.device
import time

import config
import dataHandler

data = {
    "SIR_device01" : [],
    "SIR_device02" : []
}

# def clientCommandCallback(cmd):
#     print("Client Command received for %s:%s: %s" % (cmd.typeId, cmd.deviceId, cmd.data))

def clientEventCallback(event):
    print("Client Event received for %s:%s: %s" % (event.typeId, event.deviceId, event.data))
    singleData = dataHandler.dataObject(event.data)
    global data
    data[singleData.device].append(singleData)


# def clientSubscribeCallback(a, b):
#     print("Client Subscribe received %s:%s" % (a, b))

def nic():
    a = 1+2

if __name__ == "__main__":
    d1 = {'d': {'timestamp': 1611878326773, 'temperature': {'inside': '22.89', 'outside': '7.23'}, 'air_pressure': '1015', 'humidity': '38.90', 'deviceId': 'SIR_device01'}}
    d2 = {'d': {'timestamp': 1611878346773, 'temperature': {'inside': '26.92', 'outside': '9.36'}, 'air_pressure': '1019', 'humidity': '38.15', 'deviceId': 'SIR_device02'}}
    d3 = {'d': {'timestamp': 1611878366778, 'temperature': {'inside': '24.32', 'outside': '7.69'}, 'air_pressure': '1012', 'humidity': '38.27', 'deviceId': 'SIR_device01'}}
    d4 = {'d': {'timestamp': 1611878386778, 'temperature': {'inside': '22.42', 'outside': '8.53'}, 'air_pressure': '1013', 'humidity': '38.64', 'deviceId': 'SIR_device02'}}
    ddd = [d1,d2,d3,d4]
    data
    for i in ddd:
        singleData = dataHandler.dataObject(i)
        data[singleData.device].append(singleData)

    dataHandler.printData(data)

if __name__ == "__main123123__":
    client = wiotp.sdk.application.ApplicationClient(config=config.getConfig(), logHandlers=None)
    client.connect()
    client.deviceEventCallback = clientEventCallback
    #client.deviceCommandCallback = clientCommandCallback
    #client.subscriptionCallback = clientSubscribeCallback

    #statusMid = client.subscribeToDeviceStatus("+", "+")
    eventsMid = client.subscribeToDeviceEvents("+", "+", "+")

    #while len(data["SIR_device01"]) < 31 and len(data["SIR_device02"]) < 31:
    while len(data["SIR_device01"]) < 2 or len(data["SIR_device02"]) < 2: #debug only
        time.sleep(2)
    dataHandler.printData(data)
    client.disconnect()
