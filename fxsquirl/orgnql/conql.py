# @@@@@@@@@@@@@@@Pheonix.Organelle.Store.OrgnQL.FSonql@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid:
	name:  Module FileSystem Ext Py Doc#		||
	description: >

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/store/store.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
# ===============================================================================||
from os.path import abspath, dirname, join
# ===============================================================================||
from diskcache import Cache
# ===============================================================================||
from condor import condor  # ||

# =============================Common Globals====================================||
here = join(dirname(__file__), '')  # ||
there = abspath(join('../../..'))  # ||set path at pheonix level
version = '0.0.0.0.0.0'  # ||
log = False
# ===============================================================================||
pxcfg = join(abspath(here), '_data_/orgnql.yaml')


class doc():
	''' '''

	def __init__(self, doc=None, kind=None, cfg=None):  # ||exp, cmd
		self.doc = doc  # ||set document var
		self.config = condor.instruct(pxcfg).select('cachonql').override(cfg)  # ||
		self.store()

	def store(self):
		''' '''
		self.store = Cache()
		return self

	def write(self, data):
		''' '''
		if isinstance(data, dict):
			for key in data.keys():
				self.store[key] = data[key]
		return self

	def read(self):
		''' '''
		for key in self.store.keys():
			yield self.store[key]


# ===========================Code Source Examples================================||
# ================================:::DNA:::======================================||
'''
'''
