#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
''' #																			||
--- #																			||
<(META)>: #																		||
	docid: <^[uuid]^> #															||
	name:  Organisms Level FxSQuIRL Module Python Document#						||
	description: > #															||
		Fractionally Executed SQL Queued Interactive Recursion Layer

		integrate deeply with worldbridger api system to use both the local
		set of databases along with data to be sourced from a distributed
		set of data providers including a torrent style data transfer method
		mediated by onchain metadata

		intended to provide a defined multi-sink, multi-source, multi-format
		data object

		high level abstraction layer overtop of all the pheonix molecules and
		elements I/O and data manipulation

		Routing Data Manipulations between inmem databases, stored databases,
		remote databases, etc		#osbrain named server?

		only one shared cache inmem db others must be private spin a process for
		each in memdb for each fileinmemdb needed use the single shared cache
		for the main app db have the name server communicate directly here

		inmemdb
		bigtable
		cmd = "CREATE TABLE bgtbl col0-col49"#use machine learning here

		appdb...one per device running application multiple interaction pathways
		filedbs...unknown number
		how to determine when a fileDB should get its own bigtable

		increased security
		how to implement permissions effectively?? no permissions needed really
		until multiuser...however a user and admin role could be leveraged
		from the beginning and provide a framework for the multiuser expansion
		reduced overhead for lots of small workbooks using a combined bigtable
		how to combine efficiently?  columns mapped via some configuration
		file...sqlite having no hard type columns is more viable here
		in other databases we need to determine the column type and choose
		accordingly
		process:
			load document
			get all sectn ids from file db and load into inmem big table
			map document table columns to bigtable columns
			read document
			check bigtable documents
			if no runs are connected to the current document...how to tell
			check m_run table
			check _run table
			once completed
			if not there:
				load document limit 0 to displaysize-y*(1+i%)
			if is there get first and lest seq
				compare against displaysize-y
					if not then grab additional
						check if first is 0 then get from bottom
					if not split gap and get from top first
						then from bottom
			also verify that full seq is available
			if not get
			next verify that all sectns are the most recent
			if there is not then

		store needs to be hooked directly allowing execution of the storage
		action or hooked by the write module to output the string for the command to handle the storage action
		that the lookup table exists and needs to be located if the data value is not an id
		then it is assumed that at a minimum the user is unaware of the lookup table
		try to find the lookup table...it could be that two similar tables exist
		it also could be that a table exists but this entry is a new item it will also need
		to be able to determine which lookup table is the most appropriate
		Potentially move this sane to the calcgen text module
		pheonix.analyze
		need to add grammar as a rule set for a language
	todo: >
		Integrate File Lock mechanism as needed

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


		Control I/O for relational database formats#							||=>Describe class
			Create a generic datastructure class that allows for usage of various
			different datastructures from the fxsquirl module configured to integrate
			with nchantrs displays
			use transactions List Model with ability to filter model data based on column
			keywords for creating a spreadsheet like table of data
			Build a generic Datastructure model for read and write of data for the
			nchants application
			this is the basis position of integration for the future fxsquril engine
		database as a source
		how to access the database as a source

		source for a tree??
		source for a tab??

		yaml file as a source

	expirary: <[expiration]> #											||
	version: <[version]> #												||
	authority: document|this #											||
	security: sec|lvl2 #												||
	<(WT)>: -32 #														||
''' #																	||
import os, re, copy, pandas as pd, zipfile as zipf#						||
try:#																	||
	from git import Repo#												||
except:#																||
	print('git import at Elements.Store failed')#						||
