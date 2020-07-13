import minimalmodbus
import json
import requests
from datetime import datetime
import time

num_retransmissions = 20
#timerCount = 100
#timerArray = range(timerCount)
# while 1:
with open('site_data.txt') as readFile:
    configData = json.load(readFile)

print(configData)

# don't forget to close the file
readFile.close()
invMod = []
inverterData = []
errorCode = {
    'code': [],
    'Problem ModBus Address': [],
    'Problem COM port': []
}

dateTimeObject = datetime.now()
currentDate = dateTimeObject.strftime("%d/%m/%Y")
currentTime = dateTimeObject.strftime("%H:%M:%S")

for i in range(configData['Number of Devices']):
        # if configData['Device Data'][i]['devType'] == 'i':
        try:
            invMod.append(minimalmodbus.Instrument('/dev/ttyUSB0', configData['Device Data'][i]['address'], 'rtu', True))
            invMod[-1].serial.timeout = 1
            invMod[-1].serial.baudrate = 9600

        except:
            errorCode['code'].append('COM Problem')
            errorCode['Problem COM port'].append({'COM Port': 'COM' + str(configData['Device Data'][i]['comNum']),'Address':configData['Device Data'][i]['address']})
            if configData['Device Data'][i]['devType'] == 'i':
                inverterData.append({
                    "DeviceAddress": invMod[-1].address,
                    "DeviceType": 'Inverter',
                    "ICOMPort" : 'failed',
                    "Raw Data": []
                })
            else:
                inverterData.append({
                    "DeviceAddress": invMod[-1].address,
                    "DeviceType": 'Weather Station',
                    "WCOMPort": 'failed',
                    "Raw Data": []
                })
        else:
            if configData['Device Data'][i]['devType'] == 'i':
                inverterData.append({
                    "DeviceAddress": invMod[-1].address,
                    "DeviceType": 'Inverter',
                    "ICOMPort": 'success',
                    "Raw Data": []
                })
            else:
                inverterData.append({
                    "DeviceAddress": invMod[-1].address,
                    "DeviceType": 'Weather Station',
                    "WCOMPort": 'success',
                    "Raw Data": []
                })

        ## RETRY ALGO
        for tries in range(num_retransmissions):

            time.sleep(0.2)  # delay before request

            try:   
                print("device address: " + str(configData["Device Data"][i]['address']) + "-try num: " + str(tries))
                if configData['Device Data'][i]['devType'] == 'i':
                    invCode4_1 = invMod[-1].read_registers(5000, 49, 4)
                    invCode4_2 = invMod[-1].read_registers(5112, 35, 4)
                else:
                    wthCode = invMod[-1].read_registers(0,43,3)
            except:
                print("continued")   
                continue
            else:
                if configData['Device Data'][i]['devType'] == 'i':
                    inverterData[-1]['IModBus'] = 'success'
                    inverterData[-1]['Raw Data'] = (invCode4_1 + invCode4_2)
                else:
                    inverterData[-1]['WModBus'] = 'success'
                    inverterData[-1]['Raw Data'] = wthCode
                break
            
        else:
            errorCode['code'].append('Address Problem')
            errorCode['Problem ModBus Address'].append(configData['Device Data'][i]['address'])
            if configData['Device Data'][i]['devType'] == 'i':
                inverterData[-1]['IModBus'] = 'failed'
            else:
                inverterData[-1]['WModBus'] = 'failed'
            inverterData[-1]['Raw Data'] = []
            
                



        if configData['Device Data'][i]['devType'] == 'i':
            inverterData[-1]['IcurrentDate'] = currentDate
            inverterData[-1]['IcurrentTime'] = currentTime
        else:
            inverterData[-1]['WcurrentDate'] = currentDate
            inverterData[-1]['WcurrentTime'] = currentTime
##

# legend for all the data, addresses and types
# print(invMod[0].address)
# print(invMod[1].address)

