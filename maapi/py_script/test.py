
import bmp085 as BMP085

sensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)

print float(sensor.read_raw_pressure())
print float(sensor.read_pressure())/100
print float(sensor.read_raw_temp())
print float(sensor.read_temperature())
