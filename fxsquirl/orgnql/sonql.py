#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
''' #																			||
--- #																			||
<(META)>: #																		||
	docid: 'c5185013-7cae-4cf6-b7a6-093dfbbe337b' #								||
	name: Elements Level Store.Orgnql Module SQL Extension Python Doc #			||
	description: > #															||
		create SQL statements and issue them against various databases#			||
	expirary: <[expiration]> #													||
	version: <[version]> #														||
	authority: document|this #													||
	security: sec|lvl2 #														||
	<(WT)>: -32 #																||
''' #																			||
# -*- coding: utf-8 -*-
#===============================================================================||
import datetime as dt, re, sys#													||
from os.path import abspath, dirname, join#										||
from os import makedirs
#===============================================================================||
from pandas import DataFrame
import pyodbc as sql, sqlite3 as sql3, copy
try:
	import psycopg2 as psql#				||
except:
	print('No POSTGRESQL Library')
#===============================================================================||
from condor import condor, thing#										||

from subtrix import subtrix#									||

from excalc import exam, text as calct, tree as calctr, data as calcd#								||
from fxsquirl.utils import yieldBreak
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/orgnql.yaml')#									||assign default config

class doc(object):#																		||=>Define class
	'''Control I/O for relational database formats'''#								||=>Describe class
	def __init__(self, doc, kind=None, params=None, cfg=None):#					||=>
		self.doc = doc#															||set doc var
		self.config = condor.instruct(pxcfg).override(cfg).select('sonql')#		||
		self.session = self.config.session
		if kind == None:#														||
			kind = exam.thing(self.doc).kind#									||
		self.kind = kind#						||
		self._findDBType()#														||
		self._conx({'server': '', 'database': self.doc})#													||
		self.dbdata = self.config.dikt[self.dbt]
		self.admindata = calctr.stuff(self.dbdata['cfg'])
		self.dikt, self.build, self.dfs, self.beenChecked = {}, {}, {}, {}

	def builder(self, table: str, how: str='SELECT', what: str='table'):#		||
		'''Build query'''#
		if table not in self.dikt.keys():
			self.dikt[table] = {}#													||set sql cmd container
		if 'columns' not in self.dikt[table].keys() and how != 'DROP':#							||
			self.getTableColumns(table)#										||read columns from table in database
		cfg = self.admindata.it
		cfg['scheme'] = self.scheme
		cols = []
		if how != 'DROP':
			cols = self.validateColumns(list(self.dikt[table]['columns']), how)
		if how == 'SELECT':#													||
			cmd = bldSELECT(cols, table, cfg, self.dbt, self.config.dikt)#		||build select query
		elif how == 'CRE':#														||
			if what == 'table':#												||
				cmd = bldCRETable(cols, table, cfg, self.dbt, self.config.dikt)#||build table creation query
			elif what == 'view':#												||
				cmd = bldCREView(table, cmd, cfg, self.dbt, self.config.dikt)
		elif how == 'INSERT':#													||
			cmd = bldINSERT(cols, table, cfg, self.dbt, self.config.dikt)#		||build insert query
		elif how == 'DROP':#													||
			cmd = bldDROP(table, cfg, self.dbt, what, self.config.dikt)#		||build drop query
		elif how == 'UPDATE':#													||
			cmd = bldUPDATE(cols, table, cfg, self.dbt, self.config.dikt)#		||build update query
		elif how == 'UPSERT':
			cmd = bldUPSERT(cols, table, cfg, self.dbt, self.config.dikt)
		elif how == 'RENAME':
			cmd = bldRENAME(table, cfg['ntable'], cfg, self.dbt, self.config.dikt)
		elif how == 'REV':#														||
			cmd = bldREV(cols, table, cfg, self.dbt, self.config.dikt)#			||build revision query
		self.dikt[table]['columns'] = cols
		self.dikt[table]['cmd'] = cmd
		return cmd

	def checkTable(self, table):
		'''Check if table exists in the connected database'''
		cmd = self.config.dikt[self.dbt]['cmds']['exists_table']
		curs = self.conn.cursor()
		data={'<[table]>': sanitize(table, self.dbt), '<[scheme]>': self.scheme}
