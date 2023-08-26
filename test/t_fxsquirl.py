#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid: <^(UUID)^>  #														||
	name:  #																	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
'''
# -*- coding: utf-8 -*-
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from squirl.orgnql import fonql
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/t_fxsquirl.yaml'




def test_Chunk():
	''' '''

def test_Chunker():
	''' '''

def test_Chunker_write():
	''' '''

def test_Chunker_write_store():
	''' '''

def test_Chunker_verify():
	''' '''

def test_Chunker_ver():
	''' '''
