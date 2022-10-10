import os
import glob
import time
import serial

#cargar en los modulos correspondientes
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Variables de ubicacion de datos del sensor y ubicacion arduino
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
arduino = serial.Serial("/dev/ttyACM0",9600)
arduino.flushInput()

#funcion para abrir el archivo de la salida de t° 
def read_temp_raw():
        f = open(device_file, 'r')
#leen las lineas y se devuelven para que el codigo se pueda usar
        lines = f.readlines()
        f.close()
        return lines
#funcion de procesamiento de dator de la anterior funcion 
def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c

class sensor():
        "class temperatura"
        temperatura = read_temp()

datos = sensor()

while True:
	try:
		lineBytes = arduino.readline()
		datosAR= lineBytes.decode("utf-8").strip()
		print(datosAR)
		print("La temperatura actual es: "+str(datos.temperatura)+" ˚C")
		time.sleep(0.5)
	except keyboardInterrupt:
                break
