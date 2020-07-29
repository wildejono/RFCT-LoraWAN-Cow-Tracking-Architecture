#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.au.thethings.network'
PORT = 1700

NTP = "au.pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'WildeOptusNetwork'
WIFI_PASS = 'WildeOptus101!'

# for AU915
LORA_FREQUENCY = 916800000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5
