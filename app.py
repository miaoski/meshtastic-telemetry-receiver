# Subscribe to meshtastic serial interface for environmental telemetries
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from pprint import pprint
from time import sleep
from datetime import datetime

# packets = []

def onReceive(packet, interface): # called when a packet arrives
    # print(f"Received: {packet}")
    # pprint(packet)
    # packets.append(packet)
    try:
        if packet['decoded']['portnum'] == 'TELEMETRY_APP' and \
          'environmentMetrics' in packet['decoded']['telemetry']:
            t = packet['decoded']['telemetry']['environmentMetrics']['temperature']
            h = packet['decoded']['telemetry']['environmentMetrics']['relativeHumidity']
            ts = datetime.utcfromtimestamp(packet['decoded']['telemetry']['time']).strftime('%Y-%m-%d %H:%M:%S')
            rssi = packet['rxRssi']
            snr  = packet['rxSnr']
            rxts = datetime.utcfromtimestamp(packet['rxTime']).strftime('%Y-%m-%d %H:%M:%S')
            sid  = packet['fromId']
            print(f'''
Sensor ID  : {sid}
Temperature: {t}
Humidity   : {h}
Time       : {ts}
RSSI       : {rssi}
SNR        : {snr}
Rx Time    : {rxts}''')
    except KeyError:
        pprint(packet)
        pass

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("hello mesh")

pub.subscribe(onReceive, "meshtastic.receive")

# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface()

while True:
    sleep(1)
