#@@@@@@@@@@@@@@fxsquirl.ObjNQL.TBLONQL@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: 'b814603c-c22e-4e19-a19d-fff51a69716e'
	name: TBLONQL
	description: >
		Table based data I/O
	expirary: <[expiration]>  #											||
	version: <[version]>  #												||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
import csv, pandas as pd
from pandas import read_csv, DataFrame, read_excel
from io import StringIO
#===============================================================================||
from condor import condor#							||
from fxsquirl.orgnql import sonql#					||
from excalc import exam, text as calct#					||
#===============================================================================||
here = join(dirname(__file__),'')#					||
there = abspath(join('../../..'))#					||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/objnql.yaml')#								||assign default config

class doc:#																		||
	'''I/O Comma Seperated Values'''#											||
	version = '0.0.0.0.0.0'#													||
	def __init__(self, doc, kind=None, cfg=None):#								||
		self.doc = doc#															||
		self.config = condor.instruct(pxcfg).select('tblonql').override(cfg
																		).dikt#	||load config
		#if kind == None:
		#	kind = exam.thing(self.doc).kind
		#self.kind = kind

	def read(self, cfg={}, fill=None):#								||
		'''/O Comma Seperated Values into tables and frames'''
		table = calct.stuff(self.doc).filename().it
		if 'page' not in cfg.keys():
			cfg['page'] = 100000# refactor to pull from config
		codingls = ['UTF-8','UTF-16','ASCII','ANSI','Windows-1252']
		for df in read_csv(self.doc, chunksize=cfg['page'], iterator=True,
															low_memory=False):#	||
			self.table = list(df)#										||
			self.text = str(df)#										||
			self.lines = str(self.text).split('\n')
			table = calct.stuff(self.doc).filename(False).it
			self.dikt = {table: {'columns': df.columns, 'records': df}}#		||
			self.dfs = {table: df}
			yield self
		yield None

	def append(self, data, ext='.csv', cfg=None):
		''' '''
		if cfg == None:
			cfg = {'mode': 'a'}
		self.write(data, ext, cfg)
		return self

	def write(self, data, ext='.csv', cfg=None):#								||
		'''Write tables and frames into comma seperated value files'''#			||
		if cfg == None:#														||
			cfg = {'mode': 'w'}#												||
		if not isinstance(data, DataFrame):#									||
			data = DataFrame(data)#												||
		data.to_csv(self.doc, index=False, mode=cfg['mode'], header=False,#		||
															encoding='utf-8')#	||
		return self

	def table(self, headstrip):
		''' '''
		df = read_excel('{0}/{1}'.format(path, f1l3), sheet='Sheet1')
		self.cols, self.rows, cnt = df.columns, [], 0
		while cnt < len(df[cols[0]]):#gives the lenght of first data column
			row = []
			for col in cols:
				row.append(df[col][cnt])
			self.rows.append(row)
			cnt += 1
		if self.ftype == 'XL':
			self.table = read_excel(f1l3, sheet)
			self.columns = self.xl.head(1)
			self.data = []
			for row in xl.iterrows():
				self.data.append(row)
		elif iscsv:
			self.columns = CSV.head
			with open(f1l3.csv,newline='') as DOC:
				header = csv.Sniffer().has_header(DOC.read())
				array = csv.reader(DOC)
		return self


#===============================Source Materials================================||
'''
http://pythondata.com/working-large-csv-files-python/
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
