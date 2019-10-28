import serial
import sys, traceback

from time import sleep

print( "IBM Python dials 6094-010 V1.0.0" )

dials = serial.Serial('/dev/cu.PL2303-0030134', 9600, timeout=1, parity=serial.PARITY_ODD, bytesize=8)

dials.flushInput()
dials.flush()

#check to see if dials are connected:
dials.write(chr(0x06))
status = dials.read(1)

if status:
  if status == chr(0x08):
    print "Dials connected!"
    print ("status: ", status)
  else:
    print "Unexpected status byte:", ord(status)
if not status:
  print( "FAIL: dials not found, NULL" )
  print( "Exiting IBM Python dials program!" )
  dials.close()
  sys.exit(0)

# reset dials: 0x01
dials.write( chr(0x01) )

sleep(1.0) # Time in seconds.

# configure dials for output - Initialize Dials:
dials.write( chr(0x08) )

# set dial precision: 0xC8 [byte]
# set dial precision to 8 bits per dial
dials.write(chr(0xC8))
dials.write(chr(0xFF))

print "Dials are ready to send data:"

try:
  while True:
    pass
    value = dials.read(2)
    if value:
      H_byte = ord(value[0])
      L_byte = ord(value[1])
      HL_word = (H_byte << 8) + L_byte
      dialNo = (H_byte >> 3) & 0x07
      position = ((H_byte << 7) & 0xFF) | (L_byte & 127)
      print "Dial ", dialNo+1," Position: ", position
      #print "HL_word: ", bin(HL_word) #BINARY output of H_byte + L_byte
except KeyboardInterrupt:
  print
  print "Control-C received IBM dials terminating!"
  dials.close()
  pass