#		if log: print('Check Table with cmd')
		data, cmd = runREAD(self.conn, cmd, data, self.dbt)
		if data != []:
			return True
		return False

	def delete(self, data):
		'''Delete records given a where function with the option to use the
			admin fields of actv, dlt'''
		return self

	def drop(self, tables, what: str='table', lock=3321):
		'''Delete database assets defined by given data'''
		if tables == 'ALL':
			prefixes = ['pg_', 'sql_', 'sqlite_']#avoid dropping system tables
			tables = list(self.getInfo(what, True, False).dikt.keys())
			for table in tables:
				for prefix in prefixes:
					if prefix in table:
						tables.pop(tables.index(table))
		if isinstance(tables, str):
			tables = [tables]
		if isinstance(tables, dict):
			tables = tables.keys()
		if log: print('Drop Tables')
		for table in tables:
			if log: print(f'Drop Table {table}')
			self.builder(table, 'DROP', what)
			if lock != 3333:
				return self
			self._run(table, [], 'DROP')
		return self

	def execute(self, cmd: str, table: str=''):
		'''Execute given cmd'''
		if table == '':
			table = self.getTable(cmd)
		self.dikt[table] = {'cmd': cmd}
		self._rurn(table, [], self.getHow(cmd))
		return self

	def expand(self):
		'''Add columns to an existing table
			use revisioning cmd to accomplish this function
			read current table
			create temp table with old and new columns
			drop originial table
			copy temp table to original table name
			drop temp table'''

	def getInfo(self, what='table', getTables=True, getColumns=True):
		'''Retreive Information about the database'''
		if log: print('Get Info')
		if what == 'table':
			cmd = sanitize(self.dbdata['cmds']['all_table'],self.dbt,'cmd')#	||
		elif what == 'view':
			cmd = sanitize(self.dbdata['cmds']['all_view'],self.dbt,'cmd')#	||
		if self.dbt == 'POSTGRESQL':
			table = 'information_schema.tables'
		elif self.dbt == 'SQLT':
			table = 'sqlite_master'
		else:
			print('Get Info from table failed for db type',self.dbt)#		||
		if table not in self.dikt.keys():
			self.dikt[table] = {}
		self.dikt[table]['cmd'] = cmd
		data = {'scheme': self.scheme}
		self._run(table, data, 'SELECT')
		if log: print('Table List Read from Database')
		if getTables:
			records = [t[0] for t in self.dikt[table]['records']]
			if what == 'table':
				self.getTables(records, getColumns)
			elif what == 'view':
				self.getTables(records, getColumns)
		self.dikt.pop(table)
		return self

	def getSchemes(self):
		'''Get all Active Schemes from Database'''
		cmd = self.config[self.dbt]['cmds']['get_schemes']#					||
		self._run(cmd, [])#											||run sql cmd
		return self

	def getTables(self, tables, getCols=True, scheme='Public'):
		''' '''
		for table in tables:#limit the auto grab to 10 tables
			if table == '':
				continue
			if table not in self.dikt.keys():
				self.dikt[table] = {}
			if getCols == True:
				if log: print(f'Get Columns for {table}')
				self.getTableColumns(table)
		return self

	def getTableColumns(self, table):#								||
		'''get columns from database table'''
		table = sanitize(table, self.dbt, 'table')
		cmd = self.dbdata['cmds']['get_columns']#								||pull sql statement from config file
		subs = {'<[table]>': table, '<[scheme]>': self.scheme}#					||
		self.dikt[table]['cmd'] = subtrix.mechanism(cmd, subs).run()[0]
		done = self._run(table, [], 'SELECT')#										||run sql cmd
		if log: print('Get Table Columns', done)
		if log: print('DB', self.dikt[table])
		if done:
			if 'columns' not in self.dikt[table].keys():
				self.dikt[table]['columns'] = []#									||
			for col in self.dikt[table]['records']:#								||
				#if log: print('COL', col)
				if self.dbt == 'SQLT':
					self.dikt[table]['columns'].append(col[1])#						||
				elif self.dbt == 'POSTGRESQL':
					self.dikt[table]['columns'].append(col[2])
		return self#															||

	def getTableLength(self, table):
		''' '''
		cmd = self.config[self.dbt]['cmds']['lengthoftable']#					||
		self._run(cmd, [], 'read', table)
		self.dikt = self.build
		return self

	def read(self, data: dict={}, cfg: dict={}, gfill: dict={}):#					||
		'''Return iterator object to pull data in chunks via offset'''#			||
		if log: print(f'Read Data {data}')
		self.dikt, self.dfs = {}, {}
		if data == {}:
			data['table'] = self.getInfo('table').dikt
			data['view'] = self.getInfo('view').dikt
		how = 'SELECT'
		self.build = data
		if 'WHERE' in cfg:#this is a hack on the merge...replace with config override?
			self.admindata.it['WHERE'] = cfg['WHERE']
			if log: print('WHERE', cfg['WHERE'])
		fill = self.admindata.merge(gfill, None, ':::ROOT:::', 'override').it
		#******************************Hack*************************************
		fill['fill']['<[offset]>'] = 0
		if 'page' in gfill.keys():
			fill['fill']['<[limit]>'] = gfill['page']
		#***********************************************************************
		for key in self.build.keys():# the key could be views or tables
			if key == 'cmd':
				table = key
				columns = extractCmdColumns(self.build[table])
				self.dikt[table] = {'cmd': self.build[table], 'columns': columns}
				while True:
					self._run(key, fill['fill'], how)
					if yieldBreak(self.dikt, table):
						break
					fill['fill']['<[offset]>'] += fill['fill']['<[limit]>']#					||
					self.dfs[table] = DataFrame(self.dikt[table]['records'],
										columns=self.dikt[table]['columns'])#	||
					yield self
					self.dfs[table] = DataFrame()
			else:
				for table in self.build[key]:
					table = sanitize(table, self.dbt)
					self.dikt[table] = {}
					self.builder(table, how)#										||
					self.status = True
					while True:
						self._run(table, fill['fill'], how)
						if yieldBreak(self.dikt, table):
							self.status = False
							break
						fill['fill']['<[offset]>'] += fill['fill']['<[limit]>']#					||
						self.dfs[table] = DataFrame(self.dikt[table]['records'],
											columns=self.dikt[table]['columns'])#	||
						if self.dfs[table].empty:
							self.status = False
							break
						yield self
						self.status = True
						self.dfs[table] = DataFrame()
		yield self

	def rename(self, table, ntable):
		''' '''
		self.build = {table: {}}
		cfg = {'ntable': ntable}
		how = 'RENAME'
		self.builder(how, {}, cfg, what)
		self._run(table, [], how)
		return self

	def validateColumns(self, cols: list, how: str='SELECT'):#						||
		'Increment duplicate columns from data to ensure unique columns'#		||
		tcols = []#																||
		if how == 'INSERT':#													||
			cols += [x.lower() for x in self.admindata.it['admincols'].keys()]
		for col in cols:
			if how != 'SELECT':
				col = sanitize(col, self.dbt, 'col')
			if col in ('creby', 'creon', 'modby', 'modon', 'dlt', 'actv'):
				continue
			while col in tcols:#												||
				col = f'{col}_{0}'.format(thing.what().uuid().ruuid[:5])#		||
			tcols.append(sanitize(col, self.dbt, 'col'))#						||
		return tcols

	def write(self, data, cfg: dict={}):#										||
		'''Leverage SQL Upsert in order to create a comprehensive write
			function '''
		self.dikt = sanitizeRecords(self._configure_data(data))#				||
		self._fillAdminCols()#													||
		self.admindata.merge(cfg, None, ':::ROOT:::', 'override')#				||
		for table in list(self.dikt.keys()):#						||
			if table in ('view', 'index'):
				continue
			try:
				if not self.dikt[table]['columns']:
					continue
			except Exception as e:
				if log: print(f'Columns for Table {table} not available {e}')
				continue
			if log: print('Checktable', table)
			if not self.beenChecked.get(table):
				if self.checkTable(table) == False:#								||
					self.builder(table, 'CRE')#										||
					self._run(table, [], 'CRE')#									||
			self.beenChecked[table] = True#may go bad if something breaks in the self._run preecding this
			if log: print('Check Blank input data')
			if self.dikt[table]['records'] in (None, []):#						||
				continue
			if 'WHERE' not in cfg.keys():#											||
				if log: print('Build INSERT')
				self.builder(table, 'INSERT')#										||
				if log: print('Run INSERT')
				self._run(table, self.dikt[table]['records'], 'INSERT')#			||
			else:#																	||
				if log: print('Build UPSERT')
				self.builder(table, 'UPSERT')#										||
				if log: print('Run UPSERT')
				self._run(table, data[table]['records'], 'UPSERT')#					||
		if 'view' in self.dikt.keys():
			for view in list(self.dikt['view'].keys()):
				self._run(view, [], 'CRE')
		if 'index' in self.dikt.keys():
			for index in list(self.dikt['index'].keys()):
				self._run(index, [], 'CRE')

	def _conx(self, db=None, server=None):#										||
		'''Connect to Database'''#												||
		dbvrs = self.session.ppov['stores']['DBvrs']#							||
		if db != None:#															||
			server = db['server']#												||
			self.dbase = db['database']#										||
		if self.dbt == 'SQLT':#													||
			try:#																||
				dpath = calct.stuff(self.dbase).path()#								||
				if not dpath.valid:
					makedirs(dpath.it)
				self.conn = sql3.connect(self.dbase)#							||assign db connection
			except Exception as e:#												||
				print('Database connection to',self.dbase,'failed due to',e)#	||
		elif self.dbt == 'MSSQL':#												||
			conn = f'DRIVER={{SQL SERVER}};SERVER={server};'
			conn += 'Trusted_Connection-yes;'#									||
			self.conn = sql.connect(conn)#										||
		elif self.dbt == 'MySQL':#												||
			server, port = '192.168.1.210', '3306'#								||
			self.conn = mysql.connect(conn)#									||
		elif self.dbt == 'POSTGRESQL':#											||
			self.conn = psql.connect(**dbvrs[self.doc]['conn'])#				||
		else:
			print('Failed to establish connection to', self.doc)
		return self#															||

	def _configure_data(self, data):
		'''Configure data into a standard form allowing the user to submit in
			various forms

			This whole thing is a hack and needs rebuilt

			'''
		ndata = {}
		if log: print('Data Type',type(data))
		if isinstance(data, DataFrame):#										||
			ndata[thing.what().uuid().hexid[-5:]] = {'records': data.values.tolist(),
														'columns': data.columns}#	||
		if isinstance(data, dict):
			if 'table' in data.keys():
				if not data['table']:
					return ndata
				for table in data['table'].keys():
					if isinstance(data['table'][table], dict):
						if 'dataframe' in data['table'][table].keys():
							records = data['table'][table]['dataframe'].values.tolist()
							columns = list(data['table'][table]['dataframe'].columns)
							ndata[table] = {'records': records, 'columns': columns}
						if 'records' in data['table'][table].keys():
							if isinstance(data['table'][table]['records'], DataFrame):
								if data['table'][table]['records'].empty:
									ndata[table] = {'records': None}
								else:
									records = data['table'][table]['records'].values.tolist()
									columns = list(data['table'][table]['records'].columns)
									ndata[table] = {'records': records, 'columns': columns}
							elif data['table'][table]['records'] in (None, [], [[]], [['']]):
								ndata[table] = {'records': None,
										'columns': data['table'][table]['columns']}
							else:
								#if log: print('Configure Table with data', table)
								ndata[table] = {'records': data['table'][table]['records'],
													'columns': data['table'][table]['columns']}
					elif isinstance(data['table'][table], DataFrame):
						records = data['table'][table].values.tolist()
						columns = list(data['table'][table].columns)
						ndata[table] = {'records': records, 'columns': columns}
			if 'view' in data.keys():
				ndata['view'] = data['view']
			if 'index' in data.keys():
				ndata['index'] = data['index']
			for t in data.keys():
				if t in ('table', 'view', 'index'):
					continue
				if isinstance(data[t], list):
					records = data[t]
					columns = data[t][0]
				elif isinstance(data[t], dict):
					if data[t] == {}:
						records = []
						columns = []
					elif 'records' in data[t].keys():
						if isinstance(data[t]['records'], DataFrame):
							records = data[t]['records'].values.tolist()
							columns = list(data[t]['records'].columns)
						else:
							records = data[t]['records']
							columns = data[t]['columns']
					elif 'dataframe' in data[t].keys():
						if isinstance(data[t]['dataframe'], DataFrame):
							records = data[t]['dataframe'].values.tolist()
							columns = list(data[t]['dataframe'].columns)
					else:
						print('Misconfigured SONQL data', data[t])
				elif isinstance(data[t], DataFrame):
					records = data[t].values.tolist()
					columns = list(data[t].columns)
				else:
					print('Data Table', data[t])
				ndata = {t: {'records': records, 'columns': columns}}
		return ndata

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.conn.close()

	def _fillAdminCols(self):
		'''Fill in data for admin columns, user, timestamps, etc'''
		if log: print('Fill Admin Columns')
		ndata = []
		self._setAdminData()
		for table in self.dikt.keys():#												||
			if 'records' not in self.dikt[table]:
				continue
			bdata, ndata = self.dikt[table]['records'], []#							||
			if bdata == None:
				continue
			self.validateColumns(list(self.dikt[table]['columns']))
			check = False
			for x in list(self.admindata.it['admincols'].keys()):
				if x in self.dikt[table]['columns']:
					check = True
					break
			if check == True:
				ndata = bdata
			else:
				if isinstance(bdata, DataFrame):#							||
					ndata = calcd.df2lists(bdata, self.admindata.it['admincols'])#				||
				elif bdata == None:
					continue
				else:
					for dat in bdata:#											||
						if not isinstance(dat, list):#							||
							dat = list(dat)#									||
						dat.extend(list(self.admindata.it['admincols'].values()))#				||
						ndata.append(dat)#										||
		return ndata

	def _findDBType(self):
		''' '''
		DBvrs = self.session.ppov['stores']['DBvrs']
		if ':' in self.doc:
			self.scheme = sanitize(self.doc[self.doc.find(':')+1:])
			self.doc = self.doc[:self.doc.find(':')]
		else:
			self.scheme = 'public'
		if '.sqlite' in self.doc or '.sqlite3' in self.doc or '.db' in self.doc:#				||
			self.dbt = 'SQLT'
		elif self.doc in DBvrs.keys():
			# Accept known database connections registered to the in session user or there extensions
			self.dbt = DBvrs[self.doc]['type']
		else:
			print('Unknown Database Document', self.doc)
		return self

	def _run(self, table, data: list=[], how='SELECT'):#						||cycle through cmds built to get data from various tables
		'''Fully Execute cmds built in sql document could probably recreate
			this as a method for leverage from the integrated document and a
			adhoc sql execution command'''#										||
		cols, done = [], False#													||
		try:#																	||
			cmd = self.dikt[table]['cmd']#										||
			try:#																||
				cols = self.dikt[table]['columns']#								||
			except Exception as e:#															||
				if log:
					if 'PRAGMA' in cmd:
						print(f'CMD {cmd} quering columns')
					else:
						print(f'CMD {cmd} error {e}')
		except:
			try:
				cmd = self.dikt['view'][table]['cmd']#							||
				try:
					cols = self.dikt['view'][table]['columns']#					||
				except Exception as e:
					if log: print(f'View {table} error {e}')
			except:
				try:
					cmd = self.dikt['index'][table]['cmd']#						||
					try:
						cols = self.dikt['index'][table]['columns']#			||
					except Exception as e:
						if log: print(f'Index {table} error {e}')
				except Exception as e:
					print(f'Else error {e}')
					return False
