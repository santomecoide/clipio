#  -*- coding: utf-8 -*-
import rdflib
import unicodedata
import re

from semantics.cucco.cucco import Cucco

class Preprocessor:
	def __init__(self):
		self.__norm = Cucco(language='es')
		self.__norms = [
			'remove_extra_whitespaces',
			'remove_stop_words',
			('replace_punctuation', {'replacement': ''}),
			#('replace_symbols', {'replacement': ''})
		]
		
		self.__pattern = r"\W+"
		self.__ngram = 1
		self.__lower = False

	def __normalization(self, text):
		#text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
		return self.__norm.normalize(text, self.__norms)	

	def __get_tokens(self, text):
		terms = re.split(self.__pattern, text)
		terms = [self.__stemmer(t) for t in terms if len(t.strip()) > 0]
		return terms

	def __tokenizer(self, text):
		n = self.__ngram
		norm_text = self.__normalization(text=text) 
		terms = self.__get_tokens(text=norm_text)
		if n == 1:
			return terms
		n_grams = []
		for i in range(0, len(terms) - n + 1):
			n_grams.append(" ".join(terms[i:i+n]))
		return n_grams

	def __stemmer(self, term):
		if self.__lower:
			term = term.lower()
		return term

	def __clean_text(self, text):
		text = text.replace(',', '')
		text = text.replace(';', '')
		text = text.replace('.', '')
		text = text.replace('?', '')
		text = text.replace('¿', '')
		text = text.replace('!', '')
		text = text.replace('¡', '')
		text = text.replace(':', '')
		text = text.replace('"', '')
		text = text.replace("'", '')
		text = text.replace("(", '')
		text = text.replace(")", '')
		text = text.replace("[", '')
		text = text.replace("]", '')
		text = text.replace("{", '')
		text = text.replace("}", '')
		text = text.replace("-", '')
		text = text.replace("—", '')
		text = text.replace('...', '')
		text = text.lower()
		return text

	def get_tokens(self, text):
		text = self.__clean_text(text)
		return self.__tokenizer(text)
