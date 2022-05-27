#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid:
	name: Element Level Store Module OrgNQL Extension Python Document#	||
	description: >
		Organized Notation Query Language
		Route request to the correct database type
		generate statement for given database type
		Get data stored in file systems
		Document Query Language get information
		Store data via a File System Structure

		:::TODO:::....creates duplicate zz-hist_ depths

		Write a ctd file/suplement walk over a directory and create a
		node for each file of a given type/s This Script will turn a
		given file system starting point and specified depth into a tree
		based note file.  It will document information about the files
		found and attempt to write all possible files into the content
		area based on a file extension whitelist and extension specific
		function This is grafting a file system to a cherrytree document
		options to delete filesystem/convertedfilesonly/create a monitoring
		structure to keep the two in sync???? convert a directory with a
		whitelist of file extensions to a ctd file/add


	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/store/store.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import shutil, datetime as dt, pandas as pd#						||
from ftplib import FTP#													||
from os import listdir
from os.path import abspath, dirname, join, isdir
import hashlib, time, shutil, sys, pprint
#=======================================================================||
from pandas import DataFrame
#===============================================================================||
from condor import condor, thing#								||

from fxsquirl import fxsquirl
from fxsquirl.objnql import objnql, imgonql, tblonql, txtonql#								||
from fxsquirl.orgnql import orgnql, fonql, sonql, yonql#						||

from excalc import calcgen, exam, phile as examp, text as calct, tree as calctr
from excalc import data as calcd
#=======================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
page = 1000000
#=======================================================================||
class doc:#																		||=>Define class
	'I/O organized data incl. dicts & trees to files & dbs'#					||=>Describe class
	version = '0.0.0.0.0.0'#													||=>Set version
	def __init__(self, doc, kind=None, cfg=None):#								||
		self.doct = doc#														||set doc var
		if kind == None:#														||
			kind = exam.thing(self.doct).kind#									||
		self.kind = kind#														||
		pxcfg = join(abspath(here), '_data_/orgnql.yaml')#						||use default configuration
		if self.doct!= cfg:#													||chk doc = config
			self.config = condor.instruct(pxcfg).load().override(cfg).dikt#		||load configuration file
		self._qlrtr()#															||run query language router
		self.text, self.lines, self.table = '', '', []#							||
		self.dikt, self.frame, self.tree = {}, pd.DataFrame(), {}#				||
	def _qlrtr(self):#															||=>Define module
		'Route read request to the properly formatted organization'#			||=>Describe module
#		comm.see(['Orgnql.kind',self.kind])
		for ql in self.config.keys():#									||loop thru org types
			if ql == self.kind['orgnql']['f(x)']:#						||chk org type query lang
				if ql == None:#											||
					return self#										||
				ql = 'fxsquirl.orgnql.orgnql.'+ql#		||
				self.dh = condor.instruct(ql).modulize().obj#			||set handler and objectify
				break#													||
			else:#														||
				self.dh = None#											||
		if self.dh != None:#											||
			self.org = self.dh.doc(self.doct, self.kind)#				||
		else:#															||
			self.org = None
			print('No Organized Query Language Matched')#				||
		return self#													||=>
	def conx(self):#=>Define module#									||
		self.server = self.config[dbtype]['server']#					||
		self.port = self.config[dbtype]['port']#						||
		return self#													||
	def copy(self, to, tipe=None):#										||
		'Copy an organizational document to a different format'#		||
		if tipe == None:#												||
			tipe = list(self.kind.keys())[0]#							||
		else:#															||
			to_options = self.config.keys()#							||
			if tipe in to_options:#										||
				to_tipe = self.config[tipe]#							||
		return self#													||
	def curl(self):#													||
		path = '/to/path'#												||
		site = 'sitename.com'#											||
		ftp = 'ftp://'+site+path#										||
		cmd = 'curl --ftp-create-dirs -T '+upload#						||
		cmd += ' -u '+uname+':'+pword+' '+ftp#							||
		return self#													||
	def git(self, too=None):#											||
		if too == None:#												||
			too = self.config['']#										||
		Repo.clone_from(self.frum, too)#								||
		return self#													||
	def graft(self, branch, ntrunk):#									||=>Define module
		nbranch = branch.replace(self.path, ntrunk)#					||
		if not os.path.exists(nbranch):#								||
			try:#														||
				os.makedirs(nbranch)#									||
			except:#													||
				m = ['This is the New Banch ',#							||
						nbranch, '\nCre Dir failed']#					||
				comm.see(m)#						||
	def nextrecord(self, frum=None):#									||
		'Get Iterated Sequence from Names Database for Name Code'#		||
		sonql.doc(self.frum).write(#									||
								{frum:{'records':[[]],'columns':[]}})#	||
		data = {'table': frum}#											||
		inc = next(sonql.doc(self.frum).read(data,{'page':1},'next'))#	||
		inc = inc.dikt['given']['records'][0][0]#						||
		return inc#														||
	def read(self, fill=None, cfg=None, cmd=None):#								||=>Define method
		'/O organized data from file systems, flat files and dbases'#	||=>Describe method
		if cfg == None:#												||
			cfg = {'page': 100}#										||other option is chunk
		size = 0#														||
		if self.org == None:
			self.go = False
			self.dikt = {}
			self.philes = None
		else:
			org = next(self.org.read(fill, cfg, cmd))#						||
			try:
				self.go = org.go
			except:
				comm.see(['Go not found for dh handler',self.dh])
				self.go = False
			self.dikt = org.dikt
			try:
				self.philes = org.philes
			except:
				self.philes = None
		yield self
	def read_a000(self, fill=None, cfg=None, cmd=None):#								||=>Define method
		'/O organized data from file systems, flat files and dbases'#	||=>Describe method
		if cfg == None:#												||
			cfg = {'page': 100}#										||other option is chunk
		for o in org:#													||
			size += 1#													||
			self.dikt = o.dikt#											||
			if self.dikt != None:#										||
				self.text = str(o.dikt)#								||
				self.lines = calct.stuff(self.text).makeList()#			||
				if self.frame.empty:#									||
					self.frame = pd.DataFrame(self.table)#				||
				self.tree = self.dikt#									||
			if size == cfg['page']:#									||
				self.go = True
				yield self#												||
				size = 0#												||
		self.go = False
		yield self#														||
	def sane(self):
		if self.how == 'inc':#											||
			keep, drop = self._include(self.sanes)
		else:#															||
			keep = self._exclude(self.sanes).keep#						||
		self.org.dikt = keep
	def touch(self, phile):#											||
		here = phile[:phile.rfind('/')]#								||
		if not os.path.exists(here):#									||
			os.makedirs(here)#											||
		return self
	def write(self, data):#												||=>Define method
		'I/ organized data to filesystems, flat files and dbases'#		||=>Describe method
		self.touch(self.doct)
		self.dh.doc(self.doct).write(data)#								||
		return self#													||
