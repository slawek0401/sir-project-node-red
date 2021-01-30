import wiotp.sdk.device
import time

import config
import dataHandler

devices = ["SIR_device01", "SIR_device02"]

data = {
    "SIR_device01" : [],
    "SIR_device02" : []
}

def clientEventCallback(event):
    print("Client Event received for %s:%s: %s" % (event.typeId, event.deviceId, event.data))
    singleData = dataHandler.dataObject(event.data)
    global data
    data[singleData.device].append(singleData)

if __name__ == "__main__":
    client = wiotp.sdk.application.ApplicationClient(config=config.getConfig(), logHandlers=None)
    client.connect()
    client.deviceEventCallback = clientEventCallback
    eventsMid = client.subscribeToDeviceEvents("+", "+", "+")

    while len(data["SIR_device01"]) < 31 or len(data["SIR_device02"]) < 31:
        time.sleep(2)
    dataHandler.printData(data, devices)
    dataHandler.bokehShow(data, devices)
    client.disconnect()