#		if log: print('Open Connection')
		with self.conn:
			if how == 'SELECT':#												||
				records, cmd = runREAD(self.conn, cmd, data, self.dbt)#				||
				if len(records) == 0:
					if log: print(f'No Records Found using {cmd}')
				self.dikt[table]['records'] = records#							||
				done = True#													||
			elif how in ('CRE', 'DROP', 'INSERT', 'UPSERT', 'WRITE'):#			||
				done = runWRITE(self.conn, cmd, data, how, cols, self.dbt)#		||
				self.conn.commit()
				if log: print(f'{how}ed {table}')
			else:
				if log: print(f'Execution for {how} Failed')
		return done#															||

	def _setAdminData(self):#													||
		''' '''#																||
		self.admindata.it['admincols']['creon'] = thing.when().dtid#			||
		self.admindata.it['admincols']['modon'] = thing.when().dtid#			||
		return self#															||


def backupWRITE(wro, cmd, data, status):
	'''Write database actions to a distributed communications network to ensure
		database backup via syncronized write commmands
		this is an issue with function level access within pheonix
		provide an output object
		'''

	return


def bldCREDatabase(name, owner=None, pxcfg={}):
	if owner == None:
		owner = 'solubrew'
	cmd = f'CREATE DATABASE {name}'
	return cmd


