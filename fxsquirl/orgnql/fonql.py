#@@@@@@@@@@@@@@@Pheonix.Organelle.Store.OrgnQL.FSonql@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: dfadd6af-4590-44d2-9cd5-4b29e3a2c13f
	name: Elements Level Store.Orgnql Module FileSystem Ext Py Doc#		||
	description: >
		File System Object Notation Query Language
		This script will create a list of all python files stored on the SB data repository
		log all files under the MainST structure
		then search log file and sub section the files based on location, extension, etc...
		do i need to create a revision structure for these logs?

		integrate the pyfilessytem -fs module to handle inmemory
		and remote file system connections
		look at implementing an sql/ite based file system using this api

		look at integrating filecmp
		https://docs.python.org/3/library/filecmp.html

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/store/store.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, exists, isdir, isfile, join
from os import listdir, makedirs, remove, rmdir
import datetime as dt, shutil, time, multiprocessing as mp#			||
import zipfile, tarfile#												||
from distutils.dir_util import copy_tree
from ftplib import FTP#													||
#===============================3rd Party Modules===============================||
try:
	import fs
except:
	pass
#===============================================================================||
from condor import condor, thing#										||
from excalc import text as calct, tree as calctr, data as calcd, exam
from fxsquirl.objnql import txtonql
from subtrix import subtrix#									||
#=============================Common Globals====================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True#																	||
#===============================================================================||
pxcfg = join(abspath(here), '_data_/orgnql.yaml')#								||
class doc:#																		||cmd needs to hold information about coping and/or moving files
	def __init__(self, doc, kind=None, cfg=None):#								||exp, cmd
		self.doc = doc#															||set document var
		self.config = condor.instruct(pxcfg).select('fonql').override(cfg)#		||
		self.config = self.config.dikt['LLFS']#									||load configuration file
		if kind == None:#														||
			kind = exam.thing(self.doc).kind#									||
		self.kind = kind#														||
		self.paths, self.philes, self.filters = [self.doc,], [], []#			||
		self.filters = {'inc': [], 'exc': []}#									||
		self.pool = None#														||
		self.pathslyst, self.sdepth, self.writefiles = [], doc.count('/'), []#	||
		self.date_filters = {}#													||
		self._setCheck()#														||

	def ark(self, to=None):#													||
		'''Archive file subsystem to provided location'''
		return self

	def catalog(self):
		'''Create a list of paths given a specific search conditions these catalog
			files '''
		return self

	def copy(self, to=None, how='full', force='soft', what='COPY'):#			||=>Define method
		'''copy file system default to not overwrite
			...reorganize this into the read function so that the same logic can
			be used generate the list of files and then functions such as move,
			copy, catalog, etc can be selected to done with those results'''#	||=>Describe method
		if self.pool == None:
			self.pool = mp.Pool(self.config['perf']['cores'])#					||
		read = self.read()
		while True:#															||
			go = next(read, None)#												||
			if go == None:#														||
				if log: print('File System Complete')
				break
			rpaths, mpaths = [], self.philes
			for frum in mpaths:#												||
				if self.doc not in frum and force == 'soft':#					||
					continue#													||
				too = frum.replace(self.doc, to)
				touch(too)#														||copy file system no files
				if how in ('full','files'):#									||
					if isfile(frum):#											||
						if what == 'MOVE':
							rpaths.append(frum)
						ftf = (frum, too, force, logf)
						status = self.pool.apply_async(fileCopy, ftf)#	||copy file system
			if what == 'MOVE':
				self._removeCopied(rpaths, to)
		self.pool.close()#														||
		self.pool.join()#														||
		if what == 'MOVE' and rpaths != []:#									||Cleanup empty dirs
			self._removeCopied(rpaths, to)
		return self#															||

	def tmpltCopy(self):
		''' '''
		#need to handle file creation
		#not sure how best to parse out file lines
		lines.sort()
		tree = calcd.stuff(lines).merge().it
		if log: print('Tmplt Copy', lines)
		filename = calct.stuff(lines[0]).filename().it
		for key in tree.keys():
			if key == '<(PATH)>':
				path = lines[2] - lines[1]
				text = next(txtonql.doc(path).read()).text

			elif key == '<(TEXT)>':
				text = lines[3] - lines[2]
		doct = subtrix.mechanism(text, ).run()[0]

	def curl(self):#															||
		path = '/to/path'#														||
		site = 'sitename.com'#													||
		ftp = f'ftp://{site}{path}'#											||
		cmd = f'curl --ftp-create-dirs -T {upload} -u {uname}:{pword} {ftp}'#	||
		return self#															||

	def expand(dikt, dik='', path=''):
		'rebuild the tree in to paths??'
		path += '/'+dik
		for dik in dikt.keys():
			if dik == '::FILES::':
				philedikt = {}
				for phile in dikt[dik]:
					philedikt[phile] = next(store.stuff(path+'/'+phile).read()).dikt
				dikt[dik] = philedikt
			else:
				dikt[dik] = expand(dikt[dik], dik, path)
		return dikt

	def extractFiles(self, dikt, depth=None, cnt=0):#							||
		'get files from the filesystem dictionary'#								||
		philes, cnt = [], 0#													||
		if isinstance(dikt, dict):#												||
			for key in dikt:#													||
				if key == '::FILES::':#								||
					if isinstance(dikt[key], list):
						philes += dikt[key]#								||
					else:
						philes.append(dikt[key])
				else:#													||
					if depth == None or cnt < depth:#					||
						philes += self.extractFiles(dikt[key],depth,cnt)#||
				cnt += 1#												||
		return philes#													||

	def setFilters(self, incFILTRs=[], excFILTRs=[]):
		'Need to integrate set Filters and filtr method'
		self.filters['inc'] = incFILTRs
		self.filters['exc'] = excFILTRs
		return self

	def filtr(self, filtrLS, depth=None, how='inc'):#							||
		''#									||
		if log: print('Filter Philes', self.philes)
		if self.date_filters != {}:
			#filtering date coded file names not attributes
			#is it possible to filter date
			#without some standardized coding template?
			#and bounds dates for which to start
			#
			if 'after' in self.date_filters.keys():
				for phile in philes:
					for filtr in self.date_filters['after']:
						if phdate > filtr:
							pass
			elif 'before' in self.date_filters.keys():
				pass
			elif 'equal' in self.date_filters.keys():
				pass
		self.nphiles = []
		for phile in self.philes:
			if log: print('Filter Phile', phile)
			for filt in filtrLS:
				if how == 'inc':
					if filt in phile:
						self.nphiles.append(phile)
				elif how == 'exc':
					if filt not in phile:
						self.nphiles.append(phile)
		return self#															||

	def ftp(self, uname='Anonymous', pword=None):#								||
		'connect to remote file systems using the ftp protocol'#				||
		ftp = FTP(self.frum)#													||
		ftp.login(user=uname, passwd=pword, accts='')#							||
		ftp.cwd(self.frum)#														||
		f1l3s = ftp.mlsd()#														||
		site = FTP(remote)#														||
		ftp.retrbinary(f'RETR {f1l3}')#											||
		return self#															||

	def move(self, to, how='full', force='soft'):#								||
		'move file default to no-overwrite rename config'#						||=>Describe method
		self.copy(to, how, force, 'MOVE')#										||
		return self

	def read(self, fill=None, cfg=None, cmd=None):#								||
		'''Create a Generator for Reading the Given Filesystem'''#					||
		if self.paths == []:
			self.paths.append(self.doc)
		if cfg != None:#														||
			for key in cfg.keys():#												||
				self.config[key] = cfg[key]#									||
		paths = []#																||
		while self.paths != []:#												||
			if log: print('While Read')
			for p in self.paths:#												||
				if not exists(p):
					if log: print(f'Read Path {p} doesnt exist')
					with open('fonql_error.txt', 'a') as doc:
						doc.write(p)
						self.paths.remove(p)
					continue
				#try:# need to work out dealing with permissions issues "Errno 13"
				for i in listdir(p):
					if log: print(f'file {i}')
					next(self._processSubTree(p, i))
					if log: print('Philes', self.philes)
					if len(self.philes) >= self.config['page']:#			||Set Chunk size
						if log: print('Paths', paths)
						self.dikt = calcd.stuff(self.paths).paths2Tree(True).dikt
						yield self
						for phile in self.philes:#cleanup yielded data source
							if log: print('Remove phile', phile)
							self.paths.remove(phile)
				if log: print('Read paths', self.paths)
				self.dikt = calcd.stuff(self.paths).paths2Tree(True).dikt#					||
				# except Exception as e:
				# 	if 'Errno 13' in str(e):
				# 		if log: print(f'List Dir Permission error for {p}')
				# 	if log: print(f'ListDir Error {e}')
				self.paths.remove(p)
				self.paths.sort()#									||
		yield self#																||

	def select(self, terms):#													||
		self.fs = sane.stuff(self.fs).prune(terms)
		return self

	def touch(self, too):
		touch(too)
		return self

	def write(self, load, force='0'):#											||level of force 0=softest,1=medium,2=hard
		'''Write Data to File Systems'''
		if isinstance(load, str):#												||
			if '::FILES::' not in load:#											||
				if self.doc not in load:#										||
					load = f'{self.doc}/{load}'#					||
				if exists(load):#												||
					self.ark()#													||
				lock = 0#														||
				if exists(load):#												||
					lock = 1#													||
				if force == 1:#													||
					lock = 0#													||
					self.ark(load)#												||
				if lock == 0:#													||
					makedirs(load)#												||
			else:#																||
				if log: print('File Load', load)
				if '::FILES::' == load[-9:]:
					self.check = load
					return self
				if self.check in load:
					self.writefiles.append(load)
				else:
					d = calcd.stuff(self.writefiles).paths2Tree().dikt
					if log: print('fonql D', d)
					createFiles(d)
					self.writefiles = []
					self._setCheck()
		elif isinstance(load, dict):
			self.pathlist(load, 1)#											||
			for line in self.pathslyst:#										||
				self.write(line)#											||
		elif isinstance(load, list):
			self.pathlist(load, 0)#											||
			for line in self.pathslyst:#										||
				self.write(line)#											||
		return self#															||