legendWth = [
    {
        'addr': 0,
        'description': 'WAmbientTemperature',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'deg C'
    },
    {
        'addr': 1,
        'description': 'WPVModuleTemperature',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'deg C'
    },
    {
        'addr': 13,
        'description': 'WAmbientPressure',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'HPa'
    },
    {
        'addr': 14,
        'description': 'WSolarRadiation',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'W/m^2'
    },
    {
        'addr': 21,
        'description': 'WWindDirection',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'deg'
    },
    {
        'addr': 22,
        'description': 'WWindSpeed',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'm/s'
    },

]

legendInv = [
    {
        'addr':0,
        'description':'INominalOutputPower',
        'bytes':1,
        'signed':False,
        'div':10,
        'unit':'kW'
    },
    {
        'addr':2,
        'description':'IDailyPowerYield',
        'bytes':1,
        'signed':False,
        'div':10,
        'unit':'kWh'
    },
    {
        'addr': 3,
        'description': 'ITotalPowerYield',
        'bytes': 2,
        'signed': False,
        'div': 1,
        'unit': 'kWh'
    },
    {
        'addr': 10,
        'description': 'IDCV1',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 11,
        'description': 'IDCC1',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 12,
        'description': 'IDCV2',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 13,
        'description': 'IDCC2',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 14,
        'description': 'IDCV3',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 15,
        'description': 'IDCC3',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 16,
        'description': 'ITotalDCPower',
        'bytes': 2,
        'signed': False,
        'div': 1,
        'unit': 'W'
    },
    {
        'addr': 18,
        'description': 'IPhaseAVoltage',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 19,
        'description': 'IPhaseBVoltage',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 20,
        'description': 'IPhaseCVoltage',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    },
    {
        'addr': 21,
        'description': 'IPhaseACurrent',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 22,
        'description': 'IPhaseBCurrent',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 23,
        'description': 'IPhaseCCurrent',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'A'
    },
    {
        'addr': 30,
        'description': 'IActivePower',
        'bytes': 2,
        'signed': False,
        'div': 1,
        'unit': 'W'
    },
    {
        'addr': 32,
        'description': 'IActivePower',
        'bytes': 2,
        'signed': True,
        'div': 1,
        'unit': 'VAr'
    },
    {
        'addr': 34,
        'description': 'IPowerFactor',
        'bytes': 1,
        'signed': True,
        'div': 100,
        'unit': 'N/A'
    },
    {
        'addr': 35,
        'description': 'IGridFrequency',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'Hz'
    },
    {
        'addr': 37,
        'description': 'IworkState',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'N/A'
    },
    {
        'addr': 38,
        'description': 'IYearFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'year'
    },
    {
        'addr': 39,
        'description': 'IMonthFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'month'
    },
    {
        'addr': 40,
        'description': 'IDayFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'day'
    },
    {
        'addr': 41,
        'description': 'IHourFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'hour'
    },
    {
        'addr': 42,
        'description': 'IminuteFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'minute'
    },
    {
        'addr': 43,
        'description': 'IsecondFaultAlarm',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'second'
    },
    {
        'addr': 44,
        'description': 'IFaultCode',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'N/A'
    },
    {
        'addr': 48,
        'description': 'INominalReactiveOutputPower',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'kVAr'
    },
    {
        'addr': 49,
        'description': 'IDailyRunningtime',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'minutes'
    },
    {
        'addr': 50,
        'description': 'IPresentCountry',
        'bytes': 1,
        'signed': False,
        'div': 1,
        'unit': 'N/A'
    },
    {
        'addr': 64,
        'description': 'IMonthlyPower',
        'bytes': 2,
        'signed': False,
        'div': 10,
        'unit': 'kWh'
    },
    {
        'addr': 83,
        'description': 'IBusVoltage',
        'bytes': 1,
        'signed': False,
        'div': 10,
        'unit': 'V'
    }
]


