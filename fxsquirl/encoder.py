#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '4acbaf2d-ad28-43c2-9dab-2e8dd25b994c'
	name: Encoder - Envious Elk
	description: >
		Define text encoding vs dat encoding techniques and where they
		cross

		leverage heavily the rule system and integrate the ctrlr
		to create tools for jinja and other template framework compatibilities
		also use for the encoding of sensitive information to
		UUID type data and other general obscurity needs

	expirary: <[expiration]>
	version: <[Version]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
import datetime as dt, re, shutil, sys
from os.path import abspath, dirname, join
from collections import namedtuple, OrderedDict
from types import GeneratorType
#=================================3rd Party Modules=============================||
from pandas import DataFrame, to_datetime
from numpy import finfo, iinfo, int8, int16, int32, int64, float16, float32
from numpy import float64, ndarray, object, save
from io import BytesIO
#===============================================================================||
from condor import condor#										||
from excalc import data as calcd, tree as calctr, exam#											||
from fxsquirl.orgnql import sonql
from fxsquirl import selector
#===============================================================================||
here = join(dirname(__file__),'')#												||
log = False
#===============================================================================||
pxcfg = join(abspath(here), '_data_/encoder.yaml')#								||use default configuration

class engine(selector.engine):#															||
	'''Scan data, determine possible encoding strategies and implement them
		based on configurations and analysis scoring to achieve the best feature
		encodings
		build out one of the primary encodings as turning data into db tables and back
		caring the tags to accomplish through the function chain		'''

	def __init__(self, data=[], cfg=None):#							||=>Initialize class instance
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#						||
		selector.engine.__init__(self, self.config)
		if not isinstance(data, DataFrame):
			data = DataFrame(data)
		self.data = data

	def autoEncoding(self, expand_cols):#										||
		''' '''
		for col in expand_cols:#												||
			sumthd = self.decideSummarization()#								||
			if sumthd == 'one-hot encoding':#									||
				self.ndata.extend(self.ohe(self.data[col]))#					||
		return self#															||

	def binarize(self, column='Target', activate=0, name='base'):#							||
		'''turn each category into a new binary column'''
		df = self.source[name]['store']
		self.out = df[column].apply(binarize, args=(activate,))
		print('Binarize Out', self.out)
		return self

	def binner(self, activations):#												||
		'''activations = dikt() '''
		for p in self.data:#													||
			cnt = 0#															||
			for i, j in activations:#											||
				cnt += 1#														||
				if p >= i and p <= j:#											||
					self.out.append(cnt)#										||
					break#														||
		return self#															||

	def check_exception(text, exceptions, s_exceptions):
		''' '''
		lock = 0
		for exception in exceptions:
			if exception in text:
				lock = 1
		for exception in s_exceptions:
			if exception in text[:len(exception)]:
				lock = 1
		return lock

	def combine(self, adds, common=None):
		''' '''
		for add in adds:
			self.pool.apply_async(self.procCombine(add))
		self.kind = exam.thing(self.ndata).kind#need to build the examination from the
		#known kinds for speed but reanalyzing is more accurate
		return self

	def count(self, coldat):#									||
		'''Calculate count data from given data'''
		counts = calcd.thing(coldat).counts#							||
		return self#													||

	def dataType(self):
		''' '''
		self.categoricals = self.selectCols('discrete', 'datatype')#	||
		self.variables = self.selectCols('continous', 'datatype')#		||
		self.drops = self.selectCols('drop', 'datatype')
		return self

	def expand(self, guide=None, method='filesystem'):
		'''Find known items and expand using a known method
			implement interpolation and extrapolation techniques here
			by leveraging the generator module to fill in missing values or
			extend data sets'''
		if guide == None:
			self._performSearch()
		method = self.config['method']['expand'][method]
		path += '/'+dik
		for dik in dikt.keys():
			for x in method['finder']['keys']:
				if x in dik:
					lock = False
				philedikt = {}
				for phile in dikt[dik]:
					philedikt[phile] = next(store.stuff(path+'/'+phile).read()).dikt
				dikt[dik] = philedikt
			for x in method['finder']['values']:
				if x in dikt[dik]:
					lock = False
				philedikt = {}
				for phile in dikt:
					pass
			else:
				dikt[dik] = expand(dikt[dik], dik, path)
		return dikt

	def feedback(self, data, params=None, cfg=None):#					||
		'Implement feedback loop from metrology to predictology'
		if params == None:#												||
			params = self.cfg['params']#								||
		self.goal = params['goal']#										||
		self.actrtr()#													||

	def frequency(self):
		''' '''
		pass

	def knowns(self, categories=['New','Old']):
		'''knowns allows for a connection to categories inwhich to interact'''
		self.knowns = categories
		return self

	def mapp(self, address):
		''' '''
		nd, nvectors, crystal = [self.data, len(address.keys()), {}]
		qube = [[] for i in range(nvectors)]
		for vector, samples in address.items():
			for sample in samples:
				qube[vector] = sample
		self.qube = qube
		return self

	def numerize(self):#														||
		''' '''
		self.unique = {}#														||
		for dim in self.categoricals.keys():#									||
			data = calcd.thing(self.data[dim]).go()#							||
			self.cats[dim] = data.subset#										||
			self.cnts[dim] = data.counts#										||
		return self#															||

	def ohe(self, dat, cfg={}, usemap=None, limit=None):#						||
		'''One-hot encoding...with dimensionality limiting defintions
			dat = pandas.series

			need to scan data and generate a list of possible categories
			create default sets for various commmons in encoder.yaml
				such as weekday, month

			need to add a value range one hot encoding options this is a form
			of binning....look integrate the binning function from numerai
			targeting '''
		limit = []
		if usemap != None:
			map = self.config.dikt[usemap]['map']
			cats = list(map.values())
		else:
			if 'limit' not in cfg.keys():
				cfg['limit'] = 1000#findOHELimit(dat)
				#need to find the most common data entries
			map = []
			for d in dat:
				if d not in limit:
					map.append(d)
				if len(limit) == cfg['limit']:
					map.append('other')
					break
		if 'cats' not in cfg.keys():
