#@@@@@@@@@@@@@@Pheonix.Organelle.Collector.Collector@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '19586915-c5c8-431c-9ff8-b323c9e614e7'
	name: FxSQuiRL Builder Module Python Document
	description: >
		An engine for building data artificats
	expirary: '<^[expiration]^>'
	version: '<^[version]^>'
	path: '<[LEXIvrs]>fxsquirl/builder.py'
	authority: 'document|this'
	security: 'seclvl2'
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
import urllib, datetime as dt, time, sys#							||
#===============================================================================||
from pandas import DataFrame, concat
#===============================================================================||
from condor import condor, thing#										||
from excalc import tree as calctr, ts as calcts
from squirl.objnql import tblonql
from squirl.orgnql import conql, fonql, monql, sonql, yonql
from fxsquirl.libs import DataFrame, Cache
#===============================================================================||
here = join(dirname(__file__),'')#						||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_', 'builder.yaml')#								||use default configuration

class engine():#															||
	'''The Builder engine is designed to setup data storage resources such as
		a cache
		a database
			view
			index
			load
			table
		a filesystem
		an endpoint connection
			to an API
			to an FTP site
		files of various types
		'''
	def __init__(self, cfg={}):#		||
		''' '''#							||
		self.config = condor.instruct(pxcfg).override(cfg)#							||load configuration file
		self.cache = None

	def addColumn(self, fx, column, params={}, new_column=None, name='base'):
		'''Add a column to a dataframe held in the sink dataframes dictionary
		'''
		if name == None:
			stuuid = what().uuid().ruuid[-5:]
			name = f'{column}_{stuuid}'
		df = self.sinkdfs[name][column].apply(fx, params)
		self.sinkdfs[name][new_column] = df
		return self

	def build(self, ):
		''' '''
		if 'view' in load.keys() and self.extractonly == False:
			self.createView(load)
		elif 'index' in load.keys() and self.extractonly == False:
			self.createIndex(load)
		elif 'load' in load.keys():
			self.sinkdfs[table] = self.buildDFs(load['load'], table)
			lock = 0
		elif 'table' in load.keys():
			##hack
			if table == None:
				table = load['table']
		return self

	def buildDB(self, load: dict={}, map: dict={}):
		'''Create Databse Tables, Views, and Indexes from a sturctured
			dictionary => {
				table:
				view:
				index:
			}
		'''
		for i, l in load.items():
			if i in ('index'):
				continue
			self.wrtr({i: l})
		return self

	def buildFS(self, home):
		''' '''
		fs = fonql.doc(home).read()
		while True:
			fd = next(fs, None)
			if fd == None:
				break
			for f in fd.dikt.philes:
				doc = txtonql.doc(f).read()
				ndoc = subtrix.mechanism(doc, self.config).run()[0]
				txtonql.doc(f).write(ndoc)
		return self

	def buildEndPoint(self, links: list=[], ept: str='map', service='etherscan'):#					||
		'''Build end point given links a ept parse type
		links:
		ept:
		fairly specific to etherscan need to expand if possible
		'''#																||
		self.bep = self.config.dikt['api']['url']#								||base end point
		params = self.config.dikt['api']['parameters']
		params = params if params else {}
		self.parameters = calctr.stuff(params)#	||
		apikeys = self.config.session.ppov['apikeys']
		if apikeys:
			self.parameters.it['apikey'] = apikeys[service]['key']
		if ept == 'seq':
			links = [self.config.dikt['build'][x] for x in links]
		self.links = links
		url = ''
		for link in links:
			if '?' not in link and '&' not in link and '=' not in link:#		|| sanitize for parameter based links
				url = f'{url}{link}/'#											||
			else:
				url = f'{url}{link}'#											||
		if '/' == url[len(url)-1:]:
			url = url[:len(url)-1]
		self.ep = f'{self.bep}{url}'#											||
		return self#															||

	def buildMappedColumn(self, map: dict, table: str):
		'''Map table column to new column using the map key
		map:
		table:
		'''
		for key, col in map.items():#											||
			self.sinkdfs[table][col] = self.sinkdfs[table][key]#						||
			self.sinkdfs[table].drop(key, inplace=True)#							||
		return self

	def buildMappedRecords(self, ep, row, columns, table, psize):
		'''Combine various data into rows and concatenate to sink dataframes
			for prepreration for database storage
			not sure what the append row was about
			'''
		appendrow = []
		record = self.buildMappedRecord(ep, row, columns)
		if record == ['' for x in range(len(record))]:#filtering out records full of ''
			return self
		if not table in self.cache.store.iterkeys():
			self.cache.store.add(table, DataFrame())
		df = DataFrame([appendrow + record], columns=columns)
		if isinstance(self.cache.store[table], DataFrame):
			load = [self.cache.store.pop(table), df]
			df = concat(load).reset_index(drop=True)
		self.cache.store[table] = df
		if log: print(f'build Mapped Records {table}', self.cache.store[table])
		return self

	def buildMappedRecord(self, ep, row, columns=[]):
		'''Iterate through column map and tree based row of data to create a
		table record.  The optional variable columns allows for the record to be
		remapped during runtime without losing the ability to maintain a full
		dataset configuration
		ep: end point structure from configuration
		row: row of data represented by a dictonary
		columns: optional variable to add or drop columns on the record
		'''
		record = []
		for column in columns:
			if column not in ep['map']:
				continue
			if ep['map'][column] == []:
				dat = ''
			else:
				dat = row
			for link in ep['map'][column]:#each data field could be a tree
				try:
					dat = dat[link]
				except:
					dat = ''
			record.append(dat)
		return record

	def buildMappedTable(self, rows, reqLinks: list=[], returnLinks: list=[],
									table: str='base', cols={}, psize=100000):#||
		'''Build a table out of variously structured dictionary type objects
		data: dataset to be mapped to a table
		links:
		maplinks: links to accessing the configuration for an endpoints fields
		table:
		altercols:		'''
		ep = self.config.dikt['endpoints']
		if log: print('Request Links', reqLinks)
		if reqLinks == []:
			reqLinks = self.links
		ep = calctr.treeWalk(ep, reqLinks, 'map')
		if log: print('EndPoint\n', ep)
		cols = {} if cols == None else cols
		if not ep['map'].keys():
			return False
		if cols == {}:
			cols = list(ep['map'].keys())
		if log: print('Rows\n', rows)
		if log: print('Return links\n', returnLinks)
		if isinstance(rows, dict):
			rows = calctr.treeWalk(rows, returnLinks)  #walking down the end point
		if log: print('Rows\n', rows)
		if rows == []:
			return False
		if log: print('Rows\n', type(rows))
		status = True
		if isinstance(rows, dict):#keyed data has to be accessed each element at a time
			if log: print('Map Dict', rows)
			if len(rows.items()) < psize:
				status = False
			for key, row in rows.items():
				self.buildMappedRecords(ep, row, cols, table, psize)
		elif isinstance(rows, list):
			if log: print('Map List', rows)
			if len(rows) < psize:
				status = False
			for row in rows:#need to create a path to allow side stepping this build unless appsolutely needed
				self.buildMappedRecords(ep, row, cols, table, psize)
			#self.cache.store[table] = DataFrame(rows, columns=cols)
		elif isinstance(rows, str):
			if log: print('Rows', rows)
			self.cache.store[table] = rows
		#if log: print('Mapped Table Status', rows, status, len(rows), psize)
		return status

	def createViews(self, load):
		''' '''
		self.wrtr(load)
		return self

	def dropTables(self, scheme):
		''' '''
		self.dbis[scheme].drop('ALL', 'table', 3333)
		return self

	def initCache(self, table=None, name='base'):
		''' '''
		self.sink = self.setResource(table, 'cache', {}, name)
		if not self.cache:
			self.cache = self.sink['cache']
		self.setWriter(name)
		return self

	def initSink(self, sink: str, snkt: str='database', name: str='base'):
		'''Set the active database in which to store data
		sink: data storage resource to be used for storage
		nkt: data storage type
		name: data storage resource name'''
		self.sink = self.setResource(sink, snkt, {}, name)
		if not self.cache:
			self.cache = self.sink['cache']
		self.setWriter(name)#  maybe autosetting the writer isn't a good idea
		return self

	def setWriter(self, name):
		'''Set the active sink to write to
			name:
		'''
		self.wrtr = self.sink[name.lower()]['store'].write
		return self

	def setResource(self, rsrc, srct='database', arsrc: dict={}, name='base'):
		'''Define resources for molecular engines to be used as sources and
			sinks for working with data in the system of modules'''
		if name not in arsrc.keys():
			arsrc[name] = {}
		#currently no path for handing a dataframe directly as a resource
		#
		arsrc['cache'] = conql.doc(rsrc)#what is this accomplishing?
		arsrc['cache'].store[name] = {}
		arsrc[name]['type'] = srct
		if srct in ('thing', 'object', 'thingify', 'funcify'):
			arsrc[name]['store'] = thing.thingify(rsrc)#									||
		elif srct in ('methodify', 'method'):#Turn string arguments into class function access
			arsrc[name]['store'] = getattr(self, rsrc)
			arsrc[name]['path'] = 'self'
		elif srct in ('database', 'db'):
			arsrc[name]['store'] = sonql.doc(rsrc)
			arsrc[name]['path'] = rsrc
		elif srct in ('cache', ):
			arsrc[name]['store'] = arsrc['cache']#this is becasue a default cashe resource doesnt' have a store
			arsrc[name]['path'] = rsrc
		elif srct in ('dataframe'):#this is hacked in for now
			arsrc[name]['store'] = rsrc
		else:
			print('Resource Not Found', srct)
		return arsrc

	def yieldBreak(self, data, table=None, pagesize=None):
		''' '''
		return yieldBreak(data, table, pagesize)

