import smtplib
import json

def send_alert(msg):
	with open("/Users/christian/code/secret/email.json") as data:
		data = json.load(data)
	server = smtplib.SMTP(data['server'] + ':' + data['port'])
	print server.ehlo()
	server.starttls()
	server.login(data['user'], data['password'])
	msg = "\r\n".join([
		"From: " + data['user'],
		"To: " + data['dest'],
		"Subject: Stream Alert!",
		"",
		msg
		])
	print 'sending message:\n\n', msg, '\n\nvia', data['server']
	server.sendmail(data['user'], data['dest'], msg)
	server.quit()