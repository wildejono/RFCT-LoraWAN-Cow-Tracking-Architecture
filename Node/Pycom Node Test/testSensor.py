# import lines for BME280 sensor
from machine import I2C
import BME280

i2c = I2C(0)
i2c = I2C(0, I2C.MASTER)
i2c = I2C(0, pins=('P9', 'P10'))
i2c.init(I2C.MASTER, baudrate=10000)

bme = BME280.BME280(i2c=i2c) # BME280 is the pressure, humidity and outdoor temp sensor. Uses addr=119

temp, HRtemp = bme.temperature
hum, HRhum = bme.humidity

print("Rounded Values - Temp: ", temp, "C", ", Hum: ", hum, "%")
print("Readable Values - Temp: ", HRtemp, ", Hum: ", HRhum)