#=======================================================================||
import datetime as dt, re#							||
from os.path import abspath, dirname, exists, getsize, join
import queue, time#															||
#=======================================================================||
from pandas import DataFrame
import pyodbc as sql, sqlite3 as sql3#									||
from osbrain import run_nameserver, run_agent#							||
#===============================================================================||
from condor import condor, thing#												||
from fxsquirl import collector
from fxsquirl.orgnql import fonql
from fxsquirl.objnql import objnql#						||
from fxsquirl.orgnql import orgnql#						||
from excalc import exam, text as calct, data as calcd#							||
from rhino.ossys import linux
#=======================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
log = True
#=======================================================================||
pxcfg = join(abspath(here), '_data_/fxsquirl.yaml')
class Chunk(object):
	''' '''
	def __init__(self, chunk):
		''' '''
		self.chunk = chunk
		self.sectnUUID = chunk['sectnUUID']
		self.sectnSize = chunk['sectnSize']
		self.text = chunk['Text']
		self.dtid = chunk['DTID']
		self.tipe = chunk['Type']
		self.state = chunk['State']
	def expand(self):
		''' '''
		self.decoded = encoder(self.text, self.sectnSize).decode()
		return self
	def compact(self):
		''' '''
		self.encoded = encoder(self.text, self.sectnSize).encode()
		return self
	def consume(self):
		''' '''
		what = thing.what().gen()
		when = thing.when().gen()
		self.db.write(record)
		for x in next(wb.worksheet()):
			x = calcd.stuff(x).tbl_2_str()
			sectnuuid = next(what)
			tree = {'t_sectns', {
						'columns': ['SectnUUID','Text','DTID','Type','State'],
						'records': [sectnuuid, x, next(when), tipe,
									self._determinesectnstate(x)]},
					't_docs', {
						'columns': ['docUUID', 'Name','Seq','SectnUUID','DTID',
									'Group','State'],
						'records': [next(what), name, seq, sectnuuid, next(when),
									group, self._determinedocstate()]}
					}
		self.db.write(record)
	def calcSize(self):
		''
		return self
		self.text = text
		self.size = size
	def decodeSeq(self):
		cols, rows= size.split([',','.','|'])
		nrow = [sectnUUID, seq]
		for col in cols:
			for row in rows:
				for line in text.split('\n'):
					tbl.append(line)
		return self
	def encodeSeq(self, cnt, seq):
		''
		return self
	def decodeText(self):
		''
		return self
	def encodeText(self, uuid=None):
		''
		if uuid == None:
			sectnUUID = thing.what().uuid
		return self
	def _determineSectnState(self, data):
		'determine if data contains code....need to be very careful how to handle'
		'working squashing any autoexecuting code with the ability to step it through'
		'if wanted.....'
		return self
	def _determineDocState(self):
		'doc state at this point is always going to be 0'
		return self
	def _type(self):
		if dbtype == 'POSTGRESQL':
			if len(cols) > 1590:
				#need to build a table splitter to handle table with columns over
				#1600 need to allow for admin cols
				#how to handle the complexity of inserts
				return None

