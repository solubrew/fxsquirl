#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name:
	description: >
	expirary: <[expiration]>
  	version: '0.0.0.0.0.0'#														||
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================Core Modules====================================||
import os, datetime as dt, urllib, html5lib, requests#			||
#===============================================================================||
from condor import condor#								||
#===============================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/orgnql.yaml')#								||
class doc:#																||=>Define class
	'Control I/O for Markup Language formats'#							||=>Describe module
	def __init__(self, doct, kind=None, cfg=None):#						||=>Initiate object
		self.doc = doct#												||set doc variable
		if kind == None:#												||
			kind = exam.thing(self.doc).kind#							||
		self.kind = kind#												||
		if self.doc != cfg:#											||chk config load loop
			self.config = config.instruct(pxcfg).select('gronql'#		||
												).override(cfg).dikt#	||load configuration file
		self.parser = 'html5lib'
		self.url = self.doc

	def execute(self, query, paths, args=None):
		''
		self.query(query, args)
		connect = self.post()
		comm.see(['GraphQL',connect])
		self.getdikt = {}
		c = connect
		for path in paths:
			c = c[path]
			print(c)
		self.getdikt[path] = c
		for p in self.getdikt.keys():
			url = self.getdikt[p]
			self.request = requests.get(url, stream=True)
			self.request.raise_for_status()
			self.download('/home/solubrew/DataWorkRepo/NumeraiDR/NumeraiSrcs/')
		return self

	def query(self, query, variables=None, authorization=False):
		'''send a raw request to the Numerai's GraphQL API
			query (str): the query
			variables (dict): dict of variables
			authorization (bool): does the request require authorization'''
		self.body = {'query': query,'variables': variables}
		self.headers = {'Content-type': 'application/json','Accept': 'application/json'}
		if authorization and self.token:
			public_id, secret_key = self.token
			self.headers['Authorization'] = f'Token {public_id}${secret_key}'
		return

	def post(self):
		r = requests.post(self.url, json=self.body, headers=self.headers)
		result = r.json()
		return result

	def download(self, to):
		''
		dtid = thing.when().dtid
		to += dtid
		too = to
		to += '/'+dtid+'.zip'
		with open(to, "wb") as f:
			for chunk in self.request.iter_content(1024):
				f.write(chunk)# unzip dataset
		store.stuff(to).decompress(too)

	def touch(self, path):
		os.makedirs(path)


#==========================Code Source Examples=================================||
'''
#https://github.com/graphql-python/gql

api = 'https://api-tournament.numer.ai'
query = '''query($tournament: Int! $number: Int!) {
            datasetId(number: $number)
            {dataset(tournament: $tournament)}}'''
args={'tournament': 1, 'round': 144}
gronql.doc(api).execute(query, ['data','dataset'],args)
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
