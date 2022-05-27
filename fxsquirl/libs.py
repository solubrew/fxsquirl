#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name: FxSQuiRL Libraries Module Python Document
	description: >
	expirary: <^[expiration]^>
	version: <^[version]^>
	path: <[LEXIvrs]>pheonix/fxsquirlcules/collector/collector.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#===============================================================================||
try:
	from memory_profiler import profile
except:
	profile = None
	if log: print('FxSquirl Libs No Memory Profiler Module Installed')
from pandas import DataFrame, concat
try:
	import pdfkit
except:
	pdfkit = None
	if log: print('FxSquirl Libs No PDFKit')
try:
	from pandas_datareader import data as pdr
except:
	pdr = None
	if log: print('FxSquirl Libs No Pandas Data Reader')
import numpy as np
try:
	from diskcache import Cache
except:
	Cache = None
	if log: print('FxSquirl Libs No diskcache module')