#			cfg['cats'] = calcd.stuff(dat).unique().subset
			cfg['cats'] = list(df[col].unique())
		ndat = []
		for i in dat:
			cdat = []
			for c in cfg['cats']:
				if i.lower() == c.lower():
					cdat.append(1)
				else:
					cdat.append(0)
			ndat.append(cdat)
		return ndat

	def possibles(self, char_set, combos, fixed=0):#					||
		cnt = 0#														||
		while combos > cnt:
			chars = lexi.panda.content.chunks.char_set(char_set)
			length = len(chars)
			for char in chars:
				word += char
			cnt += 1#modify this to take json document as a rule template that gets filtered against by the rule objects

	def pctmax(self, series, cfg={}):
		'''Calculate each value as a percentage of the maximal value in the dataset
			evaluate using a max value that is some % above the measured max value
			same for min value except the final min must always equal 0 or some value
			slightly larger than 0'''
		ns = []
		for v in series:
			ns.append(float(v)/float(cfg['max']))
		return ns

	def procCombine(self,add):
		lock = 0
		if isinstance(add, str):
			stuff = store.stuff(add).read()
			add, addk = stuff.frame, stuff.kind
		addcols = add.columns
		if common == None:
			common = addcols[0]
		if len(self.ndata.columns) == 0:
			self.ndata = add
			lock = 1
		if lock == 0:
			if len(self.ndata.columns) == len(addcols):
				m = ['Combine Columns',
						list(self.ndata.columns),
						list(addcols)]
				show.show(m).terminal(here).code(o[6])
				if list(self.ndata.columns) == list(addcols):
					pd.merge(self.ndata, add)
					lock = 1
		if lock == 0:
			if common in self.ndata and common in add:
				pd.merge(self.ndata, add, on=common)
				lock = 1
			else:
				m = ['These are the columns',self.ndata.columns]
				show.show(m).terminal(here).code(o[6])
		if lock == 0:
			self.findCommons()
		return self

	def structure(self, how='file'):#									||
		''' '''
		kind = exam.thing(self.data).run()#								||
		if how == 'file':#												||
			pass#														||
			#need to encrypt entire file blobs without opening?
		elif how == 'tabular':#											||
			if calctr.stuff(kind).loosekey('structure') == 'table':#	||
				for line in self.data:#									||
					for col in line:#									||
						self.akrypt(key, col, 'in')#					||

	def selectCols(self, dtype, by):
		ncols = []
		for col in self.data.columns:
			datatype = self.kset[col]['datatype']#						||
			if dtype == datatype:#										||
				ncols.append(col)#										||
		ndata = self.data.loc[:,ncols]#									||
		return ndata#													||

	def serialize(self, out=None, how='list'):
		''
		self.out = []
		for col in self.data.columns:
			for row in self.data[col]:
				if isinstance(row, dict):
					try:
						self.out.append(calctr.stuff(row).dict_2_str().it)
					except Exception as e:
						print('Score Serializtion failed',e)
						print('for these scores',scores)
				elif isinstance(row, ndarray):
					ndo = BytesIO()
					save(ndo, row)
					ndo.seek(0)
					sndo = ndo.read()
					self.out.append(sndo)
				elif isinstance(row, list):
					self.out.append(calcd.stuff(row).list_2_str().it)
				else:
					self.out.append(str(row))
		return self

	def store(self, where, patrn='iterate'):
		self.ruuid = next(what.this().now())
		self._immediate()
		if self.check().equivalance < 99:
			where = namer.engine(where).verify('unique').by(patrn)
		self._immediate(where)
		if validator.engine(where).exists():
			self._immediate('kill')
		return self

	def vectorate(self, how='CrossJoin'):# have to fix multdimentional
		#:::TODO::: integrate dataframe methods
		if how == 'CrossJoin':#combine lists A-1, A-2, B-1, B-2
			i, self.augdata = [[],[]]
			for k in self.data.keys():
				show.show(['Vectorate keys',k]).terminal(here).code(output[0])
				if i != []:
					l = [[x,y] for x in self.data[i] for y in self.data[k]]
					self.augdata.append(l)
				i = k
			self.augdata = self.augdata[0]
			show.show(['new data', self.augdata]).terminal(here).code(output[0])
		if how == 'StraightJoin':#combine lists A-1, B-2
			l, c = [[],0]
			for i in self.d0:
				l.append(i, self.d1[c])
				c += 1
		if how == 'TreeJoin':#A-_1, _2, B-_1, -_2
			pass
		return self


