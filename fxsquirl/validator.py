
#@@@@@@@@@@@@Pheonix.Organelle.Validator.Validator@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '0bbff182-7151-4e74-8bca-0bf231507762'
	name: Validator Module Python Document
	description: >
		Validate documents and datasets against basic comparisons and
		provided templates
	expirary: <[expiration]>
	version: <[version]>
	authority: document|this
	security: seclvl2
	<(WT)>: -32 #																||
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, dirname, join
import json
#=======================================================================||
from condor import condor#								||
from excalc import calcgen
from fxsquirl import selector
#=======================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
log = False
#=======================================================================||
pxcfg = join(abspath(here), '_data_/validator.yaml')#								||use default configuration

class engine(selector.engine):
	'''The Validator engine is designed to apply various validations to
		the selected data

	Check documents, objects and datasets against templates and rules

	'''

	def __init__(self, cfg=None):
		''' '''#			||
#		self.obj0, self.obj1 = obj0, obj1
#		self.it0, self.it1 = self.obj0.text, self.obj1.text#			||
		self.config = condor.instruct(pxcfg).override(cfg)#	||load configuration file
		selector.engine.__init__(self, self.config)

	def equal(self):
		self.hash0 = thing.what(self.obj0).hashish().it
		self.hash1 = thing.what(self.obj1).hashish().it
		if self.hash0 == self.hash1:
			return True
		else:
			return False
		self.name = rule['Name']#										||
		for criteria in rule['Criteria']['Include']:
			self.inc_criteria[criteria] = rule['Criteria']['Include'][criteria]
			self.exc_criteria[criteria] = rule['Criteria']['Exclude'][criteria]
		for action in rule['Actions']:
			lexi.pheonix.particles.action(action)

#	def edits1(word):
#		splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
#		deletes = [a + b[1:] for a, b in splits if b]
#		transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
#		replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
#		inserts = [a + c + b     for a, b in splits for c in alphabet]
#		return set(deletes + transposes + replaces + inserts)

	def known_edits2(word):
		return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

	def known(self, words):
		return set(w for w in words if w in NWORDS)

	def correct(word):
		candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
		return max(candidates, key=NWORDS.get)

	def spell_text():
		import re, collections
	#	def words(text): return re.findall('[a-z]+', text.lower()):
		def train(features):
			model = collections.defaultdict(lambda: 1)
			for f in features:
				model[f] += 1
			return model
		NWORDS = train(words(file('big.txt').read()))
		alphabet = 'abcdefghijklmnopqrstuvxwyz'

	def portion(self, start=0, inc=10, ordered=False):
		p0, p1, p, l = start, start+inc, start, len(self.obj0.lines)#	||
		while p1 < l:
			if ordered == True:
				m0, m1 = p0, p1
			else:
				m0, m1 = p, l
			chip0 = self.obj0.lines[p0:p1]
			if chip0 in self.obj1.lines[m0:m1]:
				self.static += 1
			else:
				self.delta += 1
			p0, p1 = p1, p1+inc
		self.same = self.static/l
		self.rmv = self.delta/l
		return self

	def words(text):
		return re.findall('[a-z]+', text.lower())

	def train(features):
		model = collections.defaultdict(lambda: 1)
		for f in features:
			model[f] += 1
		return model
		NWORDS = train(words(file('big.txt').read()))
		alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def keymap(self):
		''
		if self.obj0.dikt != {}:#				||
			for k in self.obj0.dikt.keys():
				if k in self.obj1.dikt.keys():
					goodkeys.append(k)

	def evaluation(self, model, train, keys):# Evaluate an algorithm using a cross validation split
		self.data = data
		self.algo = algo
		#evaluate a set of predictions over a various samples of the dataset provided
		#using a sampling map
		return scores

	def inspection(self, predictions):
		#get measures and monitoring tools
		show.show('Y frame is {0}'.format(y[0])).terminal().code('run')
		show.show('X frame is {0}'.format(x['Predictions'])).terminal().code('run')
		obs, c, l, inc, scores = [len(x), [], 0.5, 0.01, {}]#
#		t1, t2 = [x.index[y.0==1], x.index[y.0==0]#target = 1 and target = 0
		a = t1.count()/len(y[0])#accuarcy
		return self

	def whitelist(text, layers):
		for layer in layers:
			if layer in text:
				return True
			else:
				return False

	def blacklist(text, layers):
		for layer in layers:
			if layer in text:
				return False
			else:
				return True

	def contrastCriteria(criteria, fact):
		for criterii in criteria:
			if criterii not in fact:
				return 1
			else:
				return 0

	#modify this to take json document as a rule template that gets filtered against by the rule objects
	def checkRules(facts, rules):
		for rule in rules:
			if rule.exc_subjects:
				subject_vote = contrastCriteria(rule.inc_subjects, message.Subject)
				if rule.inc_subjects and subject_vote == 0:
					subject_vote = compareCriteria(rule.inc_subjects, message.Subject)
			if rule.exc_senders:
				subject_vote = contrastCriteria(rule.inc_subjects, message.Subject)
				if rule.inc_senders:
					subject_vote = compareCriteria(rule.inc_subjects, message.Subject)
			if send_vote == 2:
				rule_vote += 1
			for in_tag in rule.inc_tags:
				subject_vote = compareCriteria(rule.inc_subjects, message.Subject)
			for ex_tag in rule.exc_tags:
				subject_vote = contrastCriteria(rule.inc_subjects, message.Subject)
			for in_body in rule.inc_body:
				subject_vote = compareCriteria(rule.inc_subjects, message.Subject)
			for ex_body in rule.exc_body:
				subject_vote = contrastCriteria(rule.inc_subjects, message.Subject)

	def _validate(self, response):
		''' '''
		#if log: print(f'{response.text}')
		#need to validate response seperately from the json encoding
		try:
			data = json.loads(response.text)#									||
			if log: print(f'Data\n {data}')
			if data == None:
				return None
			if 'status' in data.keys():
				if 'errorcode' in data['status']:#this is specific to coinmarketcap...need to genericize and send with configs
					if data['status']['errorcode'] == 1008:
						return 'XSLOW'
			if 'error' in data.keys():#need to integrate a more thorough error handling
				if log: print(f'Data Error {data}')
				return None
			if 'result' in data.keys():
				if data['result'] == []:
					return None
				else:
					return data['result']
			return data
		except Exception as e:
			if log: print('Validation Error', e, response.text)
			if 'Throttled' in response.text:
				return 'SLOW'
			if 'Expecting value: line 1 column 1 (char 0)' in str(e):
				return 'XSLOW'
			if '<!DOCTYPE html>' in response.text:
				return 'SLOW'
			if 'JSONDecodeError' in str(e):
				return 'ABORT'
			return None
#=======================================================================||
#=======================================================================||
'''
def post_with_err_handling(url, body, headers, timeout=None):
	try:
		r = requests.post(url, json=body, headers=headers, timeout=timeout)
		r.raise_for_status()
	except requests.exceptions.HTTPError as e:
		logger.error("Http Error: {}".format(e))
	except requests.exceptions.ConnectionError as e:
		logger.error("Error Connecting: {}".format(e))
	except requests.exceptions.Timeout as e:
		logger.error("Timeout Error: {}".format(e))
	except requests.exceptions.RequestException as e:
		logger.error("Oops, something went wrong: {}".format(e))
	try:
		return r.json()
	except UnboundLocalError as e:
		# `r` isn't available, probably because the try/except above failed
		pass
	except JSONDecodeError as e:
		logger.error("Did not receive a valid JSON: {}".format(e))
		return {}
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