def bldDocs(doctype, name, options, noptions, inc):
	''' '''
	if doctype == 'audio':
		self.bldAudio(name, options, noptions, inc)
	elif doctype == 'file':
		self.bldFiles(name, options, noptions, inc)
	elif doctype == 'fs':
		self.bldFileSystems(name, options, noptions, inc)
	elif doctype == 'image':
		self.bldImages(name, options, noptions, inc)
	elif doctype == 'table':
		self.bldTables(name, options, noptions, inc)
	elif doctype == 'video':
		self.bldVideos(name, options, noptions, inc)
	elif doctype == 'view':
		self.bldViews(name, options, noptions, inc)

def bldAudio(self):
	'''Build audio files from a tmplt and fill data'''
	#need to develop a structure for audio templating
	#essentially providing a layer of tracks
	return

def bldFiles(self, name, tmplt, options):
	'''Build files from tmplt and fill data leverage various tools to
									properly format the document type'''#	||
	#write tables out to excel
	#write dictionary out to json/yaml/xml/cherrytree
	#format json ipynb
	doc = subtrix.mechanism(tmplt, options).run()[0]
	self.stor.write(doc)
	return self

def bldFileSystems(self, node, tmplt, options):
	'''Build a file subsystem from a tmplt and fill data'''
	for tmplt in self.tmplts.keys():
		path = node
		for dir in tmplt.keys():
			self.stor.write(f'{path}{dir}')

