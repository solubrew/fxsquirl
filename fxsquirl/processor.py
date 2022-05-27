#@@@@@@@@@@@@@@@@@@@@@@@@Pheonix.Molecules.Processor@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: ''
	name:
	description: >
		implement the use of numba and cuda to wrap all elements,
		fxsquirlcules, and Organisms level functions for parallization
		as possible by inherient breakdown of the function
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>
	outline:
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*
#===============================================================================||
from os.path import abspath, dirname, join
import datetime as dt, queue as q, time
import inspect
#===============================================================================||
from pandas import concat, DataFrame
#===============================================================================||
from condor import condor
from fxsquirl import builder, validator
#===============================================================================||
here = join(dirname(__file__),'')#								||
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = join(abspath(here), '_data_/processor.yaml')#								||use default configuration
class engine(validator.engine):
	''' '''
	version = '0.0.0.0.0.0'
	def __init__(self, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#						||load configuration file
		builder.engine.__init__(self, self.config)
		validator.engine.__init__(self, self.config)

	def apply(self, column_name: str, fx: str):#				||
		'''Apply function defined within class that accepts a 1xN dataset and
			return a 1x1 dataset to the processor dataset how to identify the
			correct function that could be within this class or other classes?
			add stats as a part of the class'''#				||
		return getattr(self, fx)(self.source[src]['data'][column_name])#		||

	def applyFX(self, srs, fx: dict={}, name='base'):
		'''Perform function on data within each division node such as averaging
			of values within the box need to pushc this all over to collector'''
		srs.apply(fx)
		return srs

	def applyFX_a00(self):
		if isinstance(self.source[src]['data'], dict):
			for ts, df in self.source['base'].items():
				if isinstance(df, DataFrame):
					columns = df.columns
					record = [ts]
					for col in columns:
						if col in fxmap.keys():
							record.append(self.apply(col, fxmap[col]))
					records.append(record)
			self.df = DataFrame(records, columns=['date'] + list(fxmap.keys()))
		records, columns = [], []
		for ts, df in self.tbox.items():
			if isinstance(df, DataFrame):
				#print('DF', df.head())
				columns = df.columns
				record = [ts]
				for col in columns:
					if col in fxmap.keys():
						record.append(analysis.apply(col, fxmap[col]))
				records.append(record)
		self.df = DataFrame(records, columns=['date'] + list(fxmap.keys()))
		return self

	def mapData(self, map):
		''' '''
		return self

	def mapFX(self, map):
		''' '''
		return self

	def pageDB(self, table: str, column: str, name='base'):
		'''Page through database table for parameters from the given database
			and table'''
		if log: print('Source', self.source)
		rdr = self.setReader({'table': table}, name)
		while True:
			data = next(rdr, None)
			if self.yieldBreak(data):
				break
			yield list(data.dfs[list(data.dfs.keys())[0]][column])


	def pageEP(self, spage: int=0, npages: int=0, step: int=0, params: dict={}, links: list=[], maplinks: list=[]):#	||
		'''Get data from endpoint 1 page at a time...used in coingeckoSRC'''
#		print('MERGE Parameters', params)
		for key, val in params.items():#this is forcing an override due to some failure in the override function
			self.parameters.it[key] = val
		self.parameters.merge(params, None, ':::ROOT:::', 'override')
		params = self.parameters.it
		page = spage
		params['offset'] = step
		name = 'base'
		while True:
			params['page'] = page
			self.getEP(params, links, maplinks)
			#print(self.dfs.keys())
			if self.yieldBreak(self.dfs[name], None, step):
				break
			yield self
			self.df = DataFrame()
			page += 1
			params['offset'] = step
		yield None
	def process(self, reader, load, params={}, extract=[]):
		''' '''
		for name, actions in load.items():
			self.setReader(params, reader)
			self.initExtract(*extract)
			self.collect(name)
		return self
	def processEP(self, ep, options=[], params={}, altercols={}):
		''' '''
		cfgs = self.config.dikt['endpoints'][ep]
		params = merge(self.config.dikt['params'], cfgs['params'])
		for option in cfg['options'].keys():
			if options != [] and option not in options:
				continue
			try:
				map = cfgs['options'][option]['map']
			except Exception as e:
				map = cfgs['map']
			self.buildEndPoint(cfgs['seq'], 'seq')
			page, params['offset'] = spage, step
			while True:  #this pages the
				params['page'] = page
				params['links'] = [ep, option]#pathlinks access configurations
				outPath = ['result']#pathlinks to access returned data
				#altercols maps returned data columns to a new column names
				#name is to address the resulting data
				self.getEP(params, outPath, [], name, altercols)
				if self.yieldBreak(self.dfs[name], None, step):
					#print('Process EP break')
					break
				yield self
				page += 1
				params['offset'] = step
				if page > 50:
					break
	def _processPayload(self, payload):
		'''Process given data breaking down by database storage needs across
			inmem and ondisk databases'''
		self.data = []
		return self
def _procData(cfg, params, dbo, dbi, fx, targs, filtr, ftrs=None, limit=None):
	'''Process Data Against generator engine utilzing rules and templates to
		output a batch of files and/or data entries'''
	rdr = dbo.read(cfg)
	while True:
		dataSET = next(rdr, None)
		if dataSET == None:
			break
		data = mapData(dataSET)
		for tmplt in tmplts:
			subtrix.mechanism(tmplt, data)
def _procDataTransform():
	'''Transform dataset into its most usable version for applying training
		i.e.
			convert purchase count to a percentage of the max value?
			convert event days using ohe
			convert weekday using ohe
			convert state using ohe
			convert store_id using ohe
			convert cat_id using ohe
			convert item_id using ohe


		think about creating a general processor engine that
		can be used to page through databases it seems i am reusing this
		pattern often....need the ability to dynamically call the object
		to be processed
	'''
	drops = ['creby', 'creon','modby', 'modon', 'dlt','actv']
	page = 1000000
	cfg['transcols'] = {'weekday': {'transform': 'ohe', 'cats': []},
						'state_id': {'transform': 'ohe', 'cats': []},
						'event_name_1': {'transform': 'ohe', 'cats': []},
						'event_name_2': {'transform': 'ohe', 'cats': []},
						'store_id': {'transform': 'ohe', 'cats': []},
						'cat_id': {'transform': 'ohe', 'cats': []},
						'dept_id': {'transform': 'ohe', 'cats': []},
						'num_sold': {'transform': 'percent_max', 'cats': []}}
#						'item_id': {'transform': 'ohe', 'cats': []},
	table = 'sales_train_evaluation'
	rdr = sonql.doc(db).read({'views': [table], 'page': page})
	t = 'transform_train_data_{0}'.format(thing.what().uuid().ruuid[-5:])
	enc = encoder.engine()
	'''
	 	when trying to find the possible values of a column from a paged table
		there is a strong possibility of not getting every option in each page
		then the table will have to be paged once in order to find all options

		need to combine event_name 1 and 2
		need to combine event_type 1 and 2

		when limiting the number of categoires in ohe how to find those with the
		lowest data for grouping to the other category?

	'''
	cnt = 0
	while True:
		data = next(rdr, None)
		if data == None:
			if cnt == 0:
				rdr = sonql.doc(db).read({'views': [table], 'page': page})
				cnt += 1
				continue
			else:
				break
		df = DataFrame(data.dikt[table]['records'],
										columns=data.dikt[table]['columns'])#	||
		maxv = -100000000000000000000000
		for col in cfg['transcols']:
			if col not in df.columns:
				continue
			if cnt == 0:
				if cfg['transcols'][col]['transform'] == 'ohe':
					cats = cfg['transcols'][col]['cats']
					print('Get Categories from Column', col)
					ncats = [x for x in list(df[col].unique()) if x not in cats]
					cfg['transcols'][col]['cats'] += ncats
				elif cfg['transcols'][col]['transform'] == 'percent_max':
					max = df[col].max()
					print('Max', max)
					maxv = float(maxv) if float(maxv) > float(max) else float(max)
					cfg['transcols'][col]['max'] = maxv
			else:
				print('Transform Column', col)
				if cfg['transcols'][col]['transform'] == 'ohe':
					print('Run OHE', df[col])
					data = enc.ohe(df[col], cfg['transcols'][col])
					print('New Col', data[0])
					df.drop(col, 1, inplace=True)
					ncols = ['{0}_{1}'.format(col, x) for x in range(len(data[0]))]
				elif cfg['transcols'][col]['transform'] == 'percent_max':
					print('Run Percent Max')
					#use the dataframe/series apply method to create new column?
					data = enc.pctmax(df[col], cfg['transcols'][col])
					df.drop(col, 1, inplace=True)
					ncols = ['pmax_{0}'.format(col)]

				ndf = DataFrame(data, columns=ncols)
				for ncol in ncols:
					df[ncol] = ndf[ncol]
		if cnt == 0:
			continue
		with sonql.doc(db) as dbi:
			data = calcd.df2lists(df)
			dbi.write({t:{'records': data, 'columns': df.columns}})
