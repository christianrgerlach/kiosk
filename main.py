from app import *
from catalog import build_content_catalog
import client_mon
from views import *

#main
def main():
	#runs app server
	build_content_catalog()
	app.run(
		host = "0.0.0.0",
		port = 8080,
		threaded = True,
		debug = False # MUST BE FALSE FOR DEPLOYMENT!!!
	)

#only executes if run as main
if __name__ == '__main__':
	main()
