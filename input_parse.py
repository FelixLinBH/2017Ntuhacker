# -*- coding: utf-8 -*-
import sys , os
import jieba
import jieba.posseg as pseg
import logging
def parse_price(input):
	#support : 
	#	1. 價格區間
	#	2. 價格max
	#	3. 價格min
	#words = pseg.cut("價格在 1000 ~ 5000 間")
	words = pseg.cut(input)	
	nagtive_word = [u"不" , u"不要"]
	exceed_word = [u"超" , u"超過" , u"多" , u"多於" , u"高" , u"以上" u"以外"]
	below_word = [u"便宜", u"少" , u"少於" , u"低" ,u"以內" , u"內" , u"以下"]
	between_word = [u"間" , u"~" , u"到"]
	ch_m = {u"十":10 , u"百":100 , u"千":1000 , u"萬":10000 , u"十元":10 , u"百元":100 , u"千元":1000 , u"萬元":10000 ,u"十塊":10 , u"百塊":100 , u"千塊":1000 , u"萬塊":10000}
	# 0000 -> 1111 = {nat , ex , be , btw}
	search_flag = [0,0,0,0]
	m = []
	for word, flag in words:
		#print word , flag
		if flag == 'm':
			if word in ch_m:
				m[-1] = m[-1]*ch_m[word]
			elif word.isdigit():
				m.append(int(word))
		if word in nagtive_word:
			search_flag[0] = 1
		if word in exceed_word:
			search_flag[1] = 1
		if word in below_word:
			search_flag[2] = 1
		if word in between_word:
			search_flag[3] = 1
	#print zip(["nat","ex","be","btw"] , search_flag)
	m.sort()
	dic = {}
	if len(m) == 0:
		return dic
	if search_flag[0] == 1:
		if search_flag[1] == 1 and search_flag[2] == 0:
			dic['max'] = str(m[0])
		elif search_flag[1] == 0 and search_flag[2] == 1:
			dic['min'] = str(m[0])
	else:
		if search_flag[1] == 1 and search_flag[2] == 0:
			dic['min'] = str(m[0])
		elif search_flag[1] == 0 and search_flag[2] == 1:
			dic['max'] = str(m[0])
		elif search_flag[3] == 1 and len(m) == 2:
			dic['min'] = str(m[0])
			dic['max'] = str(m[1])
			return dic
	return dic
	#print m
def parse_item(input):
	words = pseg.cut(input)
	#items = []
	item = ""
	for word, flag in words:
		#print word , flag
		if flag == 'n' or flag =='eng':
			#items.append(word)
			item += word
			#print "你想要找"  , word , "嗎?"
	return item
	
def get_yahoo_search_pars(s):
	dic = parse_price(s)
	item = parse_item(s)
	dic['q'] = item
	return dic
def talk(s):
	dic = get_yahoo_search_pars(s)
	ret = {}
	if dic['q'] == "":
		ret['statue'] = "undefine"
		ret['response'] = "您想要購買什麼?"
	elif dic['q'] != "" and ("max" not in dic and "min" not in dic):
		ret['statue'] = "noprice"
		ret['response'] = "是否想要指定購買價格範圍呢?"
	else:
		ret['statue'] = "success"
		ret['response'] = dic
	return ret
if __name__ == '__main__':
	#sys.tracebacklimit = 0
	jieba.setLogLevel(20)
	
	"""
	price_strings = ["價格在1000到5000" , "1000~5000" , "高於5000" , "低於5000" , "不要高於5000" , "不要低於5000"]
	item_strings = ["我想要買superdry的衣服" ,"衣服" ,"幫我找衣服" , "幫我找衣服和褲子" , "衣服和褲子"]
	com_strings = ["幫我找電腦"," 我想買iphone"," 我想找1萬以下的手機"," 有uniqlo的衣服嗎？"," 我想買最便宜的iphone"," 3千塊以下的addida"," 有白色的airforce嗎？" , "我想買一台在10000 到 20000的電腦"]
	
	for s in com_strings:
		print s
		print talk(s)
	
	
	"""
	
	com_strings = [com_strings[-1]]
	for s in com_strings:
		print s
		dic = get_yahoo_search_pars(s)
		shall = u"python yahoo_api.py "
		for key in dic:
			print key , dic[key]
			shall += " -"+key +" "+dic[key]
		shall = shall.encode("utf-8")
		print shall
		j = os.popen(shall).read()
		print unicode(j)
	