for i in range(inverterData.__len__()):
    if inverterData[i]['DeviceType'] == 'Inverter' and inverterData[i]['ICOMPort'] == 'success' and inverterData[i]['IModBus'] == 'success':
        for x in legendInv:
            if x['signed'] == False and x['bytes'] == 1:
                if x['description'] == 'IworkState' or x['description'] == 'IYearFaultAlarm' or x['description'] == "IMonthFaultAlarm" or x['description'] == "IDayFaultAlarm" or x['description'] == 'IHourFaultAlarm' or x['description'] == 'IminuteFaultAlarm' or x['description'] == 'IsecondFaultAlarm':
                    inverterData[i][x['description']] = int(inverterData[i]['Raw Data'][x['addr']] / x['div'])
                else:
                    inverterData[i][x['description']] = float(inverterData[i]['Raw Data'][x['addr']]/x['div'])
                    #'unit':x['unit'],
                    #'bytes':x['bytes']
                #}
            if x['signed'] == False and x['bytes'] == 2:
                inverterData[i][x['description']] = float(int.from_bytes(inverterData[i]['Raw Data'][x['addr']+1].to_bytes(2,'big')+inverterData[i]['Raw Data'][x['addr']].to_bytes(2,'big'),'big',signed = False))
                    #'unit':x['unit'],
                    #'bytes':x['bytes']
                #}
    if inverterData[i]['DeviceType'] == 'Weather Station' and inverterData[i]['WCOMPort'] == 'success' and inverterData[i]['WModBus'] == 'success':
        for x in legendWth:
            inverterData[i][x['description']] = float(inverterData[i]['Raw Data'][x['addr']] / x['div'])
                #'unit': x['unit'],
                #'bytes': x['bytes']
                #}

# print(inverterData)
# print(inverterData)

#inverterData.append(errorCode)
for i in inverterData:
    i.pop('Raw Data',None)



# print(errorCode)
#wthMod= minimalmodbus.Instrument('COM4',2,'rtu',True)

#print(wthMod)

#i=invMod.read_register(5000,0,4,False)
#i=invMod.read_long(5003,4,False,0)
#i = invMod.read_register(5000,0,4,False)
# y = wthMod.read_register(21,0,3,False)
# print(y)


### VALIDATION
wPktProblem = False
iPktProblem = False

for valu in inverterData:
    if "WCOMPort" in valu:
        if (valu["WCOMPort"] != 'success' or valu["WModBus"] != "success"):
            wPktProblem = True
    if "ICOMPort" in valu:
        if (valu["ICOMPort"] != 'success' or valu["IModBus"] != "success"):
            iPktProblem = True

inverterData.append({"wPktSuccess": not wPktProblem, "iPktSuccess": not iPktProblem})

inverterData_json = json.dumps(inverterData,indent=4)
print(inverterData[-1])
#print(inverterData_json)


#print(wPktProblem)
#print(iPktProblem)

#deleting raw data

#url2 = 'http://tskengg.com/SolarLive.aspx'

#timerArray = range(100)

## http posting
# url = 'https://webhook.site/9de21cd8-5ada-4a17-a6c5-9d5c6e06f7d9'
url = 'https://monitoringserver.herokuapp.com/api/records/monitoring'

try:
    x = requests.post(url, json = inverterData)
except:
    print('web host unreachable')
else:
    print('data sent successfully to server')
    
#     numTransmissions = numTransmissions + 1




#x = requests.post('https://ptsv2.com/t/aliiqbal/post',[{'a':2,'x':2},{'a':3,'l':2}])
#x = requests.post('https://ptsv2.com/t/aliiqbal/post',[{'a':2,'x':2},{'a':3,'l':2}])

#
# try:
#     y = requests.post(url2, json = inverterData)
# except:
#     print('web host2 unreachable')
# else:
#     print('data2 sent successfully to server')
#
# print(y.text)

#     for iterat in reversed(timerArray):
#         time.sleep(1)
#         print(str(iterat)+ " seconds till next transmission. TransmissionNO." + str(numTransmissions))
#     timerCount = (timerCount % 500) + 100
#     timerArray = range(timerCount)



