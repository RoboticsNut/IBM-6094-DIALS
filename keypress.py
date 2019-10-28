import sys
import threading
import time

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

# this is to signal when the key_pressed flag has useful data,
# it will be "set" to indicate that the key_pressed flag has been set
# accordingly
data_ready = threading.Event()

class KeyboardPoller( threading.Thread ) :
    def run( self ) :
        global key_pressed
        ch = getch()
        #ch = sys.stdin.read( 1 )
        if ch == 'k' : # the key you are interested in
            key_pressed = 1
        else :
            key_pressed = 0
        data_ready.set()

def main() :
    poller = KeyboardPoller()
    poller.start()

    # check the flag in a manner that is not blocking
    while not data_ready.isSet() :
        print "doing something (main loop)\r"
        time.sleep(.1)

    if key_pressed :
        print "You pressed the magic key!\r"
    print "all done now"

if __name__ == "__main__" :
    main()