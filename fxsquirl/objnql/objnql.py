#@@@@@@@@@@@@@@fxsquirl.ObjNQL.ObjNQL@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 775cf784-a388-4228-b0be-d46fd432d6a8
	name: Element Level Store Module ObjNQL Extension Python Document#	||
	description: >
		Object Notation Query Language
		will handle all singular object data store
		files will be opened here if the file contains structured data then
		it will be routed to the orgnql data store leg
		update to use pandas as much as possible and work with dataframes

		need to integrate more fully with the bear configs
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/store/store.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import os, datetime as dt, time#										||
#===========================3rd Party Modules===========================||
import pandas as pd
#===============================================================================||
from condor import condor, thing#										||

from fxsquirl import fxsquirl#										||
from fxsquirl.objnql import objnql, txtonql, tblonql#								||
from fxsquirl.orgnql import orgnql#								||

from excalc import exam, phile as examp, text as examt#								||
#=========================Common Globals========================================||
here = os.path.join(os.path.dirname(__file__),'')#								||
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class doc:#																		||=>Define class
	'I/O objects to persistant stores incl. file systems'#						||=>Describe class
	version = '0.0.0.0.0.0'#													||
	def __init__(self, doc, kind=None, cfg=None):#								||
		self.doct= doc#															||
		if kind == None:#														||
			self.kind = exam.thing(self.doct).kind#								||
		else:#																	||
			self.kind = kind#													||
		if cfg != None:#														||chk given configuration
			self.iconfig = config.instruct(cfg).load().dikt#					||
		pxcfg = '{0}z-data_/objnql.yaml'.format(here)#							||use default configuration
#		cfg = '/home/solubrew/data/WDM/thingery_com/content/whats/abstracts'
#		cfg += '/defined/digitalsystems/filetypes.yaml'
		self.config = config.instruct(cfg).load().dikt#					||load configuration file
#		self.config = thing.what().get(cfg).dikt#						||load configuration file
		self._qlrtr()#													||
		self.text, self.lines, self.table = '', '', []#					||
		self.dikt, self.frame, self.tree = {}, pd.DataFrame(), {}#		||
	def _qlrtr(self):#													||=>Define module
		'Route store to the properly formatted object path'#			||=>Describe module
		modlp, ql = 'fxsquirl.objnql.objnql.', None#		||
		try:
			ql = modlp+self.kind['objnql']['f(x)']
		except Exception as e:
			comm.see(['Why is this not working',e])
		if ql == None:#												||
			m = ['Routing of ',self.doct,' Failed with kind ',#			||
					self.kind]#											||
#			comm.see(m) #											||
			ql = modlp+'txtonql'#									||
		print('ObjNQL',ql)
		self.dh = config.instruct(ql).modulize().obj#			||
		self.obj = self.dh.doc(self.doct, self.kind)#					||
		return self#													||=>
	def append(self, data, ext=None, cfg=None):#						||
		cfg = {'mode': 'a'}#											||
		try:#															||
			self.dh.doc(self.doct).write(data, ext, cfg)#				||
		except Exception as e:#											||
			m = ['ObjNQL.Append Failed due to',e]#						||
			show.show(m).terminal(here).code(o[3])#						||
		return self#													||
	def getDocConfigs(self):#											||
#		show.show(self.config).terminal().code(o[6])#					||
		cfg = config.instruct(self.config['filetypes']).load().dikt
		for ql, itms in cfg.items():#							||
			if self.dtype in itms['file_exts']:#						||
				self.func = itms['f(x)']#								||
				break#													||
			else:#														||
				self.func = None#										||
		return self#													||
	def meta(self):#													||
		self.cretime = time.ctime(os.path.getmtime(self.doct))#			||
		self.size = os.path.size(f1l3)#									||
		return self#													||
	def read(self, fill=None, cfg=None, cmd=None):#						||=>Define module
		'Read data from routed object notation query'#					||=>Describe module
		if cfg == None:#												||
			cfg = {'how': 'block'}#										||other option is chunk
		next(self.obj.read(fill, cfg))#									||
		self.go = self.obj.go
		self.text, self.lines = self.obj.text, self.obj.lines#			||
		self.dikt, self.frame = self.obj.dikt, self.obj.frame#			||
		self.kind = exam.thing(self.text, self.kind).kind#				||
		if list(self.kind.keys())[0] == 'orgnql':#						||
			org = next(orgnql.doc(self.text, self.kind).read())#		||
			self.table, self.frame = self.obj.table, self.obj.frame#	||
			self.dikt, self.tree = org.dikt, org.tree#					||
		yield self
	def touch(self, phile):#											||
		here = phile[:phile.rfind('/')]#								||
		if not os.path.exists(here):#									||
			os.makedirs(here)#											||
		yield self#														||
	def web2PDF(self, site=None, out=None):
		'Save Webpage as a PDF'#										||
		if site == None:#												||
			site = self.source#											||
		if out == None:#												||
			out = self.store().outfile#									||
		try:#															||
			pdfkit.from_url(site, out)#									||
		except:#														||
			pass#write site to another list for different tools to be used for collection
		return self#													||
	def write(self, data, ext=None, cfg=None):#							||
		self.touch(self.doct)#											||
		self.dh.doc(self.doct).write(data)#								||
		return self#													||
	def screen(self, too=None, imgtype='JPEG'):#						||
		'Grab a screen shot and store it in a general store'#			||
		if too == None:#												||
			too = self.too#												||
		time.sleep(5)#													||
		ImageGrab.grab().save(too, imgtype)#							||
#==========================Source Materials=============================||
'''
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_excel.html
'''
#============================:::DNA:::==================================||
'''
<(DNA)>:
	<@[datetime]@>:
		<[class]>:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
	<[datetime]>:
		here:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