def binarize(data, activate=0):
	'''Convert dataset into a binary dataset based on activation of its value
		attribute '''
	if data == None:
		return None
#	print('Binarize Data', data)
#	df.apply(bin, axis=1)
	if activate == None:
		return float(data)
	elif activate == 0:
		if float(data) != 0:
			out = 1
		else:
			out = 0
	elif isinstance(activate, list):
		if float(data) >= float(activate[0]):
			if float(data) <= float(activate[1]):#||
				out = 1#															||
			else:#																	||
				out = 0#															||
		else:
			out = 0
	return out#																	||


def downcast(df):#																||
	'''Recast datatype for minimization of memory usage in dataframe'''#		||
	cols = df.dtypes.index.tolist()#											||
	types = df.dtypes.values.tolist()#											||
	for i,t in enumerate(types):
		colv = df[cols[i]]
		if 'int' in str(t):
			if colv.min() > iinfo(int8).min and colv.max() < iinfo(int8).max:
				df[cols[i]] = colv.astype(int8)
			elif colv.min() > iinfo(int16).min and colv.max() < iinfo(int16).max:
				df[cols[i]] = colv.astype(int16)
			elif colv.min() > iinfo(int32).min and colv.max() < iinfo(int32).max:
				df[cols[i]] = colv.astype(int32)
			else:
				df[cols[i]] = colv.astype(int64)
		elif 'float' in str(t):
			if colv.min() > finfo(float16).min and colv.max() < finfo(float16).max:
				df[cols[i]] = colv.astype(float16)
			elif colv.min() > finfo(float32).min and colv.max() < finfo(float32).max:
				df[cols[i]] = colv.astype(float32)
			else:
				df[cols[i]] = colv.astype(float64)
		elif t == object:
			if cols[i] == 'date':
				df[cols[i]] = to_datetime(colv, format='%Y-%m-%d')
			else:
				df[cols[i]] = colv.astype('category')
		elif 'str' == t:
			if colv.min() > finfo(float16).min and colv.max() < finfo(float16).max:
				df[cols[i]] = colv.astype(float16)
			elif colv.min() > finfo(float32).min and colv.max() < finfo(float32).max:
				df[cols[i]] = colv.astype(float32)
			else:
				df[cols[i]] = colv.astype(float64)
	return df


def mean_normalize():
	'''Subtract the mean from each value in data set over max, over range,
		over std dev'''