def convertImages(path, subfolder=True):
	fs = next(fonql.doc(path).read())
	tree = fs.dikt
	print('Tree',tree)
	images = tree.filtr(['.jpeg','.jpg','.bmp'])
	print('Images',images)
def foldDataSets(db, table, tag=None):
	''
	if tag == None:
		tag = 'CYCL{0}'.format(thing.what().uuid().ruuid[-5:])#					||
	else:
		return tag
	with sonql.doc(db) as dbo:
		datar = dbo.read({'tables': [table], 'page': page})
		cnt = 0
		while True:
			cnt += 1
			datao = next(datar, None)
			if datao == None:
				break
			trainc = datao.dikt[table]['columns']
			df = DataFrame(datao.dikt[table]['records'], columns=trainc)#	||
			datao.dikt[table]['records'] = []
			fd = selector.engine(df).fold('RandomSelection')
			del df
			splitPT = 315
			trainset = fd.dset0.iloc[:, 0:splitPT]
			trainvalidset = fd.dset1.iloc[:, 0:splitPT]
			with sonql.doc(db) as dbi:
				dbi.write({tag+'Train': {'columns': trainc[:splitPT], 'records': trainset}})#	||
				dbi.write({tag+'Trainvalid':{'columns': trainc[:splitPT], 'records': trainvalidset}})#	||
			del trainset
			del trainvalidset
			gc.collect()
	return tag#															||
def db2text():
	db = '/home/solubrew/OPs/_info/OPs.sqlite'
	path = '/home/solubrew/OPs/OPs.yaml'
	rdr = sonql.doc(db).read()
	data = None
	while True:
		datad = next(rdr, None)
		if datad == None or datad.dikt == data:
			break
		data = datad.dikt
		print(data)
		columns = data['OP']['columns']
		ls = ['OPId', 'CreBy', 'CreOn','ModBy','ModOn','DLT','ACTV']
		dikt = {}
		for record in data['OP']['records']:
			#need to load string to yaml formatting before writing to file
			pos = columns.index('hrid')
			dikt[record[pos]] = {}
			for i in range(len(record)):
				if columns[i] in ls:
					continue
				dikt[record[pos]][columns[i]] = next(yonql.doc(record[i], {'orgnql': {'code': 'YAML'}}).read()).dikt
	yonql.doc(path).write(dikt)
