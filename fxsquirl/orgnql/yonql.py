#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
''' #																			||
--- #																			||
<(META)>: #																		||
	docid: 6e712656-cc88-473e-9679-d9cf2e3f4807 #								||
	name: Organisms Level Chronos Module Python Document #						||
	description: > #															||

#Process the reading and writing of yaml formated data
#Describe Rethinkdb Server
#Setup a table that contains documents that are text and can be sucked
#up and rewritten on comamnd
#Setup a table that contains non-text documents and will be filled with
#links and metadata...headers....etc
#Setup a tablet that contains top level directories by device
#	idea being that you could have a mobile device root start
#somewhere within a server directory tree
#setup a table that contains 6 consecutive layers of directories
#along with parent and child information
#	this will be assembled as the overall directory structure as needed
#setup a table that contains shard based ignore patterns

#conn = reql.connect('192.168.1.145',28015).repl().db('LifeFunding')
#rdb.db_create("MentalMonkey").run()
#rdb.db("PhenominalPheonix").table_create("Projects1").run()
#join = ReQL.table("Projects").inner_join(ReQL.table("Projects1"),
#	lambda Projects_row, Projects1_row: Projects_row['id'] ==
#	Projects1_row['id']).zip().run(conn)
TODO: add TOML spec usage

	expirary: <[expiration]> #													||
	version: <[version]> #														||
	authority: document|this #													||
	security: seclvl2 #															||
	<(wt)>: -32 #																||
''' #																			||
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, exists, join#								||
from os import makedirs
import datetime as dt#															||
#================================3rd Party Modules==============================||
try:#																	||
	import rethinkdb as reql#											||
except ImportError:#													||
	print('ReQL Import Fail', ImportError)#								||
from yaml import load as yload, dump as ydump, add_representer#			||

try:#																	||
	from yaml import CLoader as Loader, CDumper as Dumper#				||
except ImportError:#													||
	print('YAML Failed')
try:
	from yaml import load as yload, dump as ydump, FullLoader#			||
except:
	print('YAML Failed')
try:
	from yaml import Loader, Dumper#							||
except:
	print('YAML Failed')
try:
	import simplejson as j
except:
	pass
try:
	from yamllint import linter as yamllinter
	from yamllint.config import YamlLintConfig
except:
	pass
from yamlinclude import YamlIncludeConstructor
import h5py
#===============================================================================||
from condor import condor, thing#								||
from fxsquirl.objnql import txtonql
from excalc import tree as calctr, exam#						||
#===============================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#===============================================================================||
class doc:#																		||=>Define class
	'Control I/O for Raw Structured formats'#									||=>Describe module
	version = '0.0.0.0.0.0'#													||=>Set version
	def __init__(self, doct, kind=None, cfg=None):#								||=>Initiate object
		self.doc = doct#														||set doc variable
		self.doct = doct
		if cfg == None:#														||chk given configuration
			cfg = join(abspath(here), '_data_/orgnql.yaml')#					||use default configuration
		if self.doc != cfg:#													||chk config load loop
			self.config = thing.what(cfg).get().dikt#							||load configuration file
			if 'yonql' not in self.config: print('YONQL', self.config)
			self.config = self.config['yonql']
		self.kind = kind
		try:
			self.tipe = kind[list(kind.keys())[0]]['code']#					||
		except:
			self.tipe = 'YAML'

	def connect(self, server=None, port=None):#							||
		if server == None:#												||
			conn = self.config[self.tipe]['servers']#					||
			server = conn[0]['ip']#										||
		if port == None:#												||
			port = conn[0]['port']#										||
		self.conn = reql.connect(server,port).repl()#					||
		if self.db == None:#											||
			self.db = conn[0]['base']['db']#							||
		#build in connection to the api of websites with simple json output
		return self#													||

	def dbdescribe(self, server, port):
		tables = ReQL.db('rethinkdb').table_list().run(conn)
		for table in tables:
			print('rethinkdb_'+table)
		dbs = ReQL.db_list().run(conn)
		for db in dbs:
			if db != 'rethinkdb':
				tables = ReQL.db(db).table_list().run(conn)
				for table in tables:
					print(db+'_'+table)

	def drop(self, limit=None):#												||
		if self.dikt != None:#													||
			self.entries = self.dikt.keys()#									||
		else:#																	||
			self.entries = None#												||
		if limit == None:#														||
			iis = ['<(META)>', '<(meta)>', '<(DNA)>', '<(dna)>']#				||
			for i in iis:#														||
				try:#															||
					self.dikt.pop(i)#											||
				except:#														||
					pass#														||
		return self#															||

	def filtr(self, filtrLS, depth=None, how='inc'):
		''#									||
		self.dikt = calctr.stuff(self.dikt).filtr(filtrLS, 'search')
		return self

	def load(self, text=None):#													||
		if text == None:
			text = self.doc
		try:#																	||
			text = text.replace('\t','  ')
			doct = f'{text}'#						||correct yaml format
			params = {'loader_class': FullLoader, 'base_dir': self.base_path}#	||
			YamlIncludeConstructor.add_to_loader_class(**params)#				||
			self.dikt = yload(doct, Loader=FullLoader)#							||load yaml str to dikt
		except Exception as e:#													||
			m = ['Couldnt Load YAML document ', text, 'due to', e]#				||
			print(*m)#															||
		return self#															||=>

	def read(self, fill=None, cfg=None, cmd=None):#								||=>Define module
		self.base_path = self.doc[:self.doc.rfind('/')+1]#						||
		try:#																	||
			if self.tipe == 'JSON':#											||
				self.doc = next(txtonql.doc(self.doc).read()).text#				||
				self.dikt = j.loads(self.doc)#									||load json string to dikt
			elif self.tipe == 'HDF5':
				with h5py.File(path, 'r') as doc:#								||
					print('open HDF5')
					self.dikt = doc
			elif self.tipe == 'REQL':#											||
				tables = self.dbdescribe(cfg['server'], cfg['port'])#			||
				if cfg['table'] in tables:#										||
					pass
			elif self.tipe == 'YAML':
				docs = []
				if self.doc[-5:] == '.yaml':#									||
					self.doc = next(txtonql.doc(self.doc).read()).text#			||
				self.dikt = self.load(self.doc).dikt#							||
			else:
				print('Fail')
				self.dikt = {}
		except Exception as e:#													||
			print('YAML Failed due to',e)
			self.dikt, checks = {}, None#										||
			if 'lint' in self.config[self.tipe].keys():#						||
				cfg = self.config[self.tipe]['lint']['defect']#					||
				if self.tipe == 'JSON':#										||
					pass#check = jsonlinter.run()
				elif self.tipe == 'YAML':
					cfg = calctr.stuff(cfg).dict_2_str().it
					cfg = cfg.replace('\t','  ')#								||correct yaml format
					config = YamlLintConfig(cfg)
					doc = self.doc.replace('\t','  ')
					check = yamllinter.run(doc, config)
				checks, go = [], True
				while go:
					try:
						checks.append(next(check))
					except:
						go = False
			m = ['Text ',self.tipe,' Format Error ',checks,
								'This file is improperly formated',self.doct,]
			print(*m)
		self.tree = None#														||
		self.text = self.doc#													||
		self.lines = self.text.split('\n')#										||
		self.table, self.frame = None, None#									||
		self.go = False
		yield self#																||=>

	def write(self, data, tipe=None, fill=None, cfg=None):#						||write dikt file as json str
		''
		add_representer(str, str_presenter)
		table, db, port, server = None, None, None, None#						||
		if tipe == None:
			tipe = self.tipe
		if 'table' in data.keys():#												||
			table = data['table']#												||
			if 'db' in data.keys():#											||
				db = data['db']#												||
				if 'port' in data.keys():#										||
					port = data['port']#										||
					if 'server' in data.keys():#								||
						server = data['server']#								||
		if 'docs' in data.keys():#												||
			data = data['docs']#												||
		create(self.tipe, self.doct, data, table, db, port, server)#				||
		return self#															||=>

	def convert(self, totipe):
		data = self.read().dikt
		self.write(data, totipe)
		return self

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		return self