def procTargetEncode(db, targ, tables, activations=[]):
	''' '''
	dbo = sonql.doc(db)
	if not isinstance(tables, list):
		tables = [tables,]
	for table in tables:
		with sonql.doc(db) as dbo:
#			print('Read Table', table, 'Page', page)
			datar = dbo.read({'tables': [table]})

			j = 0
			readcnt = 0
			while True:
				data = next(datar, None)#										||get valid fold
				readcnt += 1
				if data == None:
					print('Break from table', table)
					break

				df = DataFrame(data.dikt[table]['records'],#						||
										columns=data.dikt[table]['columns'])#	||

				targs, targCOLs = [], []
				cnt = 0
				ndf = DataFrame()
				ndf['ID'] = df['id']
				ndf['Target'] = df[targ]

				for activation in activations:
					odf = engine(df).binarize(targ, activation).out#			||
					ndf['targ{0}'.format(cnt)] = odf
					cnt += 1

				with sonql.doc(db) as dbi:
					dbi.write({'{0}targs'.format(table): {
												'records': ndf.values.tolist(),#||
												'columns': ndf.columns}})#		||
	return df


def encode(data, filePath=False):
	"""Python object to file or string."""
	if filePath:
		return json.dump(_serialize(data), filePath)
	else:
		return json.dumps(_serialize(data))


def decode(hook):
	"""File, String, or Dict to python object."""
	try:
		return json.load(hook, object_hook=_restore)
	except (AttributeError, ValueError):
		pass
	try:
		return json.loads(hook, object_hook=_restore)
	except (TypeError, ValueError):
		pass
	return json.loads(json.dumps(hook), object_hook=_restore)


###the below is used for encoding python objects to json strings###
# pylint:		disable=W0612,W0122,R0204
class Dummy(object):
	"""Dummy class to reinitialize."""
	def __init__(self):
		"""Empty init."""
		pass


def mod_load(mod, name):#integrate here with config.modulize
	"""Module loader."""
	try:
		getattr(sys.modules[mod], name)
	except KeyError:
		exec("from " + mod + " import " + name)
	return getattr(sys.modules[mod], name)


def isnamedtuple(obj):
	"""Heuristic check if an object is a namedtuple."""
	return isinstance(obj, tuple) and hasattr(obj, "_fields") and hasattr(obj, "_asdict") and callable(obj._asdict)


def _serialize(data):
	if data is None or isinstance(data, (bool, int, float, str)):
		return data
	if isinstance(data, list):
		return [_serialize(val) for val in data]
	if isinstance(data, OrderedDict):
		return {"py/collections.OrderedDict":
				[[_serialize(k), _serialize(v)] for k, v in data.items()]}
	if isnamedtuple(data):
		return {"py/collections.namedtuple": {
			"type":   type(data).__name__,
			"fields": list(data._fields),
			"values": [_serialize(getattr(data, f)) for f in data._fields]}}
	if isinstance(data, type):
		return {"py/numpy.type": data.__name__}
	if isinstance(data, np.integer):
		return {"py/numpy.int": int(data)}
	if isinstance(data, np.float):
		return {"py/numpy.float": data.hex()}
	if isinstance(data, dict):
		if all(isinstance(k, str) for k in data):
			return {k: _serialize(v) for k, v in data.items()}
		return {"py/dict": [[_serialize(k), _serialize(v)]
							for k, v in data.items()]}
	if isinstance(data, tuple):
		return {"py/tuple": [_serialize(val) for val in data]}
	if isinstance(data, set):
		return {"py/set": [_serialize(val) for val in data]}
	if isinstance(data, np.ndarray):
		return {"py/numpy.ndarray": {
			"values": data.tolist(),
			"dtype":  str(data.dtype)}}
	if isinstance(data, GeneratorType):
		return {'py/generator': str(data)}
	if not isinstance(data, type) and hasattr(data, '__module__'):
		return {'py/class': {'name': data.__class__.__name__,
							 'mod': data.__module__,
							 'attr': _serialize(data.__dict__)}}
	if '_csv.reader' in str(type(data)):
		return ''
	if not isinstance(data, type):
		try:
			hook = str(type(data)).split("'")[1].split('.')
			name, mod = hook.pop(-1), '.'.join(hook)
			return {'py/class': {'name': name,
								 'mod': mod,
								 'attr': {}}}
		except Exception:
			pass
	raise TypeError("Type %s not data-serializable" % type(data))