def storeTblFile2DB(db, fdir, wdir, fname, cmprsEXT='.zip', tableEXT='.csv'):#	||
	'Need to convert this into a util for csv to sqlite transfer'#		||
	path = '{0}{1}/'.format(wdir, fname)
	fonql.uncompress('{0}{1}{2}'.format(fdir, fname, cmprsEXT), path)#			||
	tag = thing.what().uuid().hexid[-5:]#										||
	#need to expand to allow for large directory usage


	filtrfs = next(fonql.doc(path).read()).filtr([tableEXT]).nphiles#		||
	print('Filtered Files',filtrfs)
	npath = '{0}{1}{2}.sqlite'.format(path, fname, tag)

	dbo = sonql.doc(npath)
	for phile in filtrfs:#														||
		datar = tblonql.doc('{0}/{1}'.format(path, phile)).read()#				||
		while True:#															||
			dwrite = next(datar, None)#											||
			if dwrite == None:
				print('End of File',phile)
				break
			dbo.write(dwrite.dikt)#										||
	return tag
def csv2db(dbo, path):
	datar = tblonql.doc(path).read()
	while True:
#		print('keep running')
		dwrite = next(datar, None)
		if dwrite == None:
#			print('stop running')
			break
#		print('Dwrite',dwrite)
		dbo.write(dwrite.dikt)
def dir_csv2db(path, dbPATH, fileEXT='.csv'):
	'Search directory for given file ext and transfer data to a database'
	filer = fonql.doc(path).read()
	while True:
		files = next(filer, None)
		if files == None:
			break
		dbo = sonql.doc(dbPATH)
		nphiles = files.filtr([fileEXT]).nphiles
		print('NPhiles', nphiles)
		for file in nphiles:
			print('File', file)
			fpath = '{0}{1}'.format(path, file)
			csv2db(dbo, fpath)
def getColors(path):
	''
	fs = fonql.doc(path).read()
	while True:
		philes = next(fs, None)
		if philes == None:
			break
		images = philes.filtr(['.png'])
		for image in images:
			imgOBJ = imgonql.doc(image).read()
			colors = imgOBJ.getColors()
			print('Colors',colors.hues)
			plot = imgOBJ.plot()
			thumbIMG = imgOBJ.thumb
			plotIMG = makeimage(plot)
			paletteIMG = makePalette(colors)
			#store images to a cherrytree
def compressBatchDirectories(path):
	''
	for i in listdir(path):
		if isdir('{0}/{1}'.format(path, i)):
			fonql.compress('{0}/{1}'.format(path,i))

def chunk():
	chunksize = 100000
	i = 0
	j = 1
	for df in pd.read_csv(file, chunksize=chunksize, iterator=True):
		df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
		df.index += j
		i+=1
		df.to_sql('table', csv_database, if_exists='append')
		j = df.index[-1] + 1
def CopyPath(path):
	start, end = '~','.'
	reader = fonql.doc(path).read
	args = [None, {'page': 20}]
	go, cnt = True, 0
	trimmer = calct.stuff(None)
	while go == True:
		s0 = next(reader(*args))
		m = ['Files Read',cnt,]
		log.WORKLOG('fileRenamer',m,s0.philes)
		nfiles, zips = [], []
		for phile in s0.philes:
			if start in phile:
				trimmer.renew(phile)
				pphile = [phile,]
				nfile = trimmer.trimBetween(start, end).it
				pphile.append(nfile)
				nfiles.append(pphile)
		m = ['List of Renamed Files',cnt]
		log.WORKLOG('fileRenamer',m,nfiles)
		for phile in nfiles:
			done = fonql.fileCopy(phile[0], phile[1],'Replace')
		go = s0.go
		cnt += 1
		print(cnt)
def MovePath(path):
	searchers = []
	reader = fonql.doc(path).read
	args = [None, {'page': 20}]
	go, cnt = True, 0
	trimmer = calct.stuff(None)
	while go == True:
		s0 = next(reader(*args))
		m = ['Files Read',cnt,]
		log.WORKLOG('fileRenamer',m,s0.philes)
		nfiles = []
		for phile in s0.philes:
			for searcher in searchers:
				if searcher in phile:
					nfiles.append(phile)
		m = ['List of to Move Files',cnt]
		log.WORKLOG('fileRenamer',m,nfiles)
		for phile in nfiles:
			done = fonql.fileMove(phile,':::KILL:::')
		go = s0.go
		cnt += 1
		print(cnt)
def makeFS2Cherrytree(name, path, opath, cfg=None):
	NB = nb.doc(name)
	tree = next(fonql.doc(path).read()).dikt
	for key, val in tree.items():
		if key == ':::PHILES:::':
			for phile in val:
				tree.createCell(phile)
		else:
			tree.createNode(key)