def str_presenter(dumper, data):
	if len(data.splitlines()) > 1:  # check for multiline string
		return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|-')
	return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def should_use_block(value):
	for c in u"\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
		if c in value:
			return True
	return False


def my_represent_scalar(self, tag, value, style=None):
	if style is None:
		if should_use_block(value):
			 style='|'
		else:
			style = self.default_style
	node = yaml.representer.ScalarNode(tag, value, style=style)
	if self.alias_key is not None:
		self.represented_objects[self.alias_key] = node
	return node


def formatYAML():
	yaml.representer.BaseRepresenter.represent_scalar = my_represent_scalar


def create(tipe, doc, data, table=None, db=None, port=None, server=None):#	||
	if tipe == 'REQL':
		reql.connect(server,port)
		if not db:
			reql.db_create(db).run
		if not table:
			reql.db(db).table_create(table).run()
		reql.db(db).table_populate(table).documents(doc).run()
		for table in tables:#
			if table != '_info' and table != '_WDT':#
				try:#
					r.db(db).table_create(table).run()#
				except:#
					continue#
	elif tipe == 'YAML':#														||
		if log: print(f'YAML Doc {doc}')
		touch(doc)
		with open(doc, 'w') as f:#												||open file
			ydump(data, f, Dumper=Dumper)#										||write file
	elif tipe == 'JSON':#														||
		touch(doc)
		with open(doc, 'w') as doc:#											||
			j.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)#		||write file
	elif tipe == 'BSON':
		pass


def remove():
	if self.tipe == 'REQL':
		pass
	elif self.tipe == 'YAML':
		pass
	elif self.tipe == 'JSON':
		pass
	elif self.tipe == 'BSON':
		pass


def touch(phile):#																||
	here = phile[:phile.rfind('/')]#											||
	if not exists(here):#														||
		makedirs(here)#															||


#==============================Source Materials=================================||
'''
https://github.com/toml-lang/toml
https://www.json.org/
http://www.yaml.org/spec/1.2/spec.html
https://pyyaml.org/wiki/PyYAMLDocumentation
https://github.com/yaml/pyyaml
http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
http://stackoverflow.com/questions/1889597/deleting-directory-in-python
http://rethinkdb.com/docs/security/
https://github.com/crdoconnor/strictyaml
'''
#================================:::DNA:::======================================||
'''
<(DNA)>:
	201804131312:
		doc:
			version: <[active:.version]>
			test:
			description: >
				Read and Write YAML Documents
			work:
	2018041313:
		here:
			version: <[active:.version]>
			test:
			description: >
				Interact with YAML Documents
			work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
