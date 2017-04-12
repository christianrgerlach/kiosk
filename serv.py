from flask import Flask, render_template, url_for, redirect, send_file
from os import listdir
from os.path import isfile
from itertools import cycle
from glob import glob
from random import shuffle

####### CONFIG ######

pic_slide_length = 12 #length of picture slideshow
vid_slide_length = 1 #length of video slideshow *** HTML ONLY SUPPORTS 1 ***
build_conent_catalog_freq = 500 #rebuild content catalog every N requests

#####################

app = Flask(__name__)

#list of picture paths
pics = []
#cyclical iterator of pics list
pics_cycle = cycle(pics)

#list of video paths
vids = []
#cyclical iterator of vids list
vids_cycle = cycle(vids)

#counter that counts requests, controls ratio of videos to pictures
counter = 0

#counters to track progression through content
vid_counter = 0
pic_counter = 0

#populates lists of media paths
def build_content_catalog():
	global pics
	global vids
	global pics_cycle
	global vids_cycle

	pics = glob('./media/pics/*.[Jj][Pp]*[Gg]') #grab jpegs
	pics += glob('./media/pics/*.[Pp][Nn][Gg]') #grab + add pngs
	shuffle(pics) #shuffles pics
	pics_cycle = cycle(pics) #creates cycler

	vids = glob('./media/vids/*.[Mm][Pp]4') #grabs mp4s
	vids += glob('./media/vids/*.[Ww][Ee][Bb][Mm]') #grab webms
	shuffle(vids) #shuffles vids and 
	vids_cycle = cycle(vids) #creates cycler

def get_pics(num):
	selected_pics = []
	for i in range (0, num):
		selected_pics.append(pics_cycle.next())
	return selected_pics

def get_vids(num):
	selected_vids = []
	for i in range (0, num):
		selected_vids.append(vids_cycle.next())
	return selected_vids

#returns index page
@app.route('/')
def index():
	global counter
	# if counter is mult of 500, rebuild catalog to catch new files
	if counter % build_conent_catalog_freq == 0:
		build_content_catalog()
	if counter % 2 == 0: # If counter is even
		counter += 1
		return render_template('pic.html', pics=get_pics(pic_slide_length))
	else: #if counter is odd
		counter += 1
		return render_template('vid.html', vids=get_vids(vid_slide_length))

@app.route('/pics/')
def pics():
	return render_template('pic.html', pics=get_pics(pic_slide_length))

@app.route('/vids/')
def vids():
	return render_template('vid.html', vids=get_vids(vid_slide_length))

#returns files for any page other than index
@app.route('/<path:path>')
def file_path(path):
	#if file path is valid file
	if isfile(path):
		return send_file(path) #return the file
	else:
		return '404 invalid file' #else return 404

#forces catalog update
@app.route('/catalog/')
def update():
	build_content_catalog()
	return redirect(url_for('index'))

#main
def main():
	#populates content catalog filenames
	build_content_catalog()
	#runs app server
	app.run(
		host = "0.0.0.0",
		port = 8080,
		threaded = True,
		debug = False # MUST BE FALSE FOR DEPLOYMENT!!!
	)

#only executs if run as main
if __name__ == '__main__':
	main()
