import curses

window = curses.initscr()
window.nodelay(1)

while True:
    print("Hello, world!\r")
    ch = window.getch()
    if ch >= 0:
    	curses.close()
        break
print(ch)