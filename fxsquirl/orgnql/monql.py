#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid:
	name: Markup Object Notation Query Language
	description: >
		MACRUW
		Move Archive Copy Read Update Write

		Archive, Copy, Read, Update, Write HTML and XML documents










		from local and remote locations#										||
		#Write a ctd file/suplement walk over a directory and create a node for#||
		each file of a given type/s
		#This Script will turn a given file system starting point and specified#||
		depth into a tree based note file.  It will document information about#	||
		the files found and attempt to write all possible files into the
		content area based on a file extension whitelist and extension specific#||
		function This is grafting a file system to a cherrytree document
		options to delete filesystem/convertedfilesonly/create a monitoring
		structure to keep the two in sync???? convert a directory with a
		whitelist of file extensions to a ctd file/add

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/store/orgnql/monql.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
import os, datetime as dt, urllib, html5lib, requests#							||
try:#																			||
	import simplejson as json#													||
except:#																		||
	import json#																||
from bs4 import BeautifulSoup#													||
try:#																			||
	import lxml.etree as xml#													||
	import lxml.html as html#													||
	print('Running with lxml.etree')#											||
except ImportError:#															||
	try:#																		||
		import xml.etree.cElementTree as xml#									||
		print('Running with cElementTree on Python 2.5+')#						||
	except ImportError:#														||
		try:#																	||
			import xml.etree.ElementTree as xml#								||
		except ImportError:#													||
			print('Failed to import ElementTree from any known place')#			||
#================================3rd Party Modules==============================||
try:#																			||
	import pdfkit#																||
except:#																		||
	pass#																		||
#===============================================================================||
from pandas import DataFrame#													||
#===============================================================================||
from condor import condor, thing#												||
from excalc import exam, text as calct#											||
from fxsquirl.objnql import txtonql#											||
#===============================================================================||
here = os.path.join(os.path.dirname(__file__),'')#								||
there = os.path.abspath(os.path.join('../../..'))#								||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class doc:#																		||=>Define class
	'Control I/O for Markup Language formats'#									||=>Describe module
	version = '0.0.0.0.0.0'#													||=>Set version
	def __init__(self, doc, kind=None, cfg=None):#								||=>Initiate object
		self.doc = doc#															||set doc variable
		pxcfg = join(abspath(here), '_data_/orgnql.yaml')#							||use default configuration
		if kind == None:#														||
			kind = exam.thing(self.doc).kind#									||
		self.onql = list(kind.keys())[0]
		self.kind = kind[self.onql]#											||
#		print('Exam',kind)
		if self.doc != cfg:#													||chk config load loop
			self.config = config.instruct(pxcfg).select('monql').override(cfg)#	||load configuration file
		self.parser = self.config.dikt['parser']#								||load parser
		self.dfs = {}
	def getImages(self):
		'''Extract Images from markup by pulling links and parsing encoded
																	images '''
		images = []
		for image in self.soup.find_all('img'):
			images.append(image)
		self.images = images
		return self
	def getLinks(self):#	!!!TODO!!! this needs to be moved to an extract type module
		'''Extract all unique links from markup'''
		links = []#																||
		for link in self.soup.find_all('a'):#									||
			links.append(link.get('href'))#										||
		self.links = links
		return self#															||
	def getTables(self):
		'''Extract HTML tables from document and store as dataframes'''
		tables = self.soup.findAll('table')#									||
		for table in tables:
			records, columns, cnt = [], [], 0
			rows = table.findAll('tr')
			lock = 1
			ttext = table.text
			for row in rows:
				record = []
				for col in row.findAll('td'):
					ttext = ttext.replace(col.text, '')
					if col.string == None:
						text = col.text
					else:
						text = col.string
					print('COL', text)
					record.append(sanitize(text, 'entry'))
					if '1' == record[0]:
						lock = 0
				if lock == 0:
					if records != []:
						if len(records[0]) == len(record):
							records.append(record)
					else:
						records.append(record)
			if len(records) == 0:
				continue
			while len(columns) < len(records[0]):
				columns.append(thing.what().uuid().hexid[-5:])
			print('records', records, 'columns', columns)
			t = sanitize(ttext)
			nuid = thing.what().uuid().hexid[-5:]
			self.dfs[nuid] = DataFrame(records, columns=columns)
		return self
	def getTags(self, tag):
		''' '''
		tags = []
		for tag in self.soup.find_all(tag):
			tags.append(tag)
		self.tags = tags
		return self
	def getVideos(self):
		''' '''
		vids = []
		for video in self.soup.find('a'):
			vids.append(video)
		self.vids = vids
		return self
	def read(self, cfg={}, cmd={}, fill=None):#									||=>Define module
		'''Read document and extract assets from markup languages located
			remotely or locally
			implement chunking
			'''
		doct = self.doc.replace('\t','  ')#								||correct yaml format
		if cfg == None:
			cfg = {'xml': None, 'html': None}
		if self.kind['code'] == 'XML':#											||Load XML text document
			self.text = next(txtonql.doc(self.doc).read()).text
			xmlDOC = xml.fromstring(self.text)#									||load xml str to object
			self.dikt = {xmlDOC.tag: {'Children': elem2dict(xmlDOC),#			||parse xml doc to
									'Tag': xmlDOC.tag, 'Text': xmlDOC.text, #	||standardized
									'Attributes': xmlDOC.attrib}}#				||dictionary
		elif self.kind['code'] == 'HTTP':#										||Load webpage from http server
			try:#																||
				self.doct = urllib.request.urlopen(self.doc)#					||request web page
				self.soup = BeautifulSoup(self.doct, self.parser)#				||parse w bsoup
			except Exception as e:#												||
				self.doct, self.soup = None, None#								||
				m = ['HTTP Request Error ',e,'file improperly formated',doct]#	||
				print(*m)#														||
