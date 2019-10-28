import serial

lpfk = serial.Serial('/dev/cu.PL2303-0040134', 9600, timeout=1, parity=serial.PARITY_ODD, bytesize=8)

lpfk.write(chr(0x01))

i=0
while i < 2**32:
	i += 1
	lpfk.write(chr(0x94)), lpfk.write(chr((i>>24)&0xFF)), lpfk.write(chr((i>>16)&0xFF)),lpfk.write(chr((i>>8)&0xFF)),lpfk.write(chr(i&0xFF))
