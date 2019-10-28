import serial
import sys, traceback

from time import sleep

# Import libraries for threads:
import thread

class _GetchUnix:
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch=_GetchUnix()

dialsPosition=[-1,-1,-1,-1,-1,-1,-1,-1]
dialsCounter=[0,0,0,0,0,0,0,0]
dialsDirection=[0,0,0,0,0,0,0,0]

print( "IBM Python dials 6094-010 V1.0.0" )

dials = serial.Serial('/dev/cu.PL2303-0030134', 9600, timeout=.1, parity=serial.PARITY_ODD, bytesize=8)

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

print "Dials are ready to send data!"
print "Turn dial to display value:"

# Get initial dial values:
dials.write("\x0b")

initialDialsValues = dials.read(16)

if initialDialsValues:
  for index in xrange(0,16,2):
    H_byte = ord(initialDialsValues[index])
    L_byte = ord(initialDialsValues[index+1])
    HL_word = (H_byte << 8) + L_byte
    dialNo = (H_byte >> 3) & 0x07
    position = ((H_byte << 7) & 0xFF) | (L_byte & 127)
    direction= (H_byte >> 2) & 0x01
    dialsPosition[index/2]=position
    dialsDirection[index/2]=direction
else:
  print "Error reading dials values!"
  print "initialDialsValues returned:",ord(initialDialsValues)

# # generate dial layout:
# for index in xrange(0,8):
#   if dialsPosition[index] > -1:
#     print "dial %d: direction %d value %3d counter %8d" %(index+1,  dialsDirection[index], dialsPosition[index], dialsCounter[index])
#   else:
#     print "Error: dial %d contains no value" %(index)


_direction = 0
_position = 0

def display():
  print("\033[8A"),
  print chr(0xd),
        
  for index in xrange(0,8):
    if dialsPosition[index] > -1:
      print "dial %d: direction %d value %3d counter %8d\r" %(index+1, dialsDirection[index], dialsPosition[index], dialsCounter[index])
    else:
      print "dialsPosition contain no values"
      pass
    pass

  sys.stdout.flush()

# display current dials:
print("\033[8B")
display()

# Define thread L for reding keypresses:
def input_thread(L):
    key=getch()
    L.append(key)

def read_dials():
# setup threads for reading from keyboard:
  L = []
  thread.start_new_thread(input_thread, (L,))

  # try:
  while True:
    
    if L:
        key=L.pop()
        #print "Key Pressed:", ord(key)
        for index in xrange(0,8):
          dialsCounter[index]=0
        display()
        if key=='q':
          print
          print "quit invoked IBM dials terminating!"
          dials.close()
          break
        thread.start_new_thread(input_thread, (L,))
        pass

    value = dials.read(2)

    if value:
      H_byte = ord(value[0])
      L_byte = ord(value[1])
      HL_word = (H_byte << 8) + L_byte
      dialNo = (H_byte >> 3) & 0x07
      position = ((H_byte << 7) & 0xFF) | (L_byte & 127)
      direction = (H_byte >> 2) & 0x01
      dialsDirection[dialNo] = direction

      test=direction*248-position

      if (test > 0):
        dialsCounter [dialNo] -= 1;
      elif (test < 1 and direction > 0):
        dialsCounter [dialNo] -= 1;
      else:
        dialsCounter [dialNo] += 1;

      #save previous position and direction:
      _position=position
      _direction=direction
      
      #assignment of new position to dialsPosition array
      dialsPosition[dialNo]=position

      display()
    else:
      pass

read_dials()
