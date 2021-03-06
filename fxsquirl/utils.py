#@@@@@@@@@@@@@@Pheonix.Organelle.Collector.Collector@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name: Pheonix Builder Module Python Document
	description: >
		Primarily an engine class for building data artifacts
	expirary: '<^[expiration]^>'
	version: '<^[version]^>'
	authority: 'document|this'
	security: 'seclvl2'
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
here = join(dirname(__file__),'')#						||
log = False
#===============================================================================||

def csv2db(dbo, path):
	datar = tblonql.doc(path).read()
	while True:
		dwrite = next(datar, None)
		if dwrite == None:
			break
		dbo.write(dwrite.dikt)

def yieldBreak(data, table):
	if data == {}:
		if log: print('Data is empty DataFrame')
		return True
	else:
		if table == None:
			table = list(data.keys())[0]
		if table in data.keys():
			if 'records' in data[table].keys():
				if data[table]['records'] == []:
					if log: print(f'dict with empty "records" key for {table}')
					return True
			elif 'dataframe' in data[table].keys():
				if data[table]['dataframe'].empty:
					if log: print(f'dict with empty "dataframe" key for {table}')
					return True
			elif isinstance(data[table], DataFrame):
				if data[table].empty:
					if log: print(f'dict with empty DataFrame for {table}')
					return True
	return False


#===============================Source Materials================================||

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