class Chunker(collector.engine):
	'''Chunker will fractionalize and queue the sql statements executing them
	 	recursively working from the bottom of the queue but allowing
		reorganization through interaction from the user to adjust execution
		priorities'''
	version = '0.0.0.0.0.0'
	def __init__(self, doc, name: str='fxsquirl', cfg: dict={}, rst: int=0):
		'''Take from Queue of cmds and from queue of datasources'''
		self.config = condor.instruct(pxcfg).override(cfg)#		||load config
		collector.engine.__init__(self, self.config)
		self.name = name
		self.initDB(doc, rst)
		self.initStack()
		self._qlrtr(doc)
	def append(self, data, cfg=None):
		self.touch(self.place)
		self.dh.doc(self.place).append(data)
		return self
	def carveSource(self):
		''' '''
		self.sectnUUID = self.schunk['sectnUUID']
		self.sectnSize = self.schunk['sectnSize']
		self.text = self.schunk['Text']
		self.dtid = self.schunk['DTID']
		self.tipe = self.schunk['Type']
		self.state = self.schunk['State']
		return self
	def checkDBSize(self, path):
		'''Return Size in Megabytes '''
		if exists(path):
			return getsize(path)/1024/1024
		return 0
	def close(self):
		'''Run a routine storing the inmem database to the ondisk database '''
		source = 'inmem'
		self.setSource(source, 'all').setSink(self.name)
		inmemtables = self.sink[source]['store'].getTables().dikt
		filetables = self.sink[self.name]['store'].getTables().dikt
		for table in inmemtables.keys():
			if table in filetables.keys():
				updateTable(table)#update that data in the file db from inmem
			elif 'bg_' in table:
					splittable()
			elif '' in table:
				pass
		try:
			self.setSink(self.name).collect(load)
			self.setSource('inmem', 'sharedmemdb').collect()#dump to crash_sharedmemdb_<(date)>
			self.setSource('inmem', 'filememdb').collect()#dump to crash_filememdb_<(date)>
			self.setSource('inmem', 'appmemdb').collect()#dump to crash_appmemdb_<(date)>
			self.setSink(self.name).collect({'recover': True})
		except Exception as e:
			self._crash(e)
		return self
	def cmd(self, phile):
		self.skrp = store.stuff(phile).read().text
		#outputs a file/cmd to a file that will perfom the action when
		#executed is this viable outside of the original sql implemntation?
		#this would go along way towards generating streamlined versions
		#without the dynamica routing where it isn't needed due to specific
		#use cases
		return self#													||
	def cmdFractionalizer(self, cmd, targets):
		'''split cmd so that different sections can be pulled from different
			tables this is mainly intended to allow the use of the inmem
			database for active data and to take the same actions on stored data
			as well as moving the data between these states
			will need to leverage the sonql.builder function at alow level
			to duplicate cmd across various databases and table structures'''
		return self
	def compact(self):
		'''Leverage data encoding to compact a multi dimensional dataset into a
			2-dimensional dataset'''
		if uuid == None:
			sectnUUID = thing.what().uuid
		self.encoded = encoder(self.text, self.sectnSize).encode()
		return self
	def copy(self, to, touch='Soft'):#								||=>Define method
		#expand this through the router
		''
		if cfg == None:
			cfg = {'page': 100}
		if 'skrp' not in cfg.keys():
			cfg['skrp'] = self.cmd
		next(self.odoc.copy(to, cfg))#								||call read dhandler
		return o
	def copyAs(self, to, tipe='CTD', touch='Soft'):
		'''Given a store output a representation of the store in a different
			syntax'''
		while self.go == True:
			inpt = next(self.read)
			okind = exam.thing(to)
			otpt = self.write(inpt)

		return self
	def createRecord(self, record=[]):
		'''Create a New record in the connected datastore '''
		print('Record', record)
		return self
	def edit(self, data):#												||
		'Edit store from files to filesystems to dbases'#				||
		return self#													||
	def deleteRecord(self, record):
		'''Delete the given record from the connected datastore'''
		return self
	def disposition(phile, action=None):#modify this to function with any type of tranform of a fs
		if action == 'Kill':#Kill will move the file to a grave and let the life maintenace system take over the handling of the file
			grave = mps+'/History/'+tdy#								||
			if not os.path.exists(grave):#								||
				os.makedirs(grave)#										||
			shutil.move(phile,grave)#									||
		elif action == 'Desenegrate':#desenegrate removes the file and all copies of it from the system
			shutil.remove(phile)#										||
			return#														||
		elif action == 'Hold':#											||#holds the file in its current position
			return#														||
		elif action == 'Relocate':#										||move the file to a new sturctured home
			shutil.copyfile2(phile,action['home'])#						||
		return#															||
	def dropDB(self):
		'''There is some issue with deleting and then creating the same file
			with python even using python to launch a bash process
			probably a better option to drop the tables inside the database
			instead anyway as this is more easily transferable to a
			centeralized db'''
		if log: print('DropDB')
		self.sink[self.name]['store'].drop('ALL', 'view', 3333)
		self.sink[self.name]['store'].drop('ALL', 'table', 3333)
		return self
	def dropTable(self, table):
		'''Drop a table by name from the database'''
		self.sink[self.name]['store'].drop(table, 'table', 3333)
		return self
	def dropView(self, view):
		'''Drop a view by name from the database'''
		self.sink[self.name]['store'].drop(table, 'view', 3333)
	def edit(self):
		'''Combine multiple write features to allow for editing data and table
		structures as needed to increase the number of columns in a table '''
		return self
	def expand(self):
		''' '''
		'''Decode sequence splits a single field into is row and column
			components based on the type of data encoding used'''
		cols, rows= size.split([',','.','|'])
		nrow = [sectnUUID, seq]
		for col in cols:
			for row in rows:
				for line in text.split('\n'):
					tbl.append(line)
		self.decoded = encoder(self.text, self.sectnSize).decode()
		return self
	def filize(self):
		'''Turn Stream of Data into a File Like Object'''
		self.phile = io.StringIO(self.text)
		return self
	def getCodes(self, part):
		''' '''
		codes = []
		for sectn in self.config.dikt[part]['codes']:
			codes.append(sectn['symbol'])
		return codes
	def getModelSrc(self, mdlt: str, srct: str, dataview: dict={}, root=None):
		'''Return a data structure that can be input to a data model in any
			pheonix system, specifically nchants and warlock along with any
			future data model expansions provide the ability switch between a
			dict datastore and a table datastore'''
		if mdlt == 'tree':
			if isinstance(dataview, dict):
				#processing the tree requires walking the tree and interperating
				#sources to generate additional tree data to be subbed into the
				#main tree outline part of this should be pushed down into subtrix
				data = next(self._processTree(srct, dataview, mdlt, root), None)
			elif isinstance(dataview, (list, DataFrame)):
				data = next(self._processList(dataview, mdlt), None)
		elif mdlt == 'pane':
			#this is wrong decoupling needs to move the name of this view back to the tablemodels file
			if log: print('Pane Dataview', dataview)
			view = list(dataview.keys())[0]
			cols = dataview[view]['columns']
			data = next(self._processPane(view, cols), None)
		elif mdlt == 'table':
			view = list(dataview)[0]
			cols = dataview[view]['columns']
			data = next(self._processPane(view, cols), None)
		return data
	def initDB(self, doc, reset: int=0):
		'''Select data structure and data storage configurations then initialize
			data system by dropping all assets if exists and then creating
			new assests in the database at the configured location'''
		self.db = doc.format(self.name)
		#size = self.checkDBSize(self.db)
		#if size < 100:# if the overall size of the database is less than 100MB then load the whole thing into case
		#	db = 'fullcache'
		#else:
		db = 'db'
		if log: print('InitCollector', self.name.lower())
		self.initCollector(self.db, db, self.name.lower())
		if reset == 3659:
			self.dropDB()
			if log: print('Store', self.config.dikt)
			self.buildDB(self.config.dikt['config'])  #creates new database asset structure
		return self
	def initStack(self, reset: int=0):
		'''Initalize the command stack that the chunker will use to work through
			data requests from the application the stack expects to see a list
			of commands
		 	- stack:  contains a dictionary with keys target, sqlcmd, range, requires
		 	- failed: contains a dictionary with keys target, sqlcmd, range, requires, fails'''
		self.stack, self.failed =  [], []
		return self
	def load(self):
		'''Read data from on disk database and write to inmem database '''
		params = {'table': ['state', 'preferences']}#startup file configurations
		#load basic data to in memdb to start the application..include min data
		#to load last state of application
		self.setReader(params, 'filedb').setExtract().extract()
		params = self.dataset
		self.setReader(params).setSink('filememdb').collect()
		return self
	def lock(self):
		'check for existence of lock file...create lock file'
		#lock file should be a readable copy of the needed file?
		#keep updating the lock file
		return self
	def move(self, to, touch='Soft'):#								||=>Define method
		#expand this through the router
		o = orgnql.fsonql.doc(self.doc).move(to)
		return o
	def optimize(self):
		#perform metrics on stores and try to optimized for highest use cases
		#optimize for storage, avialiablity, security, redundancy, speed,
		return self
	def read(self, cfg, fx=None, tipe='load'):
		'''Accepts a configuration for the read function which is broken down
			and translated into single and multiple database reads

			Read from the correct database based on application state
			lets start with a single db setup

			output a tree of dataframes
			'''
		if tipe == 'active':#	||read data from inmem table for current interactions
			mapp = self.docMap[self.docUUID]
			self._conAPP(mapp['FILE'])
			self.doc = self.filedb.read(self.docUUID)
			#if read hits extents of active data and more is available then trigger a load read
		elif tipe == 'load':#	||read data from the ondisk table
			pass
		elif tipe == 'close':#	||read data from the ondisk table for version update comparisons
			pass
		rdr = self.sink[self.name]['store'].read(cfg)#this is going lowlevel and
		#needs to be moved up in order to leverage multisink/multisource IO
		#rdr = self.extract({'cmd': cfg['query']['cmd']})
		while True:
			data = next(rdr, None)#progress this to utilizing the Sectn protocol with multiple sources and multiple lines of data per entry
			if log: print('Data', data.dfs)
			if data == None :#or 'cmd' not in data.dfs.keys():
				if log: print('Break out of FXSQuRIL Read')
				break
			#yield data.dfs['cmd']
			yield data
		yield DataFrame()
	def read_store(self, fill=None, cfg=None):#							||=>Define method
		''
		if cfg == None:
			cfg = {'page': 100}
		if 'skrp' not in cfg.keys():
			cfg['skrp'] = self.cmd
		end = next(self.odoc.read(fill, cfg),None)#				||call read dhandler
		if end == None:
			return self
		self.text = self.odoc.text
		self.lines = self.odoc.lines
		self.table = self.odoc.table
		self.dikt = self.odoc.dikt
		self.frame = self.odoc.frame
		if not isinstance(self.frame, pd.DataFrame):
			self.frame = pd.DataFrame(self.frame)
		if not self.frame.empty:
			self.describe = {'Head': self.frame.head(),
							'Info': self.frame.describe(),
							'Size': {'DataSize': self.frame.shape,
										'MemSize': self.frame.info()}}
		self.tree = self.odoc.tree
		self.kind, okey = self.odoc.kind, list(self.odoc.kind.keys())[0]
		try:
			self.philes = self.odoc.philes
		except:
			self.philes = None
		self.go = self.odoc.go
		yield self#													||=>
	def refreshTableMap(self):
		'''Table map provides live mapping'''
		self.tblMap = []
		return self
	def sane(self, things, inc='exc'):
		self.odoc.sane(things, inc)
		return self
	def saveRecord(self):
		''' '''
		return self
	def setUpdater(self, updaters):
		'''Updaters are methods and sources that will be used to provide ongoing
			data aquistion for the application, either through a scheduled
			process, user trigger or manual button'''
		self.updaters = updaters
		return self
	def start(self):
		'''Process Stack of commands...meant to decouple the user interface from
			the data processing'''
		self.stop = False
		while not self.stop:
			uuid, target, cmd, range, requires = self.stack.pop(len(self.stack)-1)
			if requires != []:
				if uuid in self.failed['requires']:
					#need to be able to search all failed requires and handle accordingly
					self.search()
			try:
				self._process(target, cmd, range)
			except Exception as e:
				#strip all cmds that depend on the failed out at the same time
				#then bring the failure back to the users or switch to a failover
				#target which may be more costly to query but increased likely hood
				#of completing the request
				self.failed.append([cmd, dt.datetime.now(), 1])
				if log: print('Stack Process Failed', e)
	def stop(self):
		'''Update the stop variable to stop the fxsquirl processing service '''
		self.stop = True
		return self
	def update(self):
		'''Update data store by creating a version of the exisiting data the
			merge the new data with the exising data in a temp dir then copy
			into original location when complete'''
		self.read()#													||
		totemp = workdir+'/'+'<[workorder]>_'+uuid+'/'+self.doc#		||
		self.move(totemp)#												||
		datamatch = findmatch(data, self.doc)#need to match section of data to be edited
		self.write(data)#												||
		return self
	def touch(self, to, touch='Soft'):#								||=>Define method
		o = orgnql.fonql.doc(self.doc).touch(to)
		return o
	def transfer(self, to='sonql'):
		#build a method to push the data into a database
		#return snippets and translate all functions to the remainder
		#of the dataset within the query to be ran when needed
		return self
	def unlock(self):
		'delete lock file'
		return self
	def ver(self, kind):#														||=>Define module
		'Create version of stored thing'#								||=>Describe module
		if kind == 'lvl0':#												||
			self.copy('zz-hist_/','Hard')
		elif typ3 == 'image':#											||
			pass#														||
		elif typ3 == 'contextual':#										||
			pass#														||
	def verify(self):#													||=>Define module
		''#																||=>Describe module
		self.exrtr()#													||
		if self.dconf.okey != None:#									||
			self.out = True#											||
		return self#													||
	def write(self, payload, tipe=''):#default crash
		'''Any given payload is processed and written to the database structure
			process the given payload to turn into storable data'''
		self._processPayload(payload)
		table = 'test'
		wrtr = self.sink[self.name]['store'].write(payload)
		if tipe == 'active':#	||write data to new interaction data to the inmem table
			wrtr = self.sink[self.name]['store'].write({table: self.data})
		elif tipe == 'clean':#
			wrtr = self.sink[self.name]['store'].write({table: self.data})
		elif tipe == 'crash':#	||emergency dump write of all in memory data
			wrtr = self.sink[self.name]['store'].write({table: self.data})
		elif tipe == 'load':#	||write data to the inmem table from the ondisk table
			wrtr = self.sink[self.name]['store'].write({table: self.data})
		return self
	def write_store(self, data, ext='.txt', force=None, tabs=None):#			||=>Define module
		'write data to persistent data recording medium'#				||=>Describe module
		self.touch(self.place)
		if force != None:
			ql = self.config['force'][force]
			self.dh = config.instruct(ql).modulize().obj#				||set handler and objectify
		self.dh.doc(self.place).write(data)#							||execute dhandler document
		return self#													||=>
	def _clude(self, things):#											||
		found, notfound = [], []
		if isinstance(self.thing, list):#								||
			for self.it in self.thing:#									||
				if self._clude(things):#								||
					found.append(self.it)#								||
				else:#													||
					notfound.append(self.it)#							||
			return found, notfound#										||
		elif isinstance(self.thing, dict):#								||
			return self._treecludr(things)#								||
		else:#															||
			return self._cludr(things), None#							||
	def _cludr(self, things):#											||
		things = self.validate('_cluder', things)#						||
		for clude in things:#											||
			if clude in self.it:#										||
				cludr = True#											||
				break#													||
		cludr = False#													||
		return cludr#													||
	def _crash(self, e):
		'''Run a routine dumping the inmem database to a new on disk file.  to
			be used in periods of instability of the application to attempt to
			ensure a recoverable dataset on the next run of the application'''
		load = {'crashed': True, 'recover': False, 'failed': e}
		self.setSink('appdb').collect(load)
		self.setSource('inmem', 'sharedmemdb').collect()
		self.setSource('inmem', 'appmemdb').collect()
		self.setSink('filedb').setSource('inmem', 'sharedmemdb').collect()
		self.setSource('inmem', 'filememdb').collect().collect({'recover': True})
		return self
	def _process(self, cmd, name):
		''' '''
		if name in self.sink.keys():
			self.sink[name]['store'].run(cmd)
		elif name in self.src.keys():
			self.src[name]['store'].run(cmd)
		return self
	def _processPane(self, view, cols):
		''' '''
		self.setReader({'view': [view]}, self.name)
		self.initExtract(cols, 'dataframe', view)
		self.extract(view, {}, 'base', True)
		yield self.cache.store[view]
	def _processTree(self, srct, dataview, mdlt, pnode=''):
		'''Process a given tree integrating given data with data pulled from
		other sources detailed within the given data tree returning a consistent
		tree set of fully integrated data

		what value does this give over a more direct programmatic pull of data.
		the idea is the ability to interweave tree node data.  the other way
		to accomplish would be to create mock data tables with extra node data

		and then index the entire structure
		so its integrating it at the tree level or the data table level

		redesign this to write the tree provided in the cfg to the
		nodes table		'''
		if srct == 'view':
			'''need to turn extracted sql data table into a tree model table'''
			for key in dataview.keys():
				self.setReader({'view': [key]}, self.name)
				cols = dataview[key]['columns']
				self.initExtract(cols, 'dataframe', key)
				self.extract(key)
				if log: print('Tree', self.cache.store[key])
				yield self.cache.store[key]
		else:
			if tree == {}:
				yield tree
			cnt, ntree = 0, {}
			while True:
				if len(tree.keys()) == 0:
					break
				node = list(tree.keys())[cnt]
				if node == '<(SOURCE)>':  #a source node redirects the lookup
					#how to define a data source here?
					dnode = list(tree[node].keys())[0]  #moves the node down to the entry point sub
					utree = tree[node][dnode]
					tree[pnode] = {}  #erase everything below node previous to loop
					#lnode = list(tree[list(tree.keys())[0]].keys())[0]  #loop node is input point for table data
					getr = self.read({'view': {utree['view']: utree}}, '')
					lcnt = 0
					node = pnode
					while True:
						data = next(getr)
						if data.empty:
							break
						columns = utree['columns']
						ncolumns = []
						for col in columns:
							if isinstance(col, str):
								ncolumns.append(columns.index(col))
							else:
								ncolumns.append(col)
						treed =calcd.stuff(data).recurdexer(ncolumns,True).dikt#||
						cfg = {}
						if '<(OUTLINE)>' in utree.keys():
							cfg = utree['<(OUTLINE)>']
						dtree = treeBuilder(treed, ncolumns, cfg)#
						ntree = next(self._processTree(dtree, mdlt, node))
						yield ntree
				else:
					ntree[node] = next(self._processTree(tree[node], mdlt, node))
				#yield ntree
				cnt += 1
				if cnt >= len(tree.keys()):
					break
				pnode = node
			yield ntree
	def _qlrtr(self, doc, kind=None, cfg=None, tid=None):#						||
		'''how to determine routes between grid, obj, struct, orgnql'''#		||=>Describe module
		self.doc, self.place = doc, doc#										||set document var
		self.text, self.lines, self.table = '', '', []#							||
		self.dikt, self.frame, self.tree = {}, pd.DataFrame(), {}#				||
		self.givn = self.doc#													||set given var
		self.how = None#														||set down configuration
		ex = exam.thing(self.doc)#												||
		self.kind, self.okey = ex.kind, ex.okey#						||
		if self.okey == 'objnql':#										||chk key for data object
			self.dh = objnql#											||set doc handler object
			m = ['Object Storage Key Found',self.okey]
		elif self.okey == 'orgnql':#									||chk key for data organized
			self.dh = orgnql#											||set doc handler object
			m = ['Organzation Storage Key Found',self.okey]
		elif self.okey == 'cryptonql':
			self.dh == cryptonql
			m = ['Cryptographic Storage Key Found',self.okey]
		else:#															||
			m = ['No Storage Key Found',self.okey]#						||
			comm.see(m)
		self.odoc = self.dh.doc(self.doc, self.kind)#					||
		return self#													||=>
	def _treecludr(self, things):#										||=>Define method
		treesane = tree.stuff(self.thing, self.kind
													).clude(things)#	||
		found, notfound = treesane.found, treesane.notfound
		return found, notfound#											||
	def _validate(self, method, given):
		if method == '_cluder':
			if isinstance(given, str):
				given = [given, ]
				changed = True
		return given, changed
