import time, subprocess, threading, sys
from utils.custom_io import printc
from utils.clear import clear

linux = False
if sys.platform == 'linux' or sys.platform == 'linux2' :
	linux = True

if linux :
	import curses

class Loader :
	loading = True
	loader = ["'....", ".'...", "..'..", "...'.", "....'", "...'.", "..'..", ".'..."]
	def load(self, loading_string) :
		counter = 0
		start = time.time()
		while self.loading :
			for i in self.loader :
				printc(loading_string if loading_string is not None else "Loading", end='')

				if linux :
					curses.initscr()
					curses.curs_set(0)

				printc(f'{i}\t{round(time.time() - start, 2)}s', end='\r')
				time.sleep(0.1)

	def stop(self) :
		self.loading = False

		if linux :
			curses.curs_set(1)
			curses.endwin()

		clear()

def loader_module(command, loading_string = "Loading") :
	loader = Loader()
	t = threading.Thread(target=loader.load, args=(loading_string,))
	t.start()
	creation =  subprocess.getoutput(command)
	loader.stop()
	t.join()