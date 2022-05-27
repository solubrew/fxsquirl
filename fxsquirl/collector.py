#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: 0ff06b79-38bf-482c-b39c-04c3d7769865
	name: FxSQuiRL Collector Module Python Document
	description: >

		Read data from the active source and write data to the active sink
		while providing ways to extract data from the process for use in further
		collections and the ability to analyze and/or modify the data between
		sink and source
		recreate tables
		build out views and indexes
		design collector to take any output given to it this means
		leveraging exam very deeply need to start by creating an output
		log for exams Find and separate specific data elements from larger
		dataset these may be in the forms of content extraction or structural
		extraction this is different than the fxsquirlcule level sane due to keep
		all elements intact extract tables from trees

	expirary: <^[expiration]^>
	version: <^[version]^>
	path: <[LEXIvrs]>fxsquirl/collector.py
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = False
#===============================================================================||
import urllib, datetime as dt, time, sys#							||
from logging import getLogger, basicConfig, DEBUG
from logging.config import fileConfig
#================================3rd Party Modules==============================||
from fxsquirl.libs import profile, np, DataFrame, concat, pdfkit, pdr
#===============================================================================||
from condor import condor, thing#												||
from excalc import data as calcd, text as calct, ts as calcts, tree as calctr#	||
from excalc import exam#														||
from fxsquirl.objnql import tblonql, txtonql
from fxsquirl.orgnql import fonql, monql, sonql, yonql
from fxsquirl import generator
from subtrix import subtrix#									||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/fxsquirl.yaml')#								||use default configuration
class engine(generator.engine):#													||
	'''
	WhereUsed:
		fxsquirl.Chunker()
		worldbridger.stone()
	'''
	def __init__(self, cfg={}):#	||
		'''Collect data in various forms from various sources and store in a
			preconfigured structure of databases and files with the ability
			to override with runtime configurations'''#							||
		self.config = condor.instruct(pxcfg).select('collector').override(cfg)#	||load configuration file
		self.session = self.config.ppov#										||
		self.extractonly = False
		generator.engine.__init__(self, self.config)

	def collect(self, table=None, map: dict={}, name='base', overwrite=False):
		'''Collect runs a data storage algorythm against any data source
			configured as an yielding object intended for paging through inputs
			and outputs in order to retrieve and store data from the source in
			either a persistent and/or temp based store.

			table: str => this should be the table specified in the reader
			map: dict => this allows for columns from one source to be mapped to another
			name: None =>
			overwrite: False =>			'''
		while True:
			robj = next(self.rdr, None)
