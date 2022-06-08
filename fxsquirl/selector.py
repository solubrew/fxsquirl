#@@@@@@@@@@@@@@@@@@ Pheonix.Molecules.Selector.Selector @@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: dde7fdeb-77c7-404d-bfc8-19b303d2b2f4
	name: Selector
	description: >
		Extract dataset and create tables of folded subdatasets

		Progressively sample images to remove in SEC to keep the
		longest history within the space constraints leaving the
		newest items more dense figure out a way to manage the curve
		of this density in the alogrythm....take presampled time and
		count information into the algorythm use the statistical
		sampling function to select pictures to keep over the life
			can i limit the amount of time spent folding?
			def origami(self, shape='envelope'):#fold out dataset in varous ways
				mn, mx, sc, subsize = [0.000000001, 0.999999999, 32, 5]#
				lendrw = len(self.data.()) look at syntax of 3rd and 4th dimensional data frames
				optimal(mn,mx,score).dikt#X-Dimensional Folded Datasets
				analyzer.engine(self.subset_data).compare()
				show.show(self.vector0).terminal(here).code('debug')
				mapping = self.vector1['folds']#factor out each row grouping....or variable folding compares
				self.vectorizedtree = categorizer.engine(self.data).vectorize(mapping).dikt#if there are categorical variables then tree based them and then sample from those groups
				self.z = selectdraws(self.data)
				self.score(self.vectorizedtree)
		check folds as i go but need a way to address folds
		{50:[0,1,5,8],350000:[]}
		also need to be able to select from database by parameters and search
		features and a specific selection criteria need to be tracted just like
		a collection
		create _procdata style function to relocate a large part of the
		foldDataSets function internal to selector allowing for that selection
		to be written to a database directly
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>/panda/LEXI/LEXI.yaml
	outline:
	expire: <^[expire]^>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===========================Core Modules================================||
from os.path import abspath, dirname, join
import sys, os, datetime as dt, math, operator, uuid, shutil, gc, time#		||
from decimal import Decimal#											||

import shutil
#===========================3rd Party Modules===========================||
from requests import get, Request, Session
from pandas import DataFrame, concat
try:
	from sklearn.model_selection import StratifiedKFold
	from sklearn.model_selection import StratifiedShuffleSplit
except:
	print('No SKLearn Module')
#=======================================================================||
from condor import condor#								||

from excalc import data as calcd

from fxsquirl import builder
from fxsquirl.orgnql import fonql
#=======================================================================||
here = join(dirname(__file__),'')#						||
there = join(dirname(__file__))
where = abspath(join('..'))#							||set path at pheonix level
module_path = abspath(join('../../../'))
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
pxcfg = join(abspath(here), '_data_/selector.yaml')#									||use default configuration
class engine(builder.engine):
	''' '''
	def __init__(self, cfg={}):#	||
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#				||load configuration file
		builder.engine.__init__(self, self.config)
		self.session = self.config.ppov#										||
		self.table = None
		self.initWebSession()

	def datasplits(self, data, splits=None, folds=None, cycdb=None):
		''' '''
#		self.dataGNR = store.stuff(data)#								||Read from the dbase or fs etc
		self.data = data
