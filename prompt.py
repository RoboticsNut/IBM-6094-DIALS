import sys

sinput=1

while True:
  try:
    if  sinput!='q':
      try:
        print "in inner most TRY:\r",
      except KeyboardInterrupt:
        print 'KeyboardInterrupt caught'
        sinput = raw_input('prompt>')
        raise  # the exception is re-raised to be caught by the outer try block
    else:
      pass
  except (KeyboardInterrupt):
    print '\nkeyboardinterrupt caught (again)'
    print '\n...Program Stopped Manually!'
    raise