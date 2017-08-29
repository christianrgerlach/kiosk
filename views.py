from app import *
from catalog import get_pics, get_vids, pic_catalog, vid_catalog, build_content_catalog
from client_mon import client_list
from filters import format_time, time_since

from os.path import isfile
from uuid import uuid4
from datetime import datetime
from werkzeug.exceptions import InternalServerError


####### CONFIG ######

pic_slide_length = 12 #length of picture slideshow
vid_slide_length = 1 #length of video slideshow *** HTML ONLY SUPPORTS 1 ***
build_content_catalog_freq = 500 #rebuild content catalog every N requests

#####################

#counter that counts requests, controls ratio of videos to pictures
counter = 0

#returns index page
@app.route('/')
def index():
	return redirect(url_for('media', location = 'common'))

@app.route('/loc/<location>')
def media(location = 'common'):
	global counter
	global client_list

	# if counter is mult of 500, rebuild catalog to catch new files
	if counter % build_content_catalog_freq == 0:
		build_content_catalog()

	if counter % 2 == 0: # If counter is even
		counter += 1
		content = get_pics(pic_slide_length, location)
		response = make_response (render_template('pic.html', content = content))
	else: #if counter is odd
		counter += 1
		content = get_vids(vid_slide_length, location)
		response = make_response (render_template('vid.html', content = content))

	#get client ID
	client_id = request.cookies.get('client_id')

	#if None, new client
	if not client_id:
		client_id = uuid4()
		print 'new client:', client_id
		response.set_cookie('client_id', bytes(client_id))
	else:
		print 'repeat_client:', client_id

	client_info = (location, request.remote_addr, datetime.now(), True, response, content)

	client_list[client_id] = client_info

	print 'current clients'
	for client in client_list.iterkeys():
		print client

	return response

@app.route('/loc/<location>/list')
def list(location = 'common'):
	return render_template('list.html', pic_list = pic_catalog[location], vid_list = vid_catalog[location])

@app.route('/dash')
def dash():
	return render_template('dash.html', client_list = client_list, client_list_len = len(client_list))

@app.route('/clients/clear', methods = ['GET','POST'])
@app.route('/clients/clear/<client>', methods = ['GET','POST'])
def clients_clear(client = None):
	global client_list
	if not client:
		client_list = {}
	else:
		del client_list[client]
	return redirect(url_for('dash'))

@app.route('/clients/lastcontent_preview/<client>')
def client_last_content_preview(client):
	return client_list[client][4]

@app.route('/clients/lastcontent_listing/<client>')
def client_last_content_listing(client):
	return render_template('list_last.html', client = client, client_list = client_list)

#returns files
@app.route('/<path:path>')
def file_path(path):
	#print "returning file" + path
	#if file path is valid file
	if isfile(path):
		return send_file(path) #return the file
	else:
		return abort(404)

#forces catalog update
@app.route('/catalog/')
def update():
	build_content_catalog()
	return redirect(url_for('media', location = 'common'))

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
	return redirect(url_for('media', location = 'common'))

