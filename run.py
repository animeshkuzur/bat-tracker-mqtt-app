# STARTUP SCRIPT

from app.app import App

def run():
	app=App()
	app.start()
	return 0

if __name__ == "__main__":
	run()