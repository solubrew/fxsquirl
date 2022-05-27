#@@@@@@@@@@@@@@@Pheonix.Store.ObjNQL.TxtONQL@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: f44e5ac0-73c7-4d95-a280-ca9bcd7b8491
	name:
	description: >
		Open Plain Text File Objects and Fill Text Template as Needed
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
import datetime as dt, pprint, time#											||
from os.path import abspath, dirname, exists, join#								||
from os import makedirs#														||
#===============================================================================||
from condor import thing#										||
from subtrix import subtrix#									||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
class doc:#																		||
	'Define Document Text from given File'#										||
	version = '0.0.0.0.0.0.0'#													||
	def __init__(self, doc, kind=None, cfg=None):#								||
		self.doc = doc#															||
		self.kind = kind#														||
		if cfg == None:#														||
			cfg = f'{here}z-data_/objnql.yaml'#									||
	def append(self, text, fill=None, cfg={}):
		''' '''
		self.write(text, fill, cfg, 'a')
		return self
	def load(self, thing=None):#												||
		'''Scan text and replace include codes with other text files '''
		if thing == None:#														||
			thing = self.doc#													||
		try:#																	||
			with open(thing, 'r') as doc:#										||
				text = doc.read()#												||
		except Exception as e:#													||
			text = ''#															||
			m = ['Couldnt Open',thing,'due to',e]#								||
			print(*m)#															||
		if log: print('TEXT', text)
		fnl = thing.rfind('/')#													||
		base_path = thing[:fnl + 1]#												||
		startpt, depth, fstart, fend = 0, 0, '<(INCL)>', '.yaml'#				||
		while True:#															||
			fspl = text[startpt:].find(fstart) + startpt#							||
			linepos = text[:fspl].rfind('\n')#									||
			depth = text[linepos:fspl].find('  ')#								||
			if depth == -1:#													||
				depth = 0#														||
			depth += 1#															||
			if fspl == startpt - 1:#												||
				break#															||
			fspl = fspl#														||
			fepl = text[fspl:].find(fend) + fspl + len(fend)#						||
			pattern = text[fspl:fepl]#											||
			if pattern == '':#													||
				startpt = fepl + len(ntext) - len(pattern)#							||
				continue#														||
			path = pattern.replace(fstart, '')#							||
			if log: print('Pattern', path, 'basepath', base_path)
			path = join(abspath(base_path), path)
			if log: print('Pattern', path, 'basepath', base_path)
			if exists(path):#													||
				ntext = self.load(path)#										||
				ntext = ntext.replace('---', ' ')#								||
				ntext = ntext.replace('\n', '\n' + '  ' * depth)#					||
			else:#																||
				ntext = path#													||
			depth = '\n' + '  ' * depth#		||
			text = f'{text[:fspl]}{depth}{ntext}{text[fepl:]}'#								||
			startpt = fepl + len(ntext) - len(path)#								||
			path = ''#															||
		return text#															||
	def kill(self, lvl=5):#														||
		if lvl == 'mustbethiscode':#											||
			pass#hard delete#													||
		else:#																	||
			pass#																||
		return self#															||
	def process(self):#															||
		if self.fill != None:#													||
			self.dikt = subtrix.mechanism(self.text, self.fill).run()#			||
			self.text = self.dikt#												||
		return self#															||
	def read(self, fill=None, kind=None):#										||
		self.fill, encode = fill, 0#											||
		self.text = self.load(self.doc)#										||
		self.process()#															||
		self.lines = self.text.split('\n')#										||
		self.table = []#														||
		self.frame = []#														||
		self.go = False#														||
		yield self#																||
	def search(self, term, boundaries=None):
		'''Search document text for given term and boundary conditions
			a none boundary should return a simple count value and true statement
			for the search term in the text

		'''

		return self
	def touch(self, phile):#													||
		phile = phile[:phile.rfind('/')]#										||
		if not exists(phile):#													||
			print('Touch File', phile)
			makedirs(phile)#														||
	def write(self, text, fill=None, cfg={}, method='w'):#								||
		if cfg == {}:
			cfg = {'how': 'raw'}
		how = cfg['how']
		if self.doc.replace('\s', '') == '':  #short cicuirting writing blank documents
			return
		self.touch(self.doc)
		self.text, self.fill = text, fill#										||
		with open(self.doc, 'w') as doc:#										||
			if how == 'raw':
				doc.write(str(self.text))#										||
			elif how == 'pretty':
				pprint.pprint(self.text, stream=doc)
def chunk(f, csize=4096):#														||
	yield iter(lambda: f.read(csize), b'')#										||
#===========================Code Source Examples================================||
'''
http://stupidpythonideas.blogspot.com/2014/07/three-ways-to-read-files.html
'''
#===============================================================================||
'''
<(DNA)>:
	2018004051530:
		doc:
			version: <[active:.version]>
			test: PASS
			description: >
			work:
	2018004051421:
		doc:
			version: 0.0.0.0.0.1
			test: PASS
			description: >
				rewrite to process template first and populate
				with given data alinearly
			work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