#		self.kind = self.dataGNR.kind
		if folds == None:#												||
			folds = self.config['folds']#								||
		self.folds = folds#
		if cycdb == None:#
			cycdbl = self.config['cycleDB']['loci']#					||
			cycdbn = self.config['cycleDB']['name']#					||
			dtid = thing.when().dtid#									||
		self._setup()#													||
		self._loadMethods()#											||
		return self

	def extractDataSet(self, table, name):
		'''is extraction via a seperate dataset really needed? not all dataset
			columns have an equivalence in the dfs tree'''
		if name not in self.cache.store['extracts'].keys():
			print(f'Dataset not initilized for {name} initialized sets {extracts.keys()}')
			return self
		extracts = self.cache.store['extracts']
		for name in extracts.keys():#			||add extracted data to dataset
			dset = extracts[name]
			keyd = None
			if name in self.cache.store.iterkeys():
				keyd = self.cache.store.pop(name)#create a reference to the current data
			if isinstance(dset, DataFrame):
				for col in dset.columns:
					if col in self.cache.store[table].columns:#						||
						dset[col] = self.cache.store[table][col]
					else:
						dset[col] = None
				if isinstance(keyd, DataFrame):# if the data that was already at this key is a a dataframe try to concat...will have issues related to column specifications
					dset.concat(keyd)
				self.cache.store[name] = dset
			elif isinstance(dset, dict):
				for dkey in dset.keys():
					if isinstance(dset[dkey], set):#				||
						dset[dkey].update(self.cache.store[table][dkey])#		||
						if isinstance(keyd, set):
							dset[dkey].union(keyd)
						if isinstance(keyd, list):
							dset[dkey].update(keyd)
					elif isinstance(dset[dkey], list):#					||
						dset[dkey] += self.cache.store[table][dkey].tolist()
						if isinstance(keyd, (list, set)):
							dset[dkey] += keyd
					elif isinstance(self.cache.store[table][dkey], int):
						pos = len(self.cache.store[table][dkey]) - 1
						dset[dkey] = self.cache.store[table][dkey][pos]
					self.cache.store.pop(dkey)
					self.cache.store[dkey] = dset[dkey]
		self.cache.store['extracts'] = extracts
		return self

	def fold(self, foldtype='SimpleFold', how='perc', inc=0, name='base'):
		'fold data in sequence with an overlap equal to inc'
		if foldtype == 'SimpleFold':#											||A simple fold creates data subsets with or without overlap
			for x in self.foldedMTHDs:
				if self.foldedMTHDs[x]['Name'] == foldtype:
					method = self.foldedMTHDs[x]
			subgroupsize = method['Data']['SubGroupSize']
			foldsize = method['Data']['DataSetCoverage']*self.datasize
			folda = self.df[0:foldsize]
			foldb = self.df[foldsize:datasize]
			self.sample, r0, r1 = [], 0, 0
			for s in range(self.n_samples):
				l = self.n_samples * self.ssize
				sample = []
				r1 = r0 + self.ssize - inc
				for number in range(r0, self.ssize+r0):
					sample.append(number)
				self.sample.append(sample)
				r0 = r1
		elif foldtype == 'StratifiedKFold':#									||A stratified fold creates subsets by some exclusive charateristic that is filtered upon
			args = {'n_folds': self.num_samples, 'shuffle': True,'random_state': 67}#	||
			args0 = {'n_splits': splits, 'shuffle': True,'random_state':42}#	||
			self.folds = StratifiedKFold(y_split, **args)#						||
		elif foldtype == 'StratifiedShuffleSplit':#								||
			args = {'n_splits': splits, 'random_state': 42,'test_size': 2}#		||
			self.folds = StratifiedShuffleSplit(**args)
		elif foldtype == 'RandomSelection':#									||A random selection creates subsets with no regard to order
			if how == 'perc':
				if log: print('SOURCEDFS', self.source)
				dset = self.source[name]['data'].sample(frac=0.6666666, random_state=200)
			elif how == 'filtr':
				dset = self.source[name]['data'][df.iloc[:,3]=='validation']
			self.dset0, self.dset1 = dset, self.source[name]['data'].drop(dset.index)
		return self

	def getColumns(self, columns):
		'''Use to select specific columns from a dataset and create a new table
			with those columns '''
		for column in columns:
			if column in table:
				ntable[column] = table[column]
			else:
				ntable[column] = newcolumn()
		return ntable

	def getEP(self, params: dict={}, links: list=[], maplinks: list=[],
									name='base', altercols={}, psize=100000):#	||
		'''Yield end point data given parameters
			how to handle non web endpoints like going through the
			uniswap source connected to the ethereum web3 portal
			a function is called directly that is build to access the
			data from the correct contract using the proper functions'''
		data = self._request(self.ep.format(**params))
		if log: print('EP Data', data)
		load = [data, links, maplinks, name, altercols, psize]
		status = self.buildMappedTable(*load)
		return status

	def getLastEntry(self, table):
		configs = {'subperiod': self.subperiod,'window': self.window,}
		self.assignConfigs()
		if not isinstance(thing, object):
			thing = thing.timser.thing(thing)
		self.thing = thing
		self.subperiod = subperiod

	def initExtract(self, columns, output='set', name='base'):
		'''Define containers for storage of data extracted during selector
			activity.  This data will be stored under the dataset attribute
			as a dictionary of keys and values.  This data is to be used to
			provide information to an outside process in this regard the data
			is appended according to the rules of the container type'''
		extracts = {}
		if 'extracts' in self.cache.store.iterkeys():
			exctracts = self.cache.store['extracts']
		if not isinstance(columns, list):
			columns = [columns]
		if output == 'dataframe':
			extracts[name] = DataFrame(columns=columns)
		else:
			named = {}
			for col in columns:
				if output == 'set':
					container = set()
				elif output == 'list':
					container = []
				elif output == 'item':
					container = 0
				named[col] = container
			extracts[name] = named
		if log: print('INIT Extracts', extracts)
		self.cache.store['extracts'] = extracts
		return self

	def initSource(self, src, srct='database', name='base'):
		'''Set a resource as source for data selection'''
		if log: print('Source Name', name)
		self.source = self.setResource(src, srct, {}, name)
		if not self.cache:
			self.cache = self.source['cache']
		return self

	def initWebSession(self):
		self.websession = Session()#											||
		self.headers = {}
		if 'api' in self.config.dikt.keys():
			if 'headers' in self.config.dikt['api'].keys():
				self.headers = self.config.dikt['api']['headers']#						||changed this from web to api
		if 'web' in self.config.dikt.keys() and self.headers == {}:
			if 'headers' in self.config.dikt['web'].keys():
				self.headers = self.config.dikt['web']['headers']
		self.websession.headers.update(self.headers)#							||
		return self

	def postEP(self):
		'''#integrate with self.WebSession _request and error handling '''
		r = requests.post(url, json=body, headers=headers, timeout=timeout)

	def randomed(self, vsize, data, size, subsize, replacement=None):
		'select a random data point with or without data point replacment'
		self.pop = describPopulation(data)
		self.subgroup = {}
		self.subgroup['id'] = 0
		self.subgroup['size'] = subsize
		uppersub = int(subsize/2)
		if subsize%2 == 0:
			lowersub = uppersub
		else:
			lowersub = uppersub + 1
		strategy = {}
		for i in range(size):
			strategy[i] = {}
			number = random().between(0,pop['size']).num
			for j in range(lowersub):
				self.strategy[j] = number-lowersub+j
			for k in range(uppersub):
				self.strategy[j+k] = number+k
		self.sdata = mapSample(data, self.strategy)
		self.samp = describeSample(self.sdata)
		l, self.sample = [self.n_samples * self.ssize, []]
		if vsize == 1:
			self.sample = [[0, ],]
			return self
		used, number = [[None], None]
		for s in range(self.n_samples):
			sample = []
			if replacement == 1:
				used = []
			for i in range(self.ssize):
				if replacement == 2:
					used = []
				while number in used:
					number = num.thing().between(0, l).it
				sample.append(number)
				used.append(number)
			self.sample.append(sample)
		return self

	def sanitize(self, data):
		if isinstance(data, list):
			data = [x for x in data if x != '']
		return data

	def search(self, term):
		'''Run Selector Engine and search through given data source '''
		if isinstance(self.data, str):
			if path.exists(self.data):
				sfs = fonql.doc(self.data).read()
				while True:
					data = next(sfs, None)
					if data == None:
						break
					with txtonql.doc(f) as doc:
						doc.write(data)
		return self

	def setHandler(self, type, fx):
		''' '''
		if type == 'HTML':
			pass
		return self

	def setReader(self, load, name='base', altercols={}):
		'''Setup reader in a database this is setting the table and any filters
		 	for the select statement, need to work in the ability to read from
			an network based endpoint as well
			should use the srctype to drive this...need to add to resource data
			'''
		if log: print('Set Reader', name, 'SOURCE', self.source)
		if log: print('Reader Parameters', load)
		if self.source[name]['type'] in ('database', 'db', 'fullcache'):
			if 'table' in load.keys():
				self.table = load['table'][0]
			elif 'view' in load.keys():
				self.table = load['view'][0]
			filtrs = load.pop('filters', {})
			if filtrs != {}:
				if 'GREATER' in filtrs['WHERE'].keys():
					for key in filtrs['WHERE']['GREATER']:
						if key not in self.last.keys():
							self.last[key] = self.getLastSink(self.table)
			self.rdr = self.source[name]['store'].read(load, filtrs)
		elif self.source[name]['type'] in ('method', 'methodify'):
			self.rdr = self.source[name]['store'](**load)
		else:
			if log: print('Source Type', self.source[name]['type'])
			if log: print('Reader not set for', name, self.source[name]['store'])
		return self

	def _loadMethods(self):
		''
		self.foldedMTHDs = self.config['methods']['folded']
		self.polarMTHDs = self.config['methods']['polar']
		self.structuredMTHDs = self.config['methods']['structured']
		self.stratifiedMTHDs = self.config['methods']['stratified']
		self.randomedMTHDs = self.config['methods']['randomed']
		self.windowedMTHDs = self.config['methods']['windowed']
		return self

	def _request(self, url: str, cnt: int=0, maxtries: int=10):
		'''Get json string data from url based endpoint and convert to dict
			review youtube download module and see if there are implmentaitons
			i can use for ensure better downloads
			should break actual request out so that it can be parallelized
			as well as run a watcher process to kill it or reset it after a
			period of time or when certain triggers are hit '''#	||
		params = {}#self.parameters.it
		while True:
			cnt += 1
			try:
				if log: print('Request URL', url)
				data = self._validate(self.websession.get(url, params=params))
				#if log: print(f'Hit {cnt} End Point {url} Returned {data}')
				if data == 'SLOW':
					print(f'SLOW {cnt}')
					time.sleep(5*cnt)
					continue
				elif data == 'XSLOW':
					print(f'XSLOW {cnt}')
					time.sleep(30*cnt)
					continue
				break
			except Exception as e:
				if log: print(f'Request Failed on try {cnt} due to {e}')
				if 'JSONDecodeError' in str(e):
					data = None
					break
				time.sleep(2**cnt)
			if cnt > maxtries:
				break
		return data

	def _setup(self):
		''
		dtid = thing.when().dtid
		unq = thing.what().uuid().ruuid[-5:]
		name = f'CYCL{unq}'
		path = f'{name}/{dtid}_{name}.sqlite'
		return name

	def _subsize(self, subsize=None):#									||
		'for each data dimension calculate a sample group sizes'#		||
		if subsize != None:#											||
			self.sets = self.kind#										||
		dimensionalities = self.kind.dimesionality()#					||find dimensions of data
		for vector in self.address.keys():#								||
			vsize = self.data.shape[vector]#							||
			if vsize == 1:#												||
				self.ssize = 1#											||
				self.n_samples = 1#										||
			else:#														||
				self.ssize = self.findSubSize(subsize, vsize)#			||
				if self.ssize == 0:#									||
					self.ssize = 1#										||
				self.n_samples =  num.thing(vsize/self.ssize).down()#	||
			self.handler(vsize)#										||
			self.address[vector] = self.sample#							||
			calcs.stuff(self.data, self.kind).optimalSubSize()
		return self#													||