########################################################################||
#need to replace this properly with a function from calcgen.tree
########################################################################||
	def pathlist(self, load, rte):#										||
		''' The path list write is to allow for writing different data formats
		'''
		if rte == 0:#													||
			for branch in load:#										||
				if self.doc not in branch:#								||
					branch = f'{self.doc}/{branch}'#							||
				self.pathslyst.append(branch)#							||
		elif rte == 1:#													||
			if 'verse' in load.keys():
				root = load['verse']#										||
			else:
				root = self.doc
			if 'tree' in load.keys():
				seed = load['tree']#										||
			else:
				seed = load
			self.branch = calctr.stuff(seed).branch().paths
			for branch in self.branch:#									||
				if self.doc not in root:#								||
					root = root + self.doc#								||
				branch = root + branch#									||
				self.pathslyst.append(branch)#							||
		self.pathslyst.sort()
		return self#													||

	def _setCheck(self):
		''' '''
		self.check = thing.what().hexid
		return self

	def _processSubTree(self, p, i):
		''' '''
		lock = self._filterPath(i)
		if log: print('LOCK', lock)
		if lock != 0:#										||
			yield self#										||
		path = f'{p}/{i}'
		if isfile(path):
			if log: print('Path add to philes ', path)
			self.philes.append(path)#							||
		elif isdir(path):#													||
			if log: print('Path add to paths', path)
			self.paths.append(path)#							||
		else:
			if log: print('Path Not Valid', path)
		yield self

	def _filterPath(self, i, switch=2):
		'''switch: determines whether to check includes, excludes or both '''
		if switch in [0, 2]:
			if self.filters['exc'] != None and self.filters['exc'] != []:#		||
				if log: print('Check Exclude Filters', self.filters['exc'])
				for filtr in self.filters['exc']:#				||Check for exclusion
					if filtr in i:#								||
						return 1#									||
		if switch in [1, 2]:
			if self.filters['inc'] != None and self.filters['inc'] != []:#		||
				if log: print('Check Include Filters', self.filters['inc'])
				for filtr in self.filters['inc']:#		||Check for inclusion
					if filtr in i:#						||
						return 0#						||
				return 1
		return 0

	def _removeCopied(self, rpaths, to):
		''' '''#													||Cleanup empty dirs
		for frum in rpaths:#											||
			if frum == self.doc:
				continue
			too = frum.replace(self.doc, to)
			if not isdir(too):
				if exists(too):
					removePath(frum, 3213)#								||
		rpaths = []
		return self


