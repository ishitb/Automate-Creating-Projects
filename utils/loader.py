import time, subprocess, threading
from utils.custom_io import printc
from utils.clear import clear

class Loader :
	loading = True
	loader = ["'....", ".'...", "..'..", "...'.", "....'", "...'.", "..'..", ".'..."]
	def load(self, loading_string) :
		counter = 0
		while self.loading :
			for i in self.loader :
				printc(loading_string if loading_string is not None else "Loading", end='')
				printc(f'{i}', end='\r')
				time.sleep(0.1)

	def stop(self) :
		self.loading = False
		clear()

def loader_module(command, loading_string = "Loading") :
	loader = Loader()
	t = threading.Thread(target=loader.load, args=(loading_string,))
	t.start()
	creation =  subprocess.getoutput(command)
	loader.stop()
	t.join()