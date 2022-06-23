import serial
import matplotlib.pyplot as plt

ser = serial.Serial(port='COM15', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,  rtscts=False, dsrdtr=False)

def ATcommand(cmd):
    ser.write(cmd.encode())
    msg=ser.readline()
    msg=msg.decode("utf-8")
    if msg.endswith("\n"):
        #print("received",msg[0:-1])
        return msg.strip()
    return ''

spectrumOrders=[8, 10, 12, 13, 14, 15,  6, 7, 9, 11, 16, 17,  0, 1, 2, 3, 4, 5]
wavelengths=[410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940]
# the read when the sensor in in black. these values are caused by the leds inside the sensor
# the gain is 3 and the inttime is 250 for these readout values
device_light=[2, 8, 68, 50, 10, 3, 3, 3, 7, 70, 35, 4, 2, 3, 3, 9, 7, 2]
def decodeSpectrum(values):
    intValues=[0]*18
    idx=0
    for value in values.split(','):
        if idx<18:
            order=spectrumOrders[idx]
            idx+=1
            intValues[order]=int(value)
    return intValues

# the gain values are: 0=1x, 1=3.7x, 2=16x,3=64x
# GAIN = 16x, Integration Time (INT_T) = 166m

msg=ATcommand("ATGAIN\r")
print(msg)
# # Set sensor integration time. Integration time = <value> * ~2.8ms.
msg=ATcommand("ATINTTIME\r")
print(msg)

cmd="ATDATA\r"
msg=ATcommand(cmd)
if msg.endswith(' OK'):
    msg=msg[0:-3]
    spectrum=decodeSpectrum(msg)
    print(spectrum)
    plt.plot(wavelengths,spectrum, 'y')
    plt.show()

print('"'+msg+'"')


