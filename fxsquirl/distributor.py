#@@@@@@@@Pheonix.Molecules.Distributor.Distributor@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 9942b938-44ae-4190-a833-25af5af8c0ef
	name: Molecule Level Distributor Module
	description: >
		Distrubte information given a distribution mapp and/or
		a set of templates. This distribution can be to a
		database, a file, a filesystem...how to integrate and handle 3rd

		general copying datasets can be file systems to be modified and rebuilt
		either as structure or structure and data

		how to use templating on a dataset directly?
		expanding a dictionary with a looping key?
		possible?

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/molecules/distributor/distributor.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, dirname, join
import os, datetime as dt#												||
#=======================================================================||
from condor import condor#								||
from excalc import exam#									||
from fxsquirl import store
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
pxcfg = join(abspath(here), '_data_/dsitributor.yaml')#								||use default configuration
class engine(object):#															||
	'distribute data & files according to templated configurations'#	||
	version = '0.0.0.0.0.0'#											||
	def __init__(self, src, options=None, cfg=None):#					||=>Initialize class instance
		'Initialize Distribution Engine'
		pxcfg = condor.instruct(pxcfg).load().override(cfg)#			||load configuration file
		self.config = pxcfg.dikt#										||
		self.session = pxcfg.ppov#										||
		self.source = src#												||
		self.kind = exam.thing(src).kind
		self.onqlSRC = list(self.kind.keys())[0]
		self.kindSRC = self.kind[self.onqlSRC]#							||
		self.dataOBJ = store.stuff(self.source).read()#					||set data
		self.distLOCI = self.mapp()
	def buildout(self, mapp=None, tmplts=None):#						||
		'load templates -> populate templates -> write file/data tree'
		#write out a csv file for data given template
		while True:
			data = next(rdr)
		if mapp == None:
			mapp = self.mapp
		if tmplts == None:#												||
			self.tmplts += tmplts#										||
		return self#													||
	def creStructure(self, verse):#										||
		#need to figure out where to implement the <(meta)> type rules
		#use template to create a new file system based on implicit
		#and explicit structures of template outline
		self.loadStructure(tmplts, data)#								||
		store.fsonql.doc(verse).write(branches)#						||
		return self#													||
	def chkStructure(self):
		strctr = self.distribute['structure']
		self.getCurrent()
		cmpr = validator.engine(self.curnt).against(strctr)
		log.out(cmpr)
		cmpr.update()
		return self
	def cfgSyncDevice(self):
		''
		return self
	def cfgSyncPath(self):
		''
		return self
	def distVersion(self, cfg=None):
		'Distribute new version of data & file given specific version'
		if cfg == None:
			nwvrsn = self.vrsns.getNext()
		self.vrsns = vrsnr.engine(self.src).versions(vers)
		return self
	def divide(self):
		'build method to seperate a file system given filtering and matching criteria'
		return
	def expand(self, tmplts=None):#should probaly develop into a generator
		'Expand templates given various data structures'
		if tmplts == None:
			tmplts = self.config['tmplts']['views']#				||
		tmplts = condor.instruct(tmplts).load()
		for view, tmplt in tmplts.items():
			options, noptions = tmplt['opts'], {}
			cmd = tmplt['cmd']
			for term in options.keys():
				if 'OR' == term:
					for term, opts in options[term].items():
						factorial = calcd.stuff(opts).factorial().it
						noptions[term] = factorial
				else:
					noptions[term] = options[term]
			fills = calctr.stuff(noptions).multiplex().it
			inc = 0
			wrdata = {}
			for fill in fills:
				name = view+str(inc)
				creview = rule.mechanism(cmd, fill).run()
				wrdata[name] = creview
				inc += 1
			self.dbo0.write({'views': wrdata})
	def getArchives(self, cfg=None):
		'read archived filesystem'
		if self.src == None:
			self.getDistributionConfig(cfg)
		sanes = ['zz-hist_',]
		self.archv = self.slctr.stratified('Filtered', sanes)['b']
		return self
	def getVersions(self, vers=[0,]):
		if self.src == None:
			self.getDistributionConfig(cfg)
		self.vrsns = vrsnr.engine(self.src).versions(vers)
		return self
	def loadStructure(self, tmplts, data=None):
		tmplts = []
		data = {}
		rules = ['VARS.FILTER.all']
		tree = rule.mechanism(tmplts, data, rules).complete()
		store.stuff()
		branches = calctr.stuff().makePaths(tmplt['structure'], verse)
		return self
	def mapp(self):
		'Create a mapping strucutre for distribution of given inputs'
		if 'store' in self.kind.keys():
			if self.kind['store'] == 'sqlite':
				pass
	def processDB(self):
		''
		dbo = sonql.doc(self.source)
		tables = self.config['tables']
		if not isinstance(tables, list):
			tables = [tables,]
		for table in tables:
			cfg = {'tables': [table], 'page': 100000}
			datar = dbo.read(cfg)
			j = 0
			while True:
				data = next(datar, None)#										||get valid fold
				if data == None:
					break
				yield DataFrame(data.dikt[table]['records'], columns=data.dikt[table]['columns'])
def distCSV(db, f, cfg):
	'Output a CSV file given a database request'
	if 'tables' in cfg.keys():
		t = cfg['tables'][0]
	else:
		t = cfg['views'][0]
	viewRDR = sonql.doc(db).read(cfg)
	while True:
		data = next(viewRDR, None)
		if data == None:
			break
		wrdata = data.dikt[t]['columns'] + data.dikt[t]['records']
		tblonql.doc(f).write(wrdata)
def distFS():
	''
#==========================Source Materials=============================||
#============================:::DNA:::==================================||
'''
---
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