def compress(frum, name=None, how='tar'):
	''' '''
	cfg = condor.instruct(pxcfg).select('fonql').dikt['ARKFS']#			||
	if name == None:
		name = calct.stuff(frum).dirname().it
	if how == 'tar':
		tarname = f'{frum}.tar.gz'
		if not exists(tarname):
			with tarfile.open(tarname, "w:gz") as t:
				try:
					t.add(frum)
				except Exception as e:
					print('Tar Failed',e,'for file',frum)
	elif how == 'zip':
		zipname = f'{frum}.zip'
		if not exists(zipname):
			with zipfile.ZipFile(frum, "w") as z:
				try:
					z.write(frum, name, compress_type, compresslevel)
				except Exception as e:
					print('Zip Failed',e,'for file',frum)


def createFiles(philes):
	''' '''
	if isinstance(philes, dict):#									||
		for f, text in philes.items():#								||file name and text
			if log: print('File', f, 'Text', text)
			if exists(f):
				#f = iteratename(f)
				txtonql.doc(f).write(text)#							||write file and iterate version
			else:
				txtonql.doc(f).write(text)#										||write file
	elif isinstance(philes, list):#												||
		for f in philes:#														||
			if exists(f):#														||
				store.stuff(f).copy(lastload)#									||
			else:#																||
				store.stuff(f).touch()#											||
	elif isinstance(philes, str):#												||
		if exists(f):#															||
			store.stuff(f).copy(lastload)#										||
		else:#																	||
			store.stuff(f).touch()#												||
	return None


