#import wiotp.sdk.client
import wiotp.sdk.device
from datetime import datetime

dateReceived = 0

def clientCommandCallback(cmd):
    print("Client Command received for %s:%s: %s" % (cmd.typeId, cmd.deviceId, cmd.data))

def clientEventCallback(event):
    print("Client Event received for %s:%s: %s" % (event.typeId, event.deviceId, event.data))
    print(event.data['d']['timestamp'])
    date = datetime.fromtimestamp(event.data['d']['timestamp']/1000)
    print(date)
    print(event.data['d']['temperature']['inside'])
    print(event.data['d']['temperature']['outside'])
    print(event.data['d']['air_pressure'])
    print(event.data['d']['humidity'])
    global dateReceived
    dateReceived = dateReceived + 1

def clientSubscribeCallback(a, b):
    print("Client Subscribe received %s:%s" % (a, b))

def nic():
    a = 1+2

if __name__ == "__main__":
    myConfig = {
    "identity": {
        "appId": "app1"
    },
    "auth": {
        "key": "a-tjxc7u-v5eknhvxss",
        "token": "cFz&aHU6i)FF5)Rljk"
    },
    "mqtt" :{
        "cleanStart": True,
        "sessionExpiry": 3600,
        "keepAlive": 100
    }
    }

    client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
    client.connect()
    client.deviceEventCallback = clientEventCallback
    client.deviceCommandCallback = clientCommandCallback
    client.subscriptionCallback = clientSubscribeCallback

    statusMid = client.subscribeToDeviceStatus("+", "+")
    eventsMid = client.subscribeToDeviceEvents("+", "+", "+")

    while dateReceived < 2:
        pass

    client.disconnect()