#			if cfg['how'] == 'streaming':#										||connect to web resource for paging
#				while True:#													||
#					self.doct = response.read(page)#							||
#					if not self.doct:#											||
#						break#													||
#					yield self#													||
			if self.soup == None and cfg['xml'] != None:#						||secondary paths...need to increase details
				try:#															||
					headers = self.config.dikt['headers'][0]#					||
					self.doct = requests.get(self.doc, headers=headers)#		||
					self.soup = BeautifulSoup(self.doct.content, self.parser)#	||
				except Exception as e:#											||
					self.doct, self.soup = None, None#							||
					m = ['HTTP Request Format Error ',e,'This doc failed',doct]#||
					print(*m)#													||
			if self.soup == None and cfg['html'] != None:#						||
				try:#															||
					headers = self.config.dikt['headers'][0]#					||
					self.doct = requests.get(self.doc, headers=headers)#		||
					self.soup = html.fromstring(self.doct.content)#				||
				except Exception as e:#											||
					self.doct, self.soup = None, None#							||
					m = ['HTTP Request Format Error',e,'This doc failed',doct]#	||
					print(*m)#													||
		elif self.kind['code'] == 'HTML':#										||Load HTML text Document
			self.soup = BeautifulSoup(self.doc, self.parser)#					||
			self.text = self.doc#												||
		self.lines = self.text.split('\n')#										||
		self.table, self.frame = None, None#									||
		yield self#																||=>
	def search(self, spat, epat):#												||
		''' '''
		self.finds, start = [], 0
		cnt = 0
		while True:
			pat = calct.stuff(self.soup).findPattern(spat, epat, start)#		||
			find = pat.pattern
			if start == pat.fepl or find == None or find == '':#				||
				break
			start = pat.fepl
			self.finds.append(find)#											||
			cnt += 1
		return self
	def touch(self, phile):#													||
		here = phile[:phile.rfind('/')]#										||
		if not os.path.exists(here):#											||
			os.makedirs(here)#													||
	def write(self, data):#														||write dikt file as json str
		if not isinstance(data, str):
			if isinstance(data, dict):
				if self.kind['code'] == 'XML':
					self.text = convert(data)
		else:
			self.text = data
		with open(self.doc, 'w') as doc:#								||
			doc.write(self.text)#										||
		return self#													||=>
	def xpath2Dict(self):
		''
		doc = {}
		for key, term in self.config.dikt['xpath'].items():
			find = self.dikt.xpath(term['term'])
			doc[key] = []
			for f in find:
				content = sanitize(f.text_content)
				doc[key].append(content)
		return self
def convert(doc):
	'''Convert various formats of dictionaries into specified
														notebook types'''#	||
	text = ttext = btext = ''
	for key, val in doc['dikt'].items():
		if 'Tag' in val.keys():
			ttext += '<{}>'.format(val['Tag'])
			if val['Text']:
				ttext += '{}'.format(val['Text'])
			btext += '</{}>'.format(val['Tag'])
		rttext, rbtext = convert(val['Children'])
		text += f'{ttext}{rttext}{rbtext}{btext}'
	return text
def elem2dict(node):
	"""	Convert an lxml.etree node tree into a dict."""
	dikt={}
	for element in node.iterchildren():
		if element.attrib != {}:
			name = element.attrib['name']
		else:
			name = element.tag
		input = {"Tag": element.tag, "Text": element.text,#						||
											"Attributes": element.attrib,#		||
											"Children": elem2dict(element)}#	||
		if name in dikt.keys():
			dikt[name].append(input)#											||
		dikt[name] = [input]#													||
	return dikt
def downAsset(path):
	''' '''

def sanitize(term, doctype=None):
	''' '''
	if doctype == 'entry':
		items = ['\n']
		for i in items:
			term = term.replace(i, '')
	else:
		items = [',', '#', '0', '[', ']', '\n\n']
		for i in items:
			term = term.replace(i, '')
	return term
#==========================Source Materials=============================||
'''
https://beautiful-soup-4.readthedocs.io/en/latest/#
http://code.activestate.com/recipes/496685-downloading-a-file-from-the-web/
http://stackoverflow.com/questions/13962719/best-way-to-programmatically-save-a-webpage-to-a-static-html-file
http://programminghistorian.org/lessons/working-with-web-pages
http://docs.seleniumhq.org/
http://docs.seleniumhq.org/projects/webdriver/
https://seleniumhq.github.io/selenium/docs/api/java/org/openqa/selenium/ie/InternetExplorerDriver.html
https://seleniumhq.github.io/selenium/docs/api/java/org/openqa/selenium/firefox/FirefoxDriver.html
https://pypi.python.org/pypi/selenium
http://www.webservicex.com/stockquote.asmx?WSDL
http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl
http://www.currencyserver.de/webservice/currencyserverwebservice.asmx?WSDL
http://soaptest.activestate.com:8080/StockQuotePlus.wsdl
http://64.110.96.190/DotNet/ProviderSearch.asmx?WSDL
https://ws-[portalname].csod.com/webservices/LMS/TranscriptAndTaskService.asmx?WSDL
http://www.federalreserve.gov/monetarypolicy/fomcminutes20150729.htm
'''
#============================:::DNA:::==================================||
'''
<(DNA)>:
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