def bldCRESchema(name, dbt, pxcfg={}):
	'Create a new schema'
	name = sanitize(name, dbt)
	return f'CREATE SCHEMA IF NOT EXISTS {name};'#								||

def bldCRETable(cols, table, cfg={}, dbt=None, pxcfg={}):
	'Build Table Creation SQL Statement'
	table = sanitize(table, dbt)#											||
	if 'POSTGRESQL' == dbt:
		if 'scheme' in cfg.keys():
			scheme = sanitize(cfg['scheme'], dbt)#							||
			schtable = f'{scheme}.{table}'
		else:
			scheme = 'public'
		cmd = bldCRESchema(scheme, dbt)#										||
	else:
		cmd, schtable = '', table
	cmd = f"{cmd}CREATE TABLE IF NOT EXISTS {schtable} ("#			||
	icol = f'{table}id'#											||
	if 'POSTGRESQL' == dbt:
		cmd = f'{cmd}{icol} SERIAL PRIMARY KEY '
	elif 'SQLT' == dbt:
		cmd = f'{cmd}[{icol}] INTEGER PRIMARY KEY AUTOINCREMENT '#				||
	for col in cols:#															||
		col = sanitize(col, dbt, 'col')
		if col.lower() == icol.lower():
			continue
		if dbt == 'POSTGRESQL':
			cmd = f'{cmd}, "{col}"'
		else:
			cmd = f'{cmd}, [{col}]'
		columntype = 'text'# supply this with cfg statement to set specifics
		if columntype == 'text':
			if dbt == 'SQLT':
				cmd = f'{cmd} TEXT \n'#											||
			elif dbt == 'POSTGRESQL':
				cmd = f'{cmd} VARCHAR \n'#
		elif columntype == 'integer':
			pass
		elif columntype == 'datetime':
			pass
		constraints = []
		for constraint in constraints:
			if constraint == 'unique':
				cmd = f'{cmd} UNIQUE'
	cmd = bldAdminConfig(cmd, cfg)
	return cmd