class FileLockException(Exception):
	pass
class FileLock(object):#												||
	''' A cross platform file locking mechanism with context-manager
								support for use in a with statement'''#	||
	def __init__(self, file_name, timeout=10, delay=.05):
		'''Specify the file to lock maximum timeout and the delay
									between each attempt to lock.'''#	||
		self.is_locked = False#											||
		self.lockfile = os.path.join(os.getcwd(),
												"%s.lock" % file_name)#	||
		self.file_name = file_name#										||
		self.timeout = timeout#											||
		self.delay = delay#												||
	def acquire(self):#													||
		''' Acquire lock If the lock is in use, check every `wait` seconds.
			until either lock is gained or exceeds `timeout` number of
					seconds, in which case it throws an exception.'''#	||
		if self.is_locked:#												||
			return#														||
		start_time = time.time()#										||
		while True:#													||
			try:#														||
				self.fd = os.open(self.lockfile,#						||
									os.O_CREAT|os.O_EXCL|os.O_RDWR)#	||
				break;#													||
			except OSError as e:#										||
				if e.errno != errno.EEXIST:#							||
					raise#												||
				if (time.time() - start_time) >= self.timeout:#			||
					raise FileLockException("Timeout occured.")#		||
				time.sleep(self.delay)#									||
		self.is_locked = True#											||
	def release(self):#													||
		'''delete the lockfile when working in a `with` statement#		||
					, this gets automatically called at the end.'''#	||
		if self.is_locked:#												||
			os.close(self.fd)#											||
			os.unlink(self.lockfile)#									||
			self.is_locked = False#										||
	def __enter__(self):#												||
		""" Activated when used in the with statement.#					||
			Should automatically acquire a lock to be used in the with block."""
		if not self.is_locked:#											||
			self.acquire()#												||
		return self#													||
	def __exit__(self, type, value, traceback):#						||
		""" Activated at the end of the with statement.#				||
			It automatically releases the lock if it isn't locked."""#	||
		if self.is_locked:#												||
			self.release()#												||
	def __del__(self):#													||
		'''Make sure that the FileLock has been removed'''#				||
		self.release()#													||

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
		if log: print(cnt)
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
		if log: print(cnt)