def bldImages(self, doctype):
	'''Build images from a tmplt and fill data'''
	#need to substitute color palattes
	#extract tmplt color palette
	#use a nearest algorithm to substitute from the provided color palette
	return

def bldTexts(self):
	'''Build text from tmplts and/or mtmplts and data'''
	return self

def bldTables(self, docs):#												||
	'''Build tables from tmplts and/or mtmplts and data'''
	for table in self.tmplts:#												||
		sqlcfg = {'tables': [table]}#										||
		while True:#														||
			data = next(self.dbo0.read(sqlcfg))#							||
			records = data.dikt[table]['records']#							||
			columns = data.dikt[table]['columns']#							||
			if data.go == False:#											||
				break#														||
			records = self.renameColumns(records, columns)#					||
			records - self.cleanData(records)#								||
			records = self.addTableColumns(records)#						||
			d = {table: {'records': records, 'columns': columns}}#			||
			self.stor.write(d)#												||
	return inc

def bldVideos(self, doctype):
	'''Build videos from a tmplts and/or mtmplts and data'''
	#need to develop a structure for video templating
	#essentially providing frames
	return

def bldViews(self, doctype, name, tmplt, options, inc=0):
	'''Create document from tmplts and/or mtmplts and data'''
	terms = next(self.data, None)#											||
	if terms == None:
		return inc
	for term in terms['options'].keys():
		if term != 'OR':
			options[term] = self.data['options'][term]
	fills = calctr.stuff(options).multiplex().it
	for fill in fills:#														||
		wrdata = {}
		doc = subtrix.mechanism(tmplt, fill).run()[0]
		edits = self.monk.dikt['DocTypes']['sql']['view']['edits']
		for find, replace in edits.items():
			if find in doc:
				doc = [doc.replace(find, replace),]
		wrdata[f'{view}{inc}'] = doc
		self.stor.write({'views': wrdata})
		inc += 1

def yieldBreak(data, table=None, pagesize=None):
	'''Utility for testing an empty yield'''
	if isinstance(data, DataFrame):
		if data.empty:
			if log: print('Data is empty DataFrame')
			return True
		if pagesize != None:
			if data.shape[0] < pagesize:
				if log: print('Data is DataFrame smaller than pagesize')
				return True
	elif isinstance(data, object):
		if data == None:
			if log: print('Data is None Object')
			return True
		elif 'df' in data.__dir__():
			if data.df.shape[0] == 0:
				if log: print('Data is object with single dataframe attribute .df')
				return True
		elif 'dfs' in data.__dir__():
			if table == None:
				table = list(data.dfs.keys())[0]
			if isinstance(data.dfs[table], DataFrame):
				if data.dfs[table].empty:
					if log: print(f'Data is object with multi dataframe attribute .dfs but {table} dataframe is empty')
					return True
				if pagesize != None:
					if data.dfs[table].shape[0] < pagesize:
						if log: print(f'Data is object with multi dataframe attribute .dfs but {table} dataframe is smaller than pagesize')
						return True
		elif 'sinkdfs' in data.__dir__():
			if table == None:
				if len(data.sinkdfs.keys()) > 0:
					table = list(data.sinkdfs.keys())[0]
				# else: Timing of sinkdfs reset is problematic
				# 	return True
			if log: print(f'Table {table} Data {data.sinkdfs.keys()}')
			if table not in data.sinkdfs.keys():
				if log: print(f'Data is object with sinkdfs but {table} not in dict')
				return True
			if isinstance(data.sinkdfs[table], DataFrame):
				if data.sinkdfs[table].empty:
					if log: print(f'Data is object with sinkdfs but {table} DataFrame is empty')
					return True
				if pagesize != None:
					if data.sinkdfs[table].shape[0] < pagesize:
						if log: print(f'Data is object with sinkdfs but {table} DataFrame is smaller than pagesize')
						return True


#==============================Source Materials=================================||
'''

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
