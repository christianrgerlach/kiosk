from os import listdir
from os.path import isdir
from itertools import cycle
from glob import glob
from random import shuffle
import sys

#force unicode for jinja
reload(sys)
sys.setdefaultencoding('utf-8')

#maps of locations to arrays of content
pic_catalog = {}
vid_catalog = {}

#maps of locations to iterable content
pic_catalog_iter = {} 
vid_catalog_iter = {}

def build_content_catalog():
	global pic_catalog
	global vid_catalog
	global pic_catalog_iter
	global vid_catalog_iter

	print "\n*** BUILDING CONTENT CATALOG ***"

	#list contents of media dir
	for content_dir in listdir('./media/'):
		if isdir('./media/' + content_dir): #if item is a directory
			print content_dir, ' - SETTING UP LOCATION'
			pics = []
			vids = []

			#gets common media
			if content_dir != 'test':
				print content_dir, ' - adding common media'
				pics += glob('./media/common/pics/*.[Jj][Pp]*[Gg]') #grab jpegs
				pics += glob('./media/common/pics/*.[Pp][Nn][Gg]') #grab + add pngs
				vids += glob('./media/common/vids/*.[Mm][Pp]4') #grabs mp4s
				vids += glob('./media/common/vids/*.[Ww][Ee][Bb][Mm]') #grab webms

			#gets location media
			if content_dir != 'common':
				print content_dir, ' - adding location media'
				pics += glob('./media/' + content_dir + '/pics/*.[Jj][Pp]*[Gg]') #grab jpegs
				pics += glob('./media/' + content_dir + '/pics/*.[Pp][Nn][Gg]') #grab + add pngs
				vids += glob('./media/' + content_dir + '/vids/*.[Mm][Pp]4') #grabs mp4s
				vids += glob('./media/' + content_dir + '/vids/*.[Ww][Ee][Bb][Mm]') #grab webms

			#shuffle lists
			shuffle(pics)
			shuffle(vids)

			pic_catalog[content_dir] = pics
			vid_catalog[content_dir] = vids

			pic_catalog_iter[content_dir] = cycle(pics)
			vid_catalog_iter[content_dir] = cycle(vids)

def get_pics(num,loc):
	print 'getting', num, 'pics for', loc
	selected_pics = []
	for i in range (0, num):
		selected_pics.append(pic_catalog_iter[loc].next())
	return selected_pics

def get_vids(num,loc):
	print 'getting', num, 'vids for', loc
	selected_vids = []
	for i in range (0, num):
		selected_vids.append(vid_catalog_iter[loc].next())
	return selected_vids