def makeFS2Cherrytree(name, path, opath, cfg=None):
	NB = nb.doc(name)
	tree = next(fonql.doc(path).read()).dikt
	for key, val in tree.items():
		if key == ':::PHILES:::':
			for phile in val:
				tree.createCell(phile)
		else:
			tree.createNode(key)

def IndexBuilder(dbo, index, cmd):
	''' '''
	dbo.run(index, cmd)
	return
def TableBuilder(dbo, cfg):
	''' '''
	dbo.write(cfg)
	return
def TablePopulator(dbi, itable, filtrs, dbo, otable):
	''' '''
	filtr = {'WHERE': {'IN': {}}}
	for filt, filtvs in filtrs.items():
		filtr['WHERE']['IN'][filt] = filtvs
	rdr = dbi.read({'table': [itable]}, filtr)
	while True:
		data = next(rdr, None)
		if data == None or data.dfs[itable].empty:
			break
		dbo.write({otable: data.dfs[itable]})
def treeBuilder(tree: dict, columns: list=[], cfg: dict={}):
	'''Waltk through dict transforming any lists and/or dataframes into
		nodes in the tree'''
	ntree = {}
	for key in tree.keys():
		if isinstance(tree[key], dict):
			ntree[key] = treeBuilder(tree[key])
		elif isinstance(tree[key], list) and columns != []:
			for column in columns:
				ntree[key] = {tree[key][0][column]: treeBuilder({}, [], cfg)}
		elif isinstance(tree[key], DataFrame):
			pass
		else:
			ntree[key] = {}
	return ntree
def ViewBuilder(dbo, view, cmd):
	''' '''
	dbo.run(view, cmd)
	return
#==========================Source Materials=============================||
'''
https://www.eversql.com/faster-pagination-in-mysql-why-order-by-with-limit-and-offset-is-slow/
https://www.sqlite.org/backup.html
https://www.sqlite.org/inmemorydb.html
https://www.sqlite.org/malloc.html

https://greek0.net/blog/2016/05/28/resource_management_with_python/
https://docs.python.org/3/library/contextlib.html

implement context manager decorator so the with statement can be used with store
https://hackernoon.com/understanding-git-fcffd87c15a3
http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-python/

'''
#============================:::DNA:::==================================||
'''
<(DNA)>:
	201804101534:
		coupling:
			version: <[active:.version]>
			test:
			description: >
				Couple tmplts and data with rule systems implicitally
				and explicitally
			work:
	201804101534:
		here:
			version: <[active:.version]>
			test:
			description: >
				Define Rule Routing for Utilization of Multiple Rule Systems
			work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
