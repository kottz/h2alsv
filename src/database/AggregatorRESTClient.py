import http.client
import requests
import json
import time


import base64

'''class JsonResponse(object):
	 def __init__(self,j):
			self.__dict__ = json.loads(j)

class Timeline(object):
	 def __init__(self,j):
			self.fragments = json.loads(j)
			
class Series(object):
	 def __init__(self,j):
			self.fragments = json.loads(j)

class UsersList(object):
	 def __init__(self,j):
			self.users = json.loads(j)'''			

class AggregatorRESTClient:

	def __init__(self, ipaddress, username, password):
		self.username = username
		self.password = password
		self.ipaddress = ipaddress
		#self.port = port #CONNECTING USING HTTPS port 443
		self.token = 0
		self.expiretime = ""

	def encode_data(self,data_string):
		return base64.b64encode( bytes(data_string, "utf-8") ).decode("ascii")

	def decode_data(self,data_string):
		return base64.b64decode( bytes(data_string, "ascii") ).decode("utf-8")

	#old request
	'''def make_request(self,uri,method,body,headers):
		conn = http.client.HTTPConnection(self.ipaddress,self.port)
		conn.request(method,uri,body,headers)
		response = conn.getresponse()
		#print(response)
		#print(response.status)
		response_body = response.read().decode('UTF-8')
		#print(response_body)
		response_status = response.status
		return response_status, response_body'''
		
			
		###SPECIALIZED REQUESTS

	#OK
	def login(self):
		conn = http.client.HTTPConnection(self.ipaddress)
		myheaders = { "Accept" : "application/json", "Content-Type":"application/x-www-form-urlencoded" }
		body = 'username=' + self.username +'&password='+ self.password
		url = 'https://'+self.ipaddress+'/aggregator/service/auth/login'
		r = requests.post(url,data = body, headers=myheaders)		
		self.token = r.headers['Authorized-By']
		if r.status_code == 200:
			self.expiretime = int(time.time()) + 3600
			print("Status: 200 OK")
		else:
			print("Status: ",r.status_code)	
		return r.status_code, r.json()

	#OK
	def refreshToken(self):
		curr_time = (int(time.time())+120)
		if curr_time > self.expiretime:
			print("Getting new token")
			self.login()
		else:
			print("Token valid - Time: "+str(curr_time)+" Expires: " +str(self.expiretime))

	#OK
	def getUsersList(self):
		self.refreshToken()
		uri = '/aggregator/service/users/useridsandpds2'
		myheaders = { "Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json" }
		url = 'https://'+self.ipaddress+uri
		r = requests.get(url, headers=myheaders)
		#print("Status: ", r.status_code)
		userslist = []		
		for element in r.json()["users"]:
			userslist.append([element["id"],element["userName"]])
		return userslist

	def deleteUser(self,user_id):
		uri = '/aggregator/service/users/'+ user_id + '/delete'
		myheaders = { "Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json" }
		url = 'https://'+self.ipaddress+uri
		r = requests.delete(url, headers=myheaders)
		print("Status: ",r.status_code)

	def addEvents(self, user_id, events):
		url = 'https://'+self.ipaddress+'/aggregator/service/users/'+ str(user_id) + '/events/new'
		headers = {"Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json"}
		#print("adding events")
		#json.dumps(events)
		#print(events)
		r = requests.post(url, data=json.dumps(events), headers=headers)
		#print("Status: ",r.status_code)
		return r.status_code

	def getEventsByExample(self, user_id, example):
		url = 'https://'+self.ipaddress+'/aggregator/service/users/'+ str(user_id) + '/events/example'
		headers = {"Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json"}
		#print("getting events")
		r = requests.post(url, data=json.dumps(example), headers=headers)
		#print("Status: ",r.status_code)
		return r.status_code, r.json()

	def getEventsIDsByExample(self, user_id, example):
		url = 'https://'+self.ipaddress+'/aggregator/service/users/'+ str(user_id) + '/events/idbyexample'
		headers = {"Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json"}
		#print("getting events")
		r = requests.post(url, data=json.dumps(example), headers=headers)
		#print("Status: ",r.status_code)
		return r.status_code, r.json()

	def getEvent(self,user_id,event_id):
		self.refreshToken()
		url = 'https://'+self.ipaddress+'/aggregator/service/users/'+ str(user_id) + '/events/' + str(event_id)
		myheaders = { "Authorized-By" : self.token, "Content-Type":"application/json", "Accept":"application/json" }
		r = requests.get(url, headers=myheaders)
		return  r.status_code, r.json()