def dirCopy(frum, to, how='Soft'):
	''
	done = False
	try:
		copy_tree(frum, to)
		done = True
	except Exception as e:
		print('Copying Directory',frum,'to',to,'failed due to',e)


def dirMove(frum, to, how='Soft'):
	''
	done = False
	try:
		dirCopy(frum, to)
		done = True
	except Exception as e:
		print('Moving Directory',frum,'to',to,'failed due to',e)
	if done == True:
		dirRemove(frum)


def dirRemove(frum, how='Soft'):
	''
	done = False


def fileCopy(frum, to, how='Soft', logf=None):#									||
	'''Copy files from place to place'''#										||
	try:
		shutil.copy(frum, to)#													||
		return True
	except Exception as e:
		if log: print(f'Copy of {frum} Failed {to} to copy by {how}\n{e}')
	return False


def fileMove(frum, to='hist', how='Soft'):
	done = False
	if to == 'hist':
		to = calct.stuff(frum).historize().it
	elif to == 'pile':
		pass#this needs to connect the session and kick out appropropriately
	try:
		done = fileCopy(frum, to, 'Force')
		if log: print(f'File Copied {done}')
		if done == True and how == ':::KILL:::':
			done = removePath(frum, 3213)
			if log: print(f'File Removed {done}')
	except Exception as e:
		what = 'Copy'
		if done == True:
			what = 'Remove'
		if log: print(f'FileMove Failed to {what} due to {e}')
		done = False
	return done#											||


def outline(srcs, sets):
	''' '''
	tree = pheonix.molecule.anal.fs.describe(srcs.fs)
	for p4th in tree.keys():
		set_p4th = p4th.repalce(srcs.fs, sets.fs)
		if not exists(set_p4th):
			makedirs(set_p4th)
		text = f"Files Cnt: {p4th['files']['cnt']}\n"
		text = f"{text} Files Size: {p4th['files']['size']}\n"
		text = f"{text} Files Newest: {0}\n"
		text = f"{text} Files List: [\n"
		for f1l3 in p4th['files']['list']:
			text = f'{text}\t{f1l3}\n'
		text = f"{text}]\n"
		text = f"{text}Dirs Cnt: {p4th['dirs']['cnt']}\n"
		text = f"{text}Dirs Size: {p4th['dirs']['size']}\n"
		text = f"{text}Dirs Newest: \n"
		text = f"{text}Dirs List: [\n"
		for d1r in p4th['dirs']['list']:
			text = f'{text}\t{d1r}\n'
		text = '{text}]\n'
		with open(set_p4th+'/'+f1l3, 'w') as doc:
			doc.write(text)
		doc.closed
	doc = pheonix.molecule.anal.fs.document(fs)
	pheonix.molecule.anal.fs.snapshot(sets, output, whitelist)


