'''
---
<(META)>:
	DOCid:
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
import tinytag
#=======================================================================||
from pheonix.comm import comm#									||
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
	def metadata(self):
		''
		return self
	def init(self):

	def encode(self):
		''
		nfile = self.it
		if self.audioOBJ == None:
			self.read()
		try:
			self.it = base64.b64encode(nfile)
		except Exception as e:
			print('Image Encoding Failed',e)
		return self
	def read(self):
		''
		return self
	def write(self):
		''
		return self