def bldAdminConfig(cmd: str, cfg: dict, pxcfg={}):
	''' '''
	lock = 0
	for key in cfg['admincols']:#this could have lots of weird side effects with column naming
		if key.lower() in cmd:
			lock = 1
			break
	if lock == 0:
		acmd = cfg['admincmd']
		cmd = f'{cmd}{acmd}'#											||
	else:
		cmd = f'{cmd})'
	return cmd

def bldCREView(view, select, cfg={}, dbt=None, pxcfg={}):
	'Build View Creation SQL Statement'
	view = sanitize(view, dbt)
	if dbt == 'POSTGRESQL':
		scheme = cfg['scheme']
		view = f'{scheme}.{view}'
		cmd = f'CREATE VIEW {view} AS {cmd}'
	else:
		cmd = f'CREATE VIEW IF NOT EXISTS {view} AS {select}'
	return cmd#							||

def bldCREIndex(cols, table, cfg={}, dbt=None, pxcfg={}):
	'Build Index Creation SQL Statement'
	table = sanitize(table, dbt)
	if dbt == 'POSTGRESQL':
		scheme = sanitize(cfg['scheme'])
		table = f'{scheme}.{table}'
	return cmd

def bldDROP(table, cfg: dict={}, dbt: str='', what: str='table', pxcfg={}):
	'''Build Asset Drop SQL Statement'''
	table = sanitize(table, dbt, 'table', cfg['scheme'])
	if what == 'table':
		cmd = f'DROP TABLE {table}'
	elif what == 'view':
		cmd = f'DROP VIEW {table}'
	elif what == 'index':
		cmd = f'DROP INDEX {table}'
	if dbt == 'POSTGRESQL':
		cmd += ' CASCADE'
	return cmd

def bldGIVEN(gcmd, cfg={}, dbt=None, pxcfg={}):
	''
	table = 'given'
	table = sanitize(table, dbt)
	if dbt == 'POSTGRESQL':
		scheme = cfg['scheme']
		table = f'{scheme}.{table}'
	self.cmdr[table] = {}
	cols = getCmdColumns(gcmd)
	if table not in self.build.keys():
		self.build[table] = {}
	self.build[table]['columns'] = cols
	self.cmdr[table]['cmd'] = gcmd
	return self

def bldINDEX(cmd, dbt=None, pxcfg={}):
	'''Add Index creation statements to the table creation also allow for future
		peformance upgrades by retoractively creating indexes'''
	return self

