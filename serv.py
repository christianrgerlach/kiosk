from flask import Flask, render_template, url_for, redirect, send_file
from os import listdir
from os.path import isfile, isdir
from itertools import cycle
from glob import glob
from random import shuffle

####### CONFIG ######

pic_slide_length = 12 #length of picture slideshow
vid_slide_length = 1 #length of video slideshow *** HTML ONLY SUPPORTS 1 ***
build_conent_catalog_freq = 500 #rebuild content catalog every N requests

#####################

app = Flask(__name__)

#counter that counts requests, controls ratio of videos to pictures
counter = 0

pic_catalog = {}
vid_catalog = {}

def build_content_catalog():
	print "\n*** BUILDING CONTENT CATALOG ***"

	#list contents of media dir
	for content in listdir('./media/'):
		if isdir('./media/' + content): #if item is a directory
			pics = []
			vids = []
			#gets common media
			pics += glob('./media/common/pics/*.[Jj][Pp]*[Gg]') #grab jpegs
			pics += glob('./media/common/pics/*.[Pp][Nn][Gg]') #grab + add pngs
			vids += glob('./media/common/vids/*.[Mm][Pp]4') #grabs mp4s
			vids += glob('./media/common/vids/*.[Ww][Ee][Bb][Mm]') #grab webms
			#gets location media
			if content != 'common':
				pics += glob('./media/' + content + '/pics/*.[Jj][Pp]*[Gg]') #grab jpegs
				pics += glob('./media/' + content + '/pics/*.[Pp][Nn][Gg]') #grab + add pngs
				vids += glob('./media/' + content + '/vids/*.[Mm][Pp]4') #grabs mp4s
				vids += glob('./media/' + content + '/vids/*.[Ww][Ee][Bb][Mm]') #grab webms
			#shuffle lists
			shuffle(pics)
			shuffle(vids)
			pic_catalog[content] = cycle(pics)
			vid_catalog[content] = cycle(vids)

def get_pics(num,loc):
	selected_pics = []
	for i in range (0, num):
		selected_pics.append(pic_catalog[loc].next())
	return selected_pics

def get_vids(num,loc):
	selected_vids = []
	for i in range (0, num):
		selected_vids.append(vid_catalog[loc].next())
	return selected_vids

#returns index page
@app.route('/')
@app.route('/<location>')
def index(location = 'common'):
	global counter

	# if counter is mult of 500, rebuild catalog to catch new files
	if counter % build_conent_catalog_freq == 0:
		build_content_catalog()

	if counter % 2 == 0: # If counter is even
		counter += 1
		return render_template('pic.html', pics=get_pics(pic_slide_length, location))
	else: #if counter is odd
		counter += 1
		return render_template('vid.html', vids=get_vids(vid_slide_length, location))

#returns files for any page other than index
@app.route('/<path:path>')
def file_path(path):
	print "returning file" + path
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
	#runs app server
	app.run(
		host = "0.0.0.0",
		port = 8080,
		threaded = True,
		debug = False # MUST BE FALSE FOR DEPLOYMENT!!!
	)

#only executes if run as main
if __name__ == '__main__':
	main()