def removePath(this, lock=0000):#												||
	'''Remove given path given the correct lock pin code this ensure intent'''#	||
	if lock != 3213:#															||
		return None#															||
	try:#																		||open try blk
		if isdir(this):#														||
			shutil.rmtree(this)#														||
			if log: print('Remove dir', this)
		if isfile(this):#														||chk if copied file exists
			remove(this)#														||rmv old file
	except Exception as e:#														||open except blk
		print('Error removing file ', this, 'due to ', e)#						||=>Set message
		return False#															||
	return True


def touch(too):#													||
	'''Spawn file subsystem into existence'''#									||
	ptoo = too[:too.rfind('/')]
	if log: print(f'Touch {ptoo}')
	if not exists(ptoo):#										||
		try:
			makedirs(ptoo)#												||
		except Exception as e:
			print('Creating Subdirectories Failed due to',e)#						||
			return False
	if not exists(too) and too != ptoo:
		try:
			with open(too, 'w') as doc:
				doc.write('')
		except Exception as e:
			print('Creating File Failed due to', e)
			return False
	return True#														||


def uncompress(zp, uzp):
	'''Uncompress given compressed file and store to uncompressed location
		zp: absolute pathlike-string
		uzp: absolute pathlike-string
	'''
	cfg = condor.instruct(pxcfg).select('fonql').dikt['ARKFS']#			||
	for ext in cfg['how']['zip']['extensions']:
		if zp[-len(ext):] == ext:
			try:
				with zipfile.ZipFile(zp, "r") as z:
					try:
						if len(z.listOfFileNames()) > 1:
							name = calct.stuff(zp).filename(False).it
							uzp = f'{uzp}/{name}'.format(uzp, name)
							makedirs(uzp)
						else:
							if log: print('NotSure')
					except Exception as e:
						if log: print('Zip Position Failed',e,zp)
						name = calct.stuff(zp).filename(False).it
						uzp = f'{uzp}/{name}'
						makedirs(uzp)
					z.extractall(uzp)
			except Exception as e:
				if 'File exists:' in e:
					continue
				if log: print(f'Unzip of {zp} failed due to {e}')
				errp = '/mnt/overse/library/Software/z-errors/src/'
				if log: print('Error Path', errp)
				if log: print(f'Move Errored File to {errp}')
				fileMove(zp,errp,':::KILL:::')
				if log: print(f'File Moved')
			finally:
				break
	for ext in cfg['how']['tar']['extensions']:
		if zp[-len(ext):] == ext:
			try:
				if ext == '.tar.bz2':
					how = "r:bz2"
				else:
					how = "r"
				with tarfile.open(zp, how) as t:
					if sum(1 for member in t if member.isreg()) > 1:
						name = calct.stuff(zp).filename(False).it
						uzp = f'{uzp}/{name}'
						makedirs(uzp)
					t.extractall(uzp)
			except Exception as e:
				if log: print(f'Untar Failed {e} for file {zp}')
			finally:
				break
	# for ext in cfg['how']['rar']['extensions']:
	# 	if zp[-len(ext):] == ext:
	# 		try:
	# 			with rarfile.open(zp, 'r') as t:
	# 				t.extractall()
	# 		except Exception as e:
	# 			print('Unrar Failed',e,'for file',zp)
	# 		finally:
	# 			break


def uncompressDirectories(path, opath=None):
	''' '''
	if log: print('Uncompress Directory')
	knowndirs = []
	if opath == None:
		opath = path
	for n in listdir(path):
		npath = f'{path}/{n}'
		pos = npath.find('.')
		if not isdir(npath[:pos]):
			uncompress(npath, opath)


#==========================Source Materials=============================||
'''

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
