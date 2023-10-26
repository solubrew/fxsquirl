#@@@@@@@@@@@@@@@@@@@@@@@@Pheonix.Organisms.Djynn.Djynn@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(meta)>:
	docid: <^[uuid]^>
	name: Organism Level Djynn Module
	description: >
		Generate documents of content by combining available data
		and templates.  The document could be an insert command to upload data
		to a database or various forms of a document from mtpmlt, tmplt, doc.
		utilize machine learning tools, random generators and
		user input to interpolate and extrapolate content

		leverage panda/mtplts
		subtrix
		eventually logicizier once nlp functions are integrated there
		as well as the afxsquirlmist/maybe instead of logicizer
		leverage visualizer/akashic to view and investigate base statistics
		by database view/pandas frame

		generate hypertuning parameters for logicizer base algorythms
		converting parameter options from the algo list

		Template interaction engine build documents from templates and
		meta-templates.
		Events are ephemeral, require resources, happen over a period #			||
		of time, may involve actors #											||

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>/pheonix/organisms/djynn/z-data_/djynn.yaml
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor#										||
from subtrix.thing import When
from fxsquirl import processor
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = join(abspath(here), '_data_/generator.yaml')#								||use default configuration
class engine(processor.engine):
	'''Create Data through Download, Expansion, and Generation'''#				||
	version = '0.0.0.0.0.0'#													||
	def __init__(self, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#				||load configuration file
		processor.engine.__init__(self, self.config)
	def buildTMPLTs(self):
		if tmplts != None or not isinstance(tmplts, list):
			tmplts = [tmplts]
		self.tmplts = tmplts
		if output == None:
			output = self.config.ppov['stores']['WORKvrs']
		self.stor = store.stuff(output)
		self.session = pxcfg.ppov#												||
		path = '{0}bear/LEXI/TMPLTs'
		self.tmplts = fsonql.doc(path)
		path = '{0}bear/LEXI/MTMPLTs'
		self.mtmplts = fsonql.doc(path)
		return self
	def buildTMPLT(self):
		'Build tmplt into outputtable object'
		return
	def buildMTMPLT(self):
		'Build mtmplt into outputtable object'
		return
	def searchTMPLTs(self):
		'Search tmplts directory for requested tmplt document or feature'
		fTMPLTs = next(self.tmplts.filtr(tmplt).read())
		return
	def searchMTMPLTs(self, mtmplt):
		'Search mtmplts directory for requests mtmplt document or feature'
		fmtmplts = []
		while True:
			results = next(self.mtmplts.filtr(mtmplt).read(), None)
			if results == None:
				break
			fmtmplts.append(results)
		return
	def genDocs(self, doctype):
		'''Generate a set of documents by expanding given data in various ways
		then save based on the document implementation type being, table, view,
		file, file system, audio, video'''
		for doc, tmplt in self.tmplts.items():#								||
			options, noptions = self.data, {}#								||
			inc = 0#											||
			#integrate factorial and multiplex at the subtrix level?
			#
			if 'OR' in options.keys():#											||
				for term, opts in options['OR'].items():#						||
					factorial = calcd.stuff(opts).factorial()#					||
					while True:#												||
						fact = next(factorial, None)#						||
						if fact == None:
							break
						noptions[term] = fact.it
						inc = self.bldDocs(doctype, name, cmd, options, noptions, inc)#	||
			else:#																||
				print('Run View Creation')
				inc = bldDocs(doctype, name, cmd, options, noptions, inc)#	||
	def add(self, fxmap):#											||
		'''A df contains the grouping for the data changes and the fxmap
			tells how to change each field Perform function on data within each
			division node such as averaging of values within the box need to
			push this all over to collector'''
		for table in fxmap.keys():
			if table not in self.sinkdfs.keys():
				continue
			for col in fxmap.keys():
				if col not in self.sinkdfs[table].columns:
					continue
				fx = fxmap[table][col]['store']
				name = fxmap[table][col]['name']
				self.sinkdfs[table][name]=self.applyFX(self.dfs[table][col],fx)
		return self
	def procDB2File(self, db, f, cfg, kcols):
		''' '''
		t = cfg['tables'][0].lower()
		cfg['page'] = 10000000
		viewRDR = sonql.doc(db).read(cfg)
		twrite = tblonql.doc(f)
		cnt = 0
		while True:
			data = next(viewRDR, None)
			if data == None:
				break
			df = DataFrame(data.dikt[t]['records'],
										columns=data.dikt[t]['columns'])#	||
			predicts = DataFrame()
			for kcol, col in kcols.items():
				predicts[kcol] = df[col]
			ndata = calcd.df2lists(predicts)
			if cnt == 0:
				ndata = [kcols] + ndata
				cnt += 1
			twrite.write(ndata)
	def fuzzing(self):
		'''build a fuzzing tool for the generator'''
		return self
	def transform(self):
		'''Generate new dataset from given dataset using known transformation
			methods '''

def copyTMPLT(tpath: str, npath: str, name: str, cfg: dict={}):
	'''Copy TMPLT from given location filling out any defined substituions and
		renaming the TMPLT for the new location'''
	tmplt = txtonql.doc(tpath).read().text
	cfg['name'] = name
	txtonql.doc(npath).write(subtrix.mechanism(tmplt, cfg).run()[0])
	return
def csvFromDB():
	'''replace with a usage of the generator engine.procDBFile'''
	t = cfg['tables'][0].lower()
	cfg['page'] = 10000000
	viewRDR = sonql.doc(db).read(cfg)
	cnt = 0
	pxcfg = condor.instruct('{0}fx.yaml'.format(here)).load().dikt#				||
	while True:
		data = next(viewRDR, None)
		predicts = DataFrame()
		if data == None:
			print('Break on count',cnt)
			break
		#need to add the columns to the records
		print(data.dikt.keys())
		df = DataFrame(data.dikt[t]['records'], columns=data.dikt[t]['columns'])
		for model in smodels.keys():
			f = f'{setPath}{When}/Submission_{smodels[model]}.csv'
			twrite = tblonql.doc(f)
			predicts['id'] = df['targetid']
			predicts['prediction_kazutsugi'] = df[smodels[model]]
			ndata = calcd.df2lists(predicts)
			if cnt == 0:
				ndata = [['id', 'prediction_kazutsugi']] + ndata
			twrite.write(ndata)
		cnt += 1




#==========================Source Materials=============================||
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