class rebuildDB(object):
	def __init__(self, db0, db1=None):
		''' '''
		pxcfg = join(abspath(here), '_data_/utilDBRebuilder.yaml')#				||use default configuration
		self.config = condor.instruct(pxcfg).load().dikt
		self.dbo0 = sonql.doc(db0)
		if db1 == None:
			db1 = calct.stuff(db0).rename().it
		self.dbo1 = sonql.doc(db1)
		self.getTables()
		self.getViews()
	def getTables(self):
		''
		self.tables = self.dbo0.getInfo().dbtables
		return self
	def getViews(self):
		self.views = self.dbo0.getInfo('views').dbtables
		return self
	def dropViews(self, view=None):
		if view != None:
			self.dbo0.drop(view)
		for view in self.views:
			self.dbo0.drop(view, 'views')
		print('Views Dropped')
	def genViews(self, tmpltVIEWs=None):#								||
		if tmpltVIEWs == None:#											||
			tmpltVIEWs = self.config['tmplts']['views']#				||
		else:#															||
			tv = condor.instruct(tmpltVIEWs).load()#					||
			tmpltVIEWs = tv.dikt['tmplts']['views']#					||
		for view, tmplt in tmpltVIEWs.items():#							||
			options, noptions = tmplt['opts'], {}#						||
			cmd, inc = tmplt['cmd'], 0#									||
			if 'OR' in options.keys():#									||
				for term, opts in options['OR'].items():#				||
					factorial = calcd.stuff(opts).factorial()#			||
					while True:#										||
						try:#											||
							noptions[term] = next(factorial).it#		||
						except:#										||
							break#										||
						inc = self.creViews(view, cmd, options,
														noptions, inc)#	||
			else:#														||
				self.creViews(view, cmd, options, noptions, inc)#		||
	def creViews(self, view, cmd, options, noptions, inc=0):#			||
		''
		for term in options.keys():
			if term != 'OR':
				noptions[term] = options[term]
		fills = calctr.stuff(noptions).multiplex().it
		for fill in fills:
			wrdata = {}
			name = view+str(inc)
			creview = rule.mechanism(cmd, fill).run()[0]
			if ',   ORDER' in creview:
				creview = [creview.replace(',   ORDER', ' ORDER'),]
			wrdata[name] = creview
			inc += 1
			self.dbo0.write({'views': wrdata})
		return inc
	def genTables(self):#												||
		''
		for table in self.tables:#										||
			sqlcfg = {'tables': [table]}#								||
			while True:#												||
				data = next(self.dbo0.read(sqlcfg))#					||
				records = data.dikt[table]['records']#					||
				columns = data.dikt[table]['columns']#					||
				if data.go == False:#									||
					break#												||
				records = self.renameColumns(records, columns)#			||
				records - self.cleanData(records)#						||
				records = self.addTableColumns(records)#				||
				d = {table: {'records': records, 'columns': columns}}#	||
				self.dbo1.write(d)#										||
	def addTableColumns(self, r):#										||
		''
		r['PercDefects'] = r['totalDefects']/sum(r['totalDefects'])#	||
		r['PerceQPs'] = r['numeQPs']/sum(r['numeQPs'])#					||
		return r#														||
	def cleanData(self, r):#											||
		#r.isna().sum()get stats on missing values...need to use to work through
		r.fillna(0)# for now we are just filling in zero values
		return r
	def renameColumns(self, r, c):#										||
		colrename = {}#													||
		for l in range(len(c)):#										||
			colrename[l] = c[l]#										||
		return r.rename(columns=colrename)#								||
def wb2SQLite(dbp, path):#												||
	''
	wb = sheet.loadWorkBook(path)
	for shname in wb.sheetnames:
		print('Get Sheet',shname)
		ws2SQLite(shname, dbp, None, wb)
def ws2SQLite(shname, dbp, path=None, wb=None):#						||
	''
	if path != None:
		wb = sheet.loadWorkBook(path)#									||
	print('Worksheet ', shname)
	records = []
	r = wb[shname].values
	rcnt = 1
	while True:
		try:
			if rcnt == 1:#												||
				columns = [x.strip(' ') for x in list(next(r)) if x != None]#				||
			else:
				row = list(next(r)[:len(columns)])
				if row[0] == None:
					break
				records.append(row)#									||
			rcnt += 1
		except Exception as e:
			print(e)
			break
	e = 'State'
	try:
		log.WORKLOG(e,columns,records)
	except:
		print('Log Failed')
	try:
		db = sonql.doc(dbp)
	except Exception as e:
		print('DB Connection Failed due to',e)
	try:
		data = {shname: {'columns': columns, 'records': records}}#		||
		db.write(data)
	except Exception as e:
		m = 'DB Write Failed'
		comm.see([m,e])
		log.ERRORLOG(e,m,data)
#==================Code Source Examples=================================||
#===========================:::DNA:::===================================||
'''
---
201804101206:
	administer:
		version: <[active:.version]>
		test:
		description: >
			Administrate Tests of the CalgGen Classes
		work:
201804101206:
	here:
		version: <[active:.version]>
		test:
		description: >
			Test Each CalcGen Class
		work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