def bldINSERT(cols, table, cfg={}, dbt=None, upsert=False, pxcfg={}):
	'''Build Data Insertion SQL Statement'''#									||
	table, cmdvals = sanitize(table, dbt), ''
	if dbt != 'SQLT':
		scheme = sanitize(cfg['scheme'], dbt)
		table = f'{scheme}.{table}'
	cmd = f'INSERT INTO {table} ('#												||
	lock = False
	for key in cfg['admincols'].keys():
		if key in cols:
			lock = True
	if lock == False:
		cols += list(cfg['admincols'].keys())
	if log: print('COLs',cols, 'NUM', len(cols))
	for col in cols:
		col = sanitize(col, dbt, 'col')
		if dbt == 'SQLT':
			cmd = f'{cmd}[{col}], '
			cmdvals = f'{cmdvals}?, '
		elif dbt == 'POSTGRESQL':
			cmd = f'{cmd}{col}, '
			cmdvals = f'{cmdvals}%s, '
	cmd, cmdvals = cmd[:-2], cmdvals[:-2]
	cmd = f'{cmd}) VALUES ({cmdvals})'
	if dbt == 'POSTGRESQL' and upsert == False:
		cmd = f'{cmd} ON CONFLICT DO NOTHING'
	return cmd

def bldModify(table, what='table', dbt=None, pxcfg={}):
	'''Modify table  '''
	if what == 'table':
		pass
		#build select
		#build insert
		#build drop
		#build select
		#build insert
		#build drop
	return cmd

def bldRENAME(table, ntable, cfg, pxcfg={}):
	'''Build command to rebuild table with a new name'''
	scheme = cfg['scheme']
	cmd = f'ALTER TABLE {scheme}.{table} RENAME TO {ntable};'
	return cmd

def bldREV(cols, table, cfg={}, dbt=None, pxcfg={}):
	'''Build a Table Revision Query - copy the original table to the same or
		a different database with a different or same name if no conflicts and
		then drop the original table from the first databse and replace with a
		modified table'''
	table = sanitize(table, dbt)
	bldSELECT()
	bldCRE()
	bldINS()
	execute()#create a copy of the existing table drop the existing table
	bldDROP()
	#need to do modifications...add columns, etc...how to determine when this is not a wanted behavior?
	bldCRE()
	bldINS()
	execute()#create a new table populate the new table
	return cmd#																	||

def bldSELECT(cols, table, cfg={}, dbt=None, pxcfg={}):
	'Build SQL Selection Statement for the given sql dialect'
	table = sanitize(table, dbt)
	if dbt == 'POSTGRESQL':
		scheme = cfg['scheme']
		table = f'{scheme}.{table}'#
#	if dbt == 'SQLT':
#		table = f'main.{table}'
	cmd = 'SELECT '#															||
	if cols == []:
		cmd += '*, '
	else:
		for col in cols:#															||
			if dbt == 'SQLT':
				cmd += f'[{col}], '
			else:
				cmd += f'{col} , '
	cmd = cmd[:cmd.rfind(',')]
	if dbt == 'POSTGRESQL':
		cmd = f'{cmd} FROM {table} '
	else:
		cmd = f'{cmd} FROM "{table}" '#											||
	if cfg != None:#															||
		if 'WHERE' in cfg:
			cmd += bldWHERE(cfg['WHERE'], table, dbt, pxcfg)
	if dbt == 'POSTGRESQL':
		colid = calct.stuff(table).trimTo('.').it[1:]
		colid = f'{colid}id'
		if colid in cols:
			cmd = f'{cmd} ORDER BY {table}.{colid}'
		elif 'id' in cols:
			cmd = f'{cmd} ORDER BY {table}.id'
		else:
			print('COLID cant figure out sort',colid)
	else:
		colid = f'{table}id'
		if colid in cols:
			cmd = f'{cmd} ORDER BY {colid}'
	for key, add in cfg['adders'].items():#												||
		cmd += f' {add}'#														||
	#print('SELECT CMD', cmd)
	return cmd

def bldUPDATE(cols, table, cfg, dbt=None, upsert=False, pxcfg={}):
	'''Build SQL to update table'''
	if table != 'scheme':
		if dbt == 'POSTGRESQL':#													||
			scheme, santable = cfg['scheme'], sanitize(table, dbt)
			fulltable = f'{scheme}.{santable}'
		else:
			fulltable = sanitize(table, dbt)
	table = table[table.find('.')+1:]
	if upsert == True:
		fulltable = ''
	cmd = f'UPDATE {fulltable} SET '
	for col in cols:
		colslug = '{'+f'{col}'+'}'
		if col == 'where':
			continue
		cmd += f"{col} = '{colslug}', "
	cmd = cmd[:-2] + bldWHERE(cfg['WHERE'], table, dbt, pxcfg)#						||
	return cmd

