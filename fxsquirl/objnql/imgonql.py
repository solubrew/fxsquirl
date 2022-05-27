'''
---
<(META)>:
	docid: 88b46f29-77e8-4b78-891c-16a19b7b768e
	name:
	description: >

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import base64, os, numpy as np, colorsys
try:#																	||
	import webp
	from PIL import Image
	didPILimport = True
except Exception as e:#													||
	didPILimport = False
	print('imgonql',e)#							||
try:#																			||
	from cv2 import destroyAllWindows, imread, imwrite, VideoCapture#			||
	didCV2import = True
except Exception as e:#															||
	didCV2import = False
	print('imgonql',e)#					||
try:
	import mpl_toolkits.mplot3d.axes3d as p3
except Exception as e:
	print('imonql',e)
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class doc(object):
	''
	version = '0.0.0.0.0.0'#
	def __init__(self, it, how='pil'):
		self.it = it
		self.imageOBJ = None
		self.init(how)
	def init(self, how):
		if how == 'pil' and didPILimport == False:
			how = 'cv2'
		if how == 'cv2' and didCV2import == False:
			return False
		return how
	def convert(self, frum='.jpeg', to='.png'):
		nfile = self.it.replace(frum, to)#								||
		if frum == '.svg':
			from cairosvg import svg2png
			with open(self.it, 'rb') as svg:
				svg2png(svg.read(), write_to=open(nfile, 'wb'))
		if frum == '.webp':
			anim = webp.load_images(self.it)
			if to == '.gif':
				# Grab a reference to the first frame, and save the entire PIL image array as GIF with 70ms frames (14.286 FPS)
				anim[0].save(nfile, save_all=True, append_images=anim[0:], duration=70, loop=0)
		if self.imageOBJ == None:
			self.read()
		try:
			imageOBJ.save(nfile)
			os.remove(self.it)
		except Exception as e:
			print('Image Conversion of ',self.it,'failed for',e)
		self.it = nfile
		return self
	def encode(self):
		nfile = self.it
		if self.imageOBJ == None:
			self.read()
		try:
			self.it = base64.b64encode(self.image)
		except Exception as e:
			print('Image Encoding Failed',e)
		return self
	def getPallette(self):
		''
		max_intensity, self.hues = 100, {}
		[xs, ys] = self.image.size
		for x in range(0, xs):
			for y in range(0, ys):
				r, g, b = self.image.getpixel((x, y))#		Get the RGB color of the pixel
#				print('r',r,'g',g,'b',b)
				r /= 255.0
				g /= 255.0
				b /= 255.0# (5)	Normalize pixel color values
				[h, s, v] = colorsys.rgb_to_hsv(r, g, b)#	Convert RGB color to HSV
				if h not in self.hues:#Marginalize s; count how many pixels have matching (h, v)
					self.hues[h] = {}
				if v not in self.hues[h]:
					self.hues[h][v] = 1
				else:
					if self.hues[h][v] < max_intensity:#not sure what the purpose of this is
						self.hues[h][v] += 1
		return self


	def read(self):
		''
		if how == 'pil':
			self.image = Image.open(self.it).convert('RGB')
		elif how == 'cv2':
			self.image = imread(self.it)
		return self
	def resize(self, size, pad=None, how='height'):
		''
		if self.imageOBJ == None:
			self.read()
		if how == 'height':
			hsize = size
			wsize = float(imageOBJ.size[0])*hsize/float(imageOBJ.size[1])
		elif how == 'width':
			wsize = size
			hsize = float(imageOBJ.size[1])*wsize/float(imageOBJ.size[0])
		imageOBJ = imageOBJ.resize((size, osize), Image.ANTIALIAS)
		if pad != None:
			self.it = calct.stuff(self.it).pad().it
		return self
	def write(self, toFILE=None):
		''
		if how == 'pil':
			self.imageOBJ.save(self.it)
		elif how == 'cv2':
			imwrite(self.it, self.imageOBJ)
		return self

def convertImages(path, subfolder=True):
	fs = next(fonql.doc(path).read())
	tree = fs.dikt
	if log: print('Tree',tree)
	images = tree.filtr(['.jpeg','.jpg','.bmp'])
	if log: print('Images',images)

def getColors(path):
	''
	fs = fonql.doc(path).read()
	while True:
		philes = next(fs, None)
		if philes == None:
			break
		images = philes.filtr(['.png'])
		for image in images:
			imgOBJ = imgonql.doc(image).read()
			colors = imgOBJ.getColors()
			if log: print('Colors',colors.hues)
			plot = imgOBJ.plot()
			thumbIMG = imgOBJ.thumb
			plotIMG = makeimage(plot)
			paletteIMG = makePalette(colors)
#==========================Source Materials=============================||
'''
https://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python
https://gist.github.com/thomir/8075839
https://github.com/deeplook/svglib
https://theailearner.com/2019/08/19/image-blending-using-image-pyramids/

#!/usr/bin/env python3

# Trevor Sullivan <trevor@trevorsullivan.net>
# https://trevorsullivan.net
# https://twitter.com/pcgeek86

# IMPORTANT: Install the webp Python package, using the following command:
# pip3 install --user webp

# Import the webp package




'''
#============================:::DNA:::==================================||
'''
---
	administer:
		version: <[active:.version]>
		test:
		description: >
			Administrate Tests of the Tmplt Classes
		work:
	here:
		version: <[active:.version]>
		test:
		description: >
			Test Each Tmplt Class
		work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
