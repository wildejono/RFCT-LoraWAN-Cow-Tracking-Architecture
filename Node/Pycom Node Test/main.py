#import node_setup # replaced with main.py implementation

## Configuration variables
MAIN_LOOP_SLEEP = 10
NODE_DEBUG_MODE = 1 # 1=comments | 0=clean

# import lines for BME280 sensor
from machine import I2C
import BME280

# import lines for LoRa Node Setup (credit PyCom & CoreElectronics)
from network import LoRa
import socket
import binascii
import struct
import time

if(NODE_DEBUG_MODE == 1):
    print("-- Node Operational!")

## BEGIN LORA SETUP

if(NODE_DEBUG_MODE == 1):
    print("-- Beginning LORA Setup...")

# Settings for AU915
LORA_FREQUENCY = 916800000
LORA_NODE_DR = 5

# TTN Parameters (APB)
dev_addr = struct.unpack(">l", binascii.unhexlify('260215B9'))[0]
nwk_swkey = binascii.unhexlify('DA3C044060B0C7B96495D4878A827BC6')
app_swkey = binascii.unhexlify('32B173FD9C447A22D6B0511C3C41EF0B')

# Create loRa object, set the mode to WAN and region to AU915
# - Note setting region does not complete setup - We must still modify channels
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)

# remove all the non-default channels
for i in range(0, 72):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

if(NODE_DEBUG_MODE == 1):
    print("-- LORA Configured!")
    print("-- Node Operational!")

## END LORA SETUP
## BEGIN BME280 SETUP

if(NODE_DEBUG_MODE == 1):
    print("-- Beginning T-H Sensor Setup...")

i2c = I2C(0)
i2c = I2C(0, I2C.MASTER)
i2c = I2C(0, pins=('P9', 'P10'))
i2c.init(I2C.MASTER, baudrate=10000)

bme = BME280.BME280(i2c=i2c) # BME280 is the pressure, humidity and outdoor temp sensor. Uses addr=119

if(NODE_DEBUG_MODE == 1):
    print("-- T-H Sensor Setup Complete!")


## END BME280 SETUP

temp, HRtemp = bme.temperature
hum, HRhum = bme.humidity

if(NODE_DEBUG_MODE == 1):
    print("-- Found Values - Temp: ", temp, ", Hum: ", hum)

## NODE MAIN LOOP BEGIN

while(True):
    ### MAIN STRUCTURE
    if(NODE_DEBUG_MODE == 1):
        print(">> Beginning Node Cycle")

    if(NODE_DEBUG_MODE == 1):
        print(">  Obtaining temperature/humidity values")

    temp, HRtemp = bme.temperature
    hum, HRhum = bme.humidity

    pkt_out = bytes([temp]) + bytes([hum])

    if(NODE_DEBUG_MODE == 1):
        print(">  Transmitting packet: ", pkt_out)

    s.send(pkt_out)

    time.sleep(MAIN_LOOP_SLEEP)

## NODE MAIN LOOP END