def bldUPSERT(cols, table, cfg, dbt: str='POSTGRESQL', pxcfg={}):
	'''Build SQL command to insert unless conflict and then update'''#			||
	if dbt == 'POSTGRESQL':
		ins = bldINSERT(cols, table, cfg, dbt, True)#							||
		upd = bldUPDATE(cols, table, cfg, dbt, True, pxcfg)#							||
		conflict  = '('
		for key in cfg['WHERE'].keys():
			for column in cfg['WHERE'][key].keys():
				conflict += f'{column}, '
		conflict = conflict[:-2]+')'
		cmd = (f'{ins} ON CONFLICT {conflict} DO {upd}')
	elif dbt == 'MYSQL' or dbt == 'MARIADB':
		scheme, santable = cfg['scheme'], sanitize(table, dbt)
		fulltable = f'{scheme}.{santable}'#
	elif dbt == 'SQLITE':
		fulltable = sanitize(table, dbt)#
	return cmd

def bldWHERE(cfg, table, dbt=None, pxcfg={}):
	'''Build where clause for cmd given parameters'''
	cmd, oor, aand = ' WHERE ', False, False
	for how in cfg.keys():
		if how == 'IN':
			if 'OR' in cfg[how].keys():
				incfg = cfg[how]['OR']
				oor = True
			elif 'AND' in cfg[how].keys():
				incfg = cfg[how]['AND']
				aand = True
			else:
				incfg = cfg[how]
			if log: print('INCFG', incfg)
			for key in incfg.keys():
				cmd += f"{key} {how} ('"
				for i in incfg[key]:
					if log: print(f'WHERE item {i}')
					cmd += f"{i}', '"
				cmd = cmd[:-3]+') '

#need to handle both same how and multi how AND OR statements
				if oor:
					cmd += 'OR '
#				if aand:
#					cmd += 'AND '
				else:
					cmd += 'AND '

			cmd = cmd[:-4]
			if oor:
				cmd = cmd[:-3]
			if aand:
				cmd = cmd[:-4]
		elif how == 'NOT IN':
			for key in cfg[how]:
				cmd += f"{key} {how} ('"
				for i in cfg[how][key]:
					cmd += f"{i}', '"
				cmd = cmd[:-3]+') '
		elif pxcfg != {} and how in pxcfg[dbt]['operators'].keys():#			||
			#this is not functioning properly
			oprtr = pxcfg[dbt]['operators'][how]
			for key in cfg[how].keys():
				i = cfg[how][key]
				cmd += f"{table}.{key} {oprtr} '{i}' AND "
			cmd = cmd[:-5]
		elif how == 'BETWEEN':
			for key in cfg[how].keys():
				v1 = cfg[how]['v1']
				v2 = cfg[how]['v2']
				cmd += f' {key} BETWEEN {v1} AND {v2} AND '
			cmd = cmd[:-5]
		cmd += ' AND '
	cmd = cmd[:-5]
	if dbt == 'POSTGRESQL':
		cmd = cmd.replace('[','').replace(']','')
	#print('WHERE CMD', cmd)
	return cmd

def extractCmdColumns(cmd, dbt=None):#										||
	'''Return the columns from a given cmd statement'''#						||
	cols, lvl = [], 1#															||
	if 'SELECT' in cmd:#														||
		bcmd = calct.stuff(cmd).trimTo('SELECT', 'exclude')
		bcmd.trimPast('FROM', 'exclude')#	||
	elif 'INSERT INTO' in cmd:#													||
		find = 'INSERT INTO {table}('
		bcmd = calct.stuff(cmd).trimTo(find, 'exclude')
		bcmd.trimPast(') VALUES (', 'exclude')#	||
	elif 'CREATE TABLE' in cmd:#												||
		find = 'CREATE TABLE IF NOT EXISTS {table} ('
		bcmd = calct.stuff(cmd).trimTo(find, 'exclude')
		bmcd.trimPast('FROM', 'exclude')#			||
	else:#																		||
		comm.see(['Cmd type not found in getCmdColumns',cmd])#					||
		lvl = 2#																||
	if lvl == 1:#																||
		for col in bcmd.it.split(','):#											||
			ncol = calct.stuff(col)
			if ' as ' in col.lower():#											||
				ncol.trimTo(' as ', 'exclude')#							||spaces inc'd for pattern uniqueness
			if '.' in ncol.it:#											||
				ncol.trimTo('.', 'exclude')#				||
			if '\t' in ncol.it:
				ncol.stripper(['\t',' '])#			||
			if '--' in ncol.it:#										||
				ncol.trimPast('--', 'exclude')#				||
			while ncol.it in cols:#										||
				ncol.rename()#											||
			ncol.it = ncol.it.strip('\n').strip(' ')#					||
			cols.append(ncol.it)#										||
	elif lvl == 2:#														||
		for col in bcmd.split(','):#									||
			if ' as ' in col.lower():#									||
				ncol = calct.stuff(col).trimTo(' as ')#					||spaces inc'd for pattern uniqueness
			else:#														||
				ncol = calct.stuff(col).trimTo('.')#					||
			while ncol.it in cols:#										||
				ncol.rename()#											||
			ncol.it = ncol.it.strip('\n').strip(' ')#					||
			cols.append(ncol.thing)#									||
	return cols#														||