def _restore(dct):
	# --- custom ---
	if "py/numpy.type" in dct:
		return np.dtype(dct["py/numpy.type"]).type
	elif "py/numpy.int" in dct:
		return np.int32(dct["py/numpy.int"])
	elif "py/numpy.float" in dct:
		return np.float64.fromhex(dct["py/numpy.float"])
	elif "py/dict" in dct:
		return dict(dct["py/dict"])
	elif "py/tuple" in dct:
		return tuple(dct["py/tuple"])
	elif "py/set" in dct:
		return set(dct["py/set"])
	elif "py/collections.namedtuple" in dct:
		data = dct["py/collections.namedtuple"]
		return namedtuple(data["type"], data["fields"])(*data["values"])
	elif "py/numpy.ndarray" in dct:
		data = dct["py/numpy.ndarray"]
		return np.array(data["values"], dtype=data["dtype"])
	elif "py/collections.OrderedDict" in dct:
		return OrderedDict(dct["py/collections.OrderedDict"])
	elif "py/generator" in dct:
		return []
	elif "py/class" in dct:
		obj = dct["py/class"]
		cls_ = mod_load(obj['mod'], obj['name'])
		class_init = Dummy()
		class_init.__class__ = cls_
		for k, v in _restore(obj['attr']).items():
			setattr(class_init, k, v)
		return class_init
	return dct

# class JSONEncodedDict(TypeDecorator):
# 	"""Represents an immutable structure as a json-encoded string."""
# 	impl = TEXT
# 	def process_bind_param(self, value, dialect):
# 		if value is not None:
# 			value = json.dumps(value)
# 		return value
# 	def process_result_value(self, value, dialect):
# 		if value is not None:
# 			value = json.loads(value)
# 		return value
#
# def base_json_conv(obj):
# 	if isinstance(obj, memoryview):
# 		obj = obj.tobytes()
# 	if isinstance(obj, numpy.int64):
# 		return int(obj)
# 	elif isinstance(obj, numpy.bool_):
# 		return bool(obj)
# 	elif isinstance(obj, set):
# 		return list(obj)
# 	elif isinstance(obj, decimal.Decimal):
# 		return float(obj)
# 	elif isinstance(obj, uuid.UUID):
# 		return str(obj)
# 	elif isinstance(obj, timedelta):
# 		return format_timedelta(obj)
# 	elif isinstance(obj, bytes):
# 		try:
# 			return obj.decode("utf-8")
# 		except Exception:
# 			return "[bytes]"
#
#
# def json_iso_dttm_ser(obj, pessimistic: Optional[bool] = False):
# 	"""json serializer that deals with dates
# 	>>> dttm = datetime(1970, 1, 1)
# 	>>> json.dumps({'dttm': dttm}, default=json_iso_dttm_ser)
# 	'{"dttm": "1970-01-01T00:00:00"}'"""
# 	val = base_json_conv(obj)
# 	if val is not None:
# 		return val
# 	if isinstance(obj, (datetime, date, time, pd.Timestamp)):
# 		obj = obj.isoformat()
# 	else:
# 		if pessimistic:
# 			return "Unserializable [{}]".format(type(obj))
# 		else:
# 			raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))
# 	return obj
# def pessimistic_json_iso_dttm_ser(obj):
# 	"""Proxy to call json_iso_dttm_ser in a pessimistic way
# 	If one of object is not serializable to json, it will still succeed"""
# 	return json_iso_dttm_ser(obj, pessimistic=True)
# def json_int_dttm_ser(obj):
# 	"""json serializer that deals with dates"""
# 	val = base_json_conv(obj)
# 	if val is not None:
# 		return val
# 	if isinstance(obj, (datetime, pd.Timestamp)):
# 		obj = datetime_to_epoch(obj)
# 	elif isinstance(obj, date):
# 		obj = (obj - EPOCH.date()).total_seconds() * 1000
# 	else:
# 		raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))
# 	return obj
# def json_dumps_w_dates(payload):
# 	return json.dumps(payload, default=json_int_dttm_ser)
#=============================Source Materials==================================||
'''
https://github.com/cmry/cmry.github.io/blob/master/sources/serialize_sk.py
https://github.com/cmry/cmry.github.io/blob/master/sources/serialize_sk.ipynb
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
