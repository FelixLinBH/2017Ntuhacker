import requests
import json
from time import gmtime, strftime
import hashlib

class Card:
	def __init__(self, CardNO, CreditInterestRate, AvailableCredit, CreditCardLimit):
		self.CardNO = CardNO
		self.CreditInterestRate = CreditInterestRate
		self.AvailableCredit = AvailableCredit
		self.CreditCardLimit = CreditCardLimit

class Account:
	serverUrl = "http://54.65.120.143:8888/hackathon/"
	token = ""
	cardArray = []
	def __init__(self, CustID, Pin):
		self.CustID = CustID
		self.Pin = Pin

	def login(self):
		rand_token = strftime("%Y%m%d%H%M%S", gmtime())
		payload = {'CustID': self.CustID, 'UserID': self.CustID, 'PIN': self.Pin , 'Token': rand_token}
		url = self.serverUrl + "login"
		r = requests.post(url, json=payload)
		if r.status_code == 200:
			auth = r.json()
			self.token = auth['Token']
			self.getCreditCard()

	def getCreditCard(self):
		url = self.serverUrl + "CreditCardLimit"
		payload = {'CustID': self.CustID, 'Token': self.token }
		r = requests.post(url, json=payload)
		if r.status_code == 200:
			data = json.loads(r.text)
			for item in data['CreditCardLimit']:
				card = Card(item['CardNO'],item['CreditInterestRate'],item['AvailableCredit'],item['CreditCardLimit'])
				self.cardArray.append(card)
	
	def buySomething(self,cardNo,tranAmt,Note):
		self.login()
		url = self.serverUrl + "CreditCardAuthorize"
		payload = {'CardNO':cardNo,'ExpDate':'1221','TranAmt':tranAmt,'TransactionDescChinese':Note}
		r = requests.post(url, json=payload)
		if r.status_code == 200:
			data = json.loads(r.text)
			if data['TranAmt'] == tranAmt:
				return 1
		return 0

	# fake list
	def getBuyList(self):
		self.login()
		url = self.serverUrl + "PaymentsDue"
		payload = {'CustID': self.CustID, 'Token': self.token }
		print(payload)
		r = requests.post(url, json=payload)
		if r.status_code == 200:
			data = json.loads(r.text)
			print(data)
			
		








account = Account("B199443055","3055")
account.login()
print(account.cardArray[0].AvailableCredit)
# account.getBuyList()
# account.login()
# account.getCreditCard()

# print(account.buySomething(account.cardArray[0].CardNO,'100','test'))






