from app import *
from views import *
from catalog import build_content_catalog
from client_mon import disconnect_monitor

#main
def main():
	#runs app server
	build_content_catalog()
	app.run(
		host = "0.0.0.0",
		port = 8080,
		threaded = True,
		debug = True # MUST BE FALSE FOR DEPLOYMENT!!!
	)

#only executes if run as main
if __name__ == '__main__':
	main()
