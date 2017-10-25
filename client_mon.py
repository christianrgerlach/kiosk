
from threading import Thread, Event
from time import sleep
from datetime import datetime
from mailer import send_alert

#holds tuples of client invo by UUID
client_list = {}
client_timeout = 900

def disconnect_monitor():
	global client_list

	while True:
		for client in client_list:
			time_since_checkin = (datetime.now() - client_list[client][2]).total_seconds()
			print 'checking client:', client, 'checked in', time_since_checkin, 'ago'
			if time_since_checkin > client_timeout:
				print client, 'lost!'
				client_list[client][3] = False
				msg = '\r\n'.join([
					'Streaming server has not heard from a client in ' + str(time_since_checkin) + 's!',
					'Please visit server dash at http://<server_address>/dash',
					'\r\n',
					'Client details:',
					'UUID:',
					client,
					'Stream:',
					client_list[client][0],
					'IP:',
					client_list[client][1],
					'Last served media:',
					str(client_list[client][5])
					])
				#send_alert(msg)

		sleep(15)

disconnect_monitor_daemon = Thread(target = disconnect_monitor)
disconnect_monitor_daemon.daemon = True
disconnect_monitor_daemon.start()