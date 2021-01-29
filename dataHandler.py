from datetime import datetime
from tabulate import tabulate
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.layouts import gridplot

class dataObject:
    def __init__(self, timestamp_, temperature_inside_, temperature_outside_, air_pressure_, humidity_, device_):
        self.timestamp = timestamp_
        self.temperature_inside = temperature_inside_
        self.temperature_outside = temperature_outside_
        self.air_pressure = air_pressure_
        self.humidity = humidity_
        self.device = device_

    def __init__(self, data):
        date = datetime.fromtimestamp(data['d']['timestamp'] / 1000)
        self.timestamp = date
        self.temperature_inside = data['d']['temperature']['inside']
        self.temperature_outside = data['d']['temperature']['outside']
        self.air_pressure = data['d']['air_pressure']
        self.humidity = data['d']['humidity']
        self.device = data['d']['deviceId']

    def toArray(self):
        return [self.timestamp, self.temperature_inside, self.temperature_outside, self.humidity, self.air_pressure]

def getStats(data, device):
    min_temp_inside = min([float(i.temperature_inside) for i in data[device]])
    min_temp_outside = min([float(i.temperature_outside) for i in data[device]])
    min_humidity = min([float(i.humidity) for i in data[device]])
    min_air_pressure = min([float(i.air_pressure) for i in data[device]])

    max_temp_inside = max([float(i.temperature_inside) for i in data[device]])
    max_temp_outside = max([float(i.temperature_outside) for i in data[device]])
    max_humidity = max([float(i.humidity) for i in data[device]])
    max_air_pressure = max([float(i.air_pressure) for i in data[device]])

    avg_temp_inside = sum([float(i.temperature_inside) for i in data[device]]) / len(data)
    avg_temp_outside = sum([float(i.temperature_outside) for i in data[device]]) / len(data)
    avg_humidity = sum([float(i.humidity) for i in data[device]]) / len(data)
    avg_air_pressure = sum([float(i.air_pressure) for i in data[device]]) / len(data)
    return [
        ['min', min_temp_inside, min_temp_outside, min_humidity, min_air_pressure],
        ['avg', avg_temp_inside, avg_temp_outside, avg_humidity, avg_air_pressure],
        ['max', max_temp_inside, max_temp_outside, max_humidity, max_air_pressure]
    ]

def getDataArray(data, device):
    dataArray = []
    for i in data[device]:
        dataArray.append(i.toArray())

    dataArray.append(['--------------------------', '--------------------', '---------------------', '----------', '--------------'])

    return dataArray


def printDataSingleDevice(data, device):
    headers = ["timestamp", "temperature_inside", "temperature_outside", "humidity", "air_pressure"]
    print("device: "+device)
    print(tabulate(getDataArray(data, "SIR_device01") + getStats(data, "SIR_device01"), headers=headers))
    print("\n\n")


def printData(data, devices):
    for device in devices:
        printDataSingleDevice(data, device)


def getSpecificData(data, device, type):
    res = []
    for d in data[device]:
        res.append(getattr(d,type))
    return res

def createPlot(timestamps, data, device, title):
    p = figure(plot_width=400, plot_height=400, title=device + ": " + title,  x_axis_type='datetime')
    p.line(timestamps, data, line_width=2)
    return p

def bokehShow(data, devices):
    headers = ["timestamp", "temperature_inside", "temperature_outside", "humidity", "air_pressure"]
    plotData = []
    for d in devices:
        deviceData = []
        for h in headers:
            oneTypeData = getSpecificData(data, d, h)
            deviceData.append(oneTypeData)
        plotData.append(deviceData)

    devicesPlots = []
    for index, deviceData in enumerate(plotData):
        devicePlots = []
        for i in range(1, len(headers)):
            devicePlots.append(createPlot(deviceData[0], deviceData[i], devices[index], headers[i]))
        devicesPlots.append(devicePlots)

    show(gridplot(devicesPlots))






    # # create a new plot (with a title) using figure
    # p = figure(plot_width=400, plot_height=400, title="My Line Plot")
    #
    # # add a line renderer
    # p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2, line_color="orange", legend_label="asdasd")
    # p.line([1, 2, 3, 4, 5], [7, 1, 3, 5, 4], line_width=2, legend_label="asdasd")
    #
    # e = figure(plot_width=400, plot_height=400, title="My Line Plot")
    #
    # # add a line renderer
    # e.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2, line_color="orange", legend_label="asdasd")
    # e.line([1, 2, 3, 4, 5], [7, 1, 3, 5, 4], line_width=2, legend_label="asdasd")
    #
    # show(row(column(p,e),column(p,e))) # show the results
    #