def imgGRAB(src, type='video'):
	''' '''
	if type == 'video':
		cap = cv2.VideoCapture(self.it)
		while(cap.isOpened()):
			if naming == None:
				name = next(thing.when().gen())
			ret, frame = cap.read()
			if ret == False:
				break
			imwrite(f'{path}/{name}.jpg',frame)
		cap.release()
		cv2.destroyAllWindows()
	return self


def webGRAB(path, params=None, cfg=None):
	''' Get Infromation from a Webpage'''
#	if log: print('HTML requests')
	stringify = {}#												||
	if params != None:
		for key, options in params.items():#					||
			d2s = calcd.stuff(options).list_2_str(None, 2).it#	||
			stringify[key] = d2s
		url = subtrix.mechanism(path, stringify).run()[0]#			||
	else:
		url = path
	url = url.replace(' ','')
	doc = next(monql.doc(url).read())
	tables = extractTables(doc)
	webo = tables
	return webo


def webImageGrab(url, path):
	response = get(url, stream=True)
	fonql.touch(path)
	with open(f'{path}', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response


def webSTORE(path, params, cfg=None):#							||
	'''Save Webpage as a PDF, or html page'''#										||
#		if cfg['intype'] == 'JSON':#									||
	try:
		self.dikt = doc.dikt#									||
	except Exceptions as e:
		if log: print('HTML',e)
	if self.dikt == {}:
		if cfg['intype'] == 'HTTP':
			if cfg['outtype'] == 'PDF':#							||
#				if log: print('CFG output PDF',cfg)
				if site == None:#									||
					site = self.source#								||
				if out == None:#									||
					out = self.store().outfile#						||
				try:#												||
					pdfkit.from_url(site, out)#						||
				except:#											||
					pass#write site to another list for different tools to be used for collection
			else:
				try:
					self.soup = doc.soup#							||
				except Exception as e:
					if log: print('Soup Grab Failed',e)
	return self#													||


#uuid = thing.what().uuid().ruuid[-5:]
#fp = open('selector__procData{0}.memlog'.format(uuid), 'w+')
#@profile(stream=fp)
def procDataExtract(db, cfg, columns):
	''' '''
	tables = cfg['tables']
	if len(tables) <= 1:
		table = tables[0]
	dbo = sonql.doc(db)
	datar = dbo.read(cfg)
	tTARGs = None
	while True:
		data = next(datar, None)#												||get valid fold
		if data == None or data.dikt[table]['records'] == []:
			break
		trainRs = DataFrame(data.dikt[table]['records'],
										columns=data.dikt[table]['columns'])#	||
		TARGs = calcd.stuff(trainRs).grabColumns(columns)
		if tTARGs is None:
			tTARGs = TARGs
			continue
		tTARGs = concat([tTARGs, TARGs])
		del TARGs
		gc.collect()
	return tTARGs


def procDataFold(db, table, tag=None):
	'''Process datafold across data source pages'''
	drops = ['creby', 'creon','modby', 'modon', 'dlt','actv']
	with sonql.doc(db) as dbo:
		rdr = dbo.read({'tables': [table]})
		cnt = 0
		while True:
#			if log: print('Count',cnt)
			cnt += 1
			data = next(rdr, None)
			if data == None:
#				if log: print('Break on cycle', cnt)
				break
			df = DataFrame(data.dikt[table]['records'],
										columns=data.dikt[table]['columns'])#	||
			for col in drops:
				df.drop(col, 1, inplace=True)
			fd = engine(df).fold('RandomSelection')
			del df
			with sonql.doc(db) as dbi:
				dbi.write({f'{tag}_train': {'columns': fd.dset0.columns,#		||
														'records': fd.dset0}})#	||
				dbi.write({f'{tag}_valid': {'columns': fd.dset1.columns,#		||
														'records': fd.dset1}})#	||
			del fd
			gc.collect()
	return tag#

#==============================Source Materials=================================||
'''

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