def runREAD(conn, cmd, fill: list=[], dbt: str='SQLT'):
	''' '''
	curs, cmd, data = conn.cursor(), subtrix.mechanism(cmd, fill).run()[0], []#	||
	try:
		if log: print(f'EXECUTE READ against {dbt} {cmd}')
		if dbt == 'SQLT':#														||
			data = [list(row) for row in curs.execute(cmd)]#					||
		elif dbt == 'POSTGRESQL':#												||
			curs.execute(cmd)#													||
			data = [list(row) for row in curs.fetchall()]#						||
		try:
			if log: print(f'Run Read Data {data[0]}')
		except:
			print(f'Run Read Data {data}')
	except Exception as e:
		print(dbt,'Read Failed due to',e,'using this cmd', cmd)
	return data, cmd

def runWRITE(conn, cmd: str, data: list, how: str='INSERT', cols: list=[],
								dbt: str='POSTGRESQL', retry=1, backup=False):#	||
	'''Run a write command against the connected database
		provide the option to output a text entry containing the command and
		data for each request.
		send to rabbitmq server
		then distribute it to back up databases
		after verification of execution on the primary database
		if verfication is not received then funnel it back through the primary
		database and write to error logs
	'''
	curs, status = conn.cursor(), False#										||
	if how in ('CRE', 'DROP', 'DELETE'):#										||
		try:#																	||
			curs.execute(cmd)#													||
			status = True#														||
		except Exception as e:#													||
			print(dbt, 'EDIT', 'Write Failed due to',e,'using cmd', cmd)#		||
	elif how in ('UPSERT') and data != None:#									||
		status = runUPSERT(curs, cmd, cols, data, backup)#						||
	elif how in ('INSERT') and data != None:#									||
		status = runINSERT(curs, cmd, data, backup)#							||
	if log: print(f'{how}\n{cmd}\n{data}')#										||
	return status#																||

def runINSERT(curs, cmd, data, backup):#										||
	''' '''
	status = False#																||
	try:#																		||
		status = curs.executemany(cmd, data)#									||
		if log: print(f'INSERT Status {status}')#								||
		if backup == True:#														||
			backupWRITE(wro, cmd, data, status)#								||
	except Exception as e:#														||
		print(dbt, 'INSERT', 'Write Failed due to',e,'using cmd', cmd)#			||
		print('Data', data[0], 'Num', len(data[0]))#							||
	return status#																||

def runUPSERT(curs, cmd, cols, data, backup):
	''' '''
	status = False
	for d in data:
		d = [sanitize(x, dbt, 'content') for x in d]
		fcmd = cmd.format(**dict(zip(cols, d)))
		try:
			status = curs.execute(fcmd, d)
			if backup == True:
				backupWRITE(wro, cmd, data, status)
		except Exception as e:
			conn.commit()# commit any work outstanding on current cursor
			print(dbt, 'UPSERT', 'Write Failed on data','due to',e)
			print('Data', d[0])
			curs = conn.cursor()# initate a new cursor to continue operation
	return status

def sanitize(entry, dbt=None, etype='table', scheme=None):
	''' '''
	if entry == None:
		return None
	if etype == 'table':
		if dbt == 'SQLT':
			entry = entry.replace("\'", '')
			entry = calct.stuff(entry).trimPast('.').it
		elif dbt == 'POSTGRESQL':

			#entry = f'{scheme}.{entry}' build this in later

			entry = entry.replace('-','_')
			entry = entry.replace('=','_')
			entry = entry.lower()
			if entry[:1].isdigit():
				entry = 'a{0}'.format(entry)
			if ':' in entry:
				entry = calct.stuff(entry).trimTo(':').it
		entry = calct.stuff(entry).trimPast('.').it
	elif etype == 'col':
		if dbt == 'SQLT':
			pass
		elif dbt == 'POSTGRESQL':
			special = ['from', 'to']
			entry = entry.replace('-','_')
			entry = entry.replace('=','_')
			entry = entry.lower()
			if entry[:1].isdigit():
				entry = 'a{0}'.format(entry)
			if entry in special:
				entry = f'"{entry}"'
	elif etype == 'cmd':
		if dbt == 'SQLT':
			pass
		elif dbt == 'POSTGRESQL':
			pass
	elif etype == 'content':
		if isinstance(entry, str):
			entry = entry.replace("'", "<apostrophe>")
			entry = entry.replace('"', '')
			entry = entry.replace('%', '<percent>')
	return entry

def sanitizeRecords(dikt):
	lock = 0
	for table in dikt.keys():
		nrecords = []
		#print('Table', table)
		if 'records' not in dikt[table].keys():
			continue
		if dikt[table]['records'] == None:
			continue
		for record in dikt[table]['records']:#intended to filter blank records
			lock = 0
			for field in record:
				if field not in (None, '', []):
					lock = 1
					break
			if lock == 1:
				nrecords.append(record)
		dikt[table]['records'] = nrecords
	return dikt


#=============================Resource Materials================================||
'''
https://dba.stackexchange.com/questions/22362/how-do-i-list-all-columns-for-a-specified-table
https://docs.python.org/2/library/sqlite3.html
https://www.sqlite.org/malloc.html
http://www.numericalexpert.com/blog/sqlite_blob_time/
https://www.eversql.com/faster-pagination-in-mysql-why-order-by-with-limit-and-offset-is-slow/

POSTGRES
https://www.citusdata.com/blog/2016/03/30/five-ways-to-paginate/
https://stackoverflow.com/questions/24761133/pandas-check-if-row-exists-with-certain-values
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