#			if overwrite and robj.status:
#				self.cache.store.pop(table)
			if table in list(self.cache.store.iterkeys()):

				#hack
				if isinstance(self.cache.store[table], dict):
					self.cache.store[table] = DataFrame()

				load = [self.cache.store[table]]
				if log: print('Load\n', load)
				if type(robj) == sonql.doc:
					# if table not in robj.dfs.keys():
					# 	break
					if log: print('ROBJ.dfs concnt', robj.dfs[table])
					load.append(robj.dfs[table])
				else:
					# if table not in robj.cache.store.iterkeys():
					# 	break
					if log: print('ROBJ.cache concat', robj.cache.store[table])
					load.append(robj.cache.store.pop(table))
				self.cache.store[table] = concat(load)
			else:
				if type(robj) == sonql.doc:
					if log: print('ROBJ.dfs', robj.dfs)
					# if table not in robj.dfs.keys():
					# 	break
					if log: print('ROBJ.dfs', robj.dfs[table])
					self.cache.store[table] = robj.dfs[table]
				else:
					# if table not in robj.cache.store.iterkeys():
					# 	break
					if log: print('ROBJ.cache', robj.cache.store[name])
					self.cache.store[table] = robj.cache.store.pop(name)
			if log: print('Collected', list(self.cache.store.iterkeys()))
			if not robj.status:#I think there is tension between single pages of data below the page size and multiple pages
				if log: print('Break Collection')
				break
		if map != {}:
			self.buildMappedColumn(map, table)
		if 'extracts' in self.cache.store.iterkeys():
			if name in self.cache.store['extracts'].keys():
				self.extractDataSet(table, name)
		if self.extractonly == False:
			if log: print('Writer', type(self.wrtr), self.cache.store[table])
			self.wrtr({table: self.cache.store[table]})#					||
		return self

	def extract(self, table=None, map: dict={}, name='base', overwrite=False):
		'''Run the collector without actually storing any information so that
			data can be extracted for in function needs downstream '''
		self.extractonly = True
		self.collect(table, map, name, overwrite)
		self.extractonly = False
		return self

	def getLastSink(self, table, sink=None):
		'''Retrieve an id from the last write to the sink for the given
		database and table in order to prevent duplicate information
		setup a tiered system to fail back to getting it from the sink database
		itself but this is the most costly...carry last sink in memory loading
		initially at first sink event....this for the application  but what
		about the repo extraction service...the message server will represent
		memory? harden with use of the osbrain and shared memory
		'''
		if table not in self.last.keys():
			self.setReader({'table': [table]}, sink)
			col = f'{table}id'
			self.initExtract(col, 'item').extract()
		self.last[table] = self.cache.store[table][col]
		return self.last[table]

	def initCollector(self, src, srct, name='base'):
		'''initate a collector on the current bridge instance'''
		self.initSource(src, srct, name)
		self.initSink(src, srct, name)
		return self

	def load(self, table, load):
		''' '''
		self.sinkdfs[table] = load
		self.wrtr(self.sinkdfs)#					||
		return self

	def setLastSink(self, sink):
		''' '''
		self.last[sink] = self.lsinkv
		self.collect({'last': {'records': [[sink, self.lsinkv]]}})
		return self

	# def setModifier(self, molecule):
	# 	'''Provide a data modification object to be used to alter collected data
	# 		in some way before storage in the sink
	#
	# 		need to create a way to add or remove data to collected data
	# 		'''
	#
	# 	if isinstance(molecule, tmapr):
	# 		self.modfx = molecule
	#
	# 	return self
	# def stake(self, sink=None, cfg=None):#											||
	# 	'''Stake bootstraps a new collection to start the building out of data
	# 		storage'''#															||
	# 	if cfg == None:
	# 		if 'stake' in self.config.dikt.keys():
	# 			cfg = self.config.dikt['stake']
	# 	if 'name' not in self.config.dikt.keys():#									||
	# 		self.name = '<[COLCTN:.incid]>'#									||set default name
	# 	else:#																	||
	# 		self.name = self.config.dikt['name']#									||
	# 	if ':.incid]>' in self.name:#											||check for name increment
	# 		self.name = subtrix.mechanism([self.name,]).run()[0]#.code()#				||
	# 	if sink == None:#														||
	# 		table = f'{self.name}'
	# 		sink  = self.session['stores']['WORKvrs']
	# 		v = f'{sink}/{self.name}/{self.name}.sqlite'#							||
	# 		sink = {'options': {'db': v, 'to': {'tables': [table]}}}#	||set db name
	# 	kind = exam.thing(sink).kind
	# 	self.onqlSINK = list(kind.keys())[0]
	# 	self.kindSINK = kind[self.onqlSINK]#							||
	# 	self.kindSINK['path'] = sink['options']['db']
	# 	self.kindSINK['table'] = sink['options']['to']['tables'][0]
	# 	return self#															||
	# def _integrateReaderObject(self, robj, table, name, overwrite=False):
	# 	''' '''
	# 	if log: print('RDRobj', robj)
		#if isinstance(robj, (sonql.doc, fonql.doc, txtonql.doc, yonql.doc)):
		# 	if log: print('RDRObj', rdrobj.dfs)
		# 	if 'dfs' in rdrobj.__dir__():
		#
		# 		if log: print('HAS DFS', rdrobj.dfs)
		# 		for key in rdrobj.dfs.keys():
		# 			if key in self.cache.store[name][table].keys():
		# 				dfs = [self.sinkdfs[key], rdrobj.dfs[key]]
		# 				self.sinkdfs[key] = concat(dfs)
		# 			else:
		# 				self.sinkdfs[key] = rdrobj.dfs[key]
		# else:
		# 	for key in rdrobj.sinkdfs.keys():
		#
		# 		if key in self.sinkdfs.keys():
		# 			if self.sinkdfs[key].equals(rdrobj.sinkdfs[key]):
		# 				del rdrobj
		# 				return self
		# 			else:
		# 				dfs = [self.sinkdfs[key], rdrobj.sinkdfs[key]]
		# 				if log: print('Concat', dfs)
		# 				self.sinkdfs[key] = concat(dfs)
		# 		elif key in rdrobj.dfs.keys():
		# 			dfs = [self.sinkdfs[key], rdrobj.dfs[key]]
		# 			if log: print('Concat', dfs)
		# 			self.sinkdfs[key] = concat(dfs)
		# 		else:
		# 			self.sinkdfs[key] = rdrobj.sinkdfs[key]
		# del rdrobj
		return self


#==========================Source Materials=============================||
''''
https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
