#!/usr/bin/python3
import requests
import aiohttp
import json
import motor.motor_asyncio
import asyncio
from kd import keyD as kd
from datetime import datetime as datt
import time

import argparse				#Modulo responsavel pelos Argumentos de chamada ao modulo
parser = argparse.ArgumentParser(          prog='apad - IPMABOT',
                    description='''ipmaBot - Recolhe periodicamente dados pela API do IPMA''',
                    epilog='''Este Bot é chamado a recolher dados pelo CRON do sistema operativo. A chamada é feita pelo script sem argumentos''')

start_time = time.time()

parser.add_argument('-unet', '--updatenet',
		action='store_true', help='Update network list and systems',)

class ipmaBot:
	def __init__(self):
		self.systems=[]
		self.data=json.loads('{}')
		self.syncSystems=[]
		self.obdDti=None
		self.obdDtf=None
		self.UrlSystems = "https://api.ipma.pt/open-data/observation/meteorology/stations/stations.json"
		self.urlData="https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
		self.dbcli = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
		self.db=self.dbcli.daphi_signals
		self.syncDts={}
#		print("IPMA BOT - INIT")

	async def maxMinDt(self): 	# devolve maximo e minimo dos Dados recebidos
		self.mindt=datt(3000, 1, 1, 0,0)
		self.maxdt=datt(1900, 1, 1, 0,0)
		for dt in self.datas:
			datim = datt.strptime(dt, '%Y-%m-%dT%H:%M')
			if datt.strptime(dt, '%Y-%m-%dT%H:%M') < self.mindt:
				self.mindt=datt.strptime(dt, '%Y-%m-%dT%H:%M')
			if datt.strptime(dt, '%Y-%m-%dT%H:%M') > self.maxdt:
				self.maxdt=datt.strptime(dt, '%Y-%m-%dT%H:%M')
		await self.writeDB()

	async def writeDB(self):
		self.maxdt=str(self.maxdt).replace(" ","T")[:-3]
		self.mindt=str(self.mindt).replace(" ","T")[:-3]
		for s in self.data:
			await self.db["ipma_"+s+"_sig"].delete_many({"dt":{"$gte":"isoDate("+self.mindt+")","$lte":"isoDate("+self.maxdt+")"}})
		for s in self.data:
			await self.db["ipma_"+s+"_sig"].insert_many(self.data[s])
		for s in self.data:
			dtf=self.syncDts[s][0]
			if len(self.syncDts[s])==1:
				await self.db.lsSystems_sig.update_one({'id': s}, {'$set': {'syncDtf': str(dtf)}})
			elif len(self.syncDts[s])==2:
				dti=self.syncDts[s][1]
				await self.db.lsSystems_sig.update_one({'id': s}, {'$set': {'syncDtf': str(dtf),'syncDti': str(dti)}})			
		print("IPMA BOT - DATA Write into DB")

	async def dataCollect(self):
		ks=kd["ipma"]
		async with aiohttp.ClientSession() as session:		#Request DATA
			async with session.get(self.urlData) as resp:
				if(resp.status==200):
					data=json.loads(await resp.text())

		keys=[]			#corre todo o Objecto e procura as keys assim um systema sem dados é preenchido 
		self.datas=[]		#objecto datas é preechido com datas - determina dt maxima e minima para a DB
		for dt in data:		#dt data atual
			self.datas.append(dt)
			for s in data[dt]:		# s - id de sistema
				if data[dt][s]:
					keys = [ks[k] for k in data[dt][s]]
		jkeys=json.loads('{}')
		for j in keys:
			jkeys[j]=""		#carregar keys JSON para elemento None

		for dt in data:				#Ojecto sem estações vazias
			for s in data[dt]:
				if not data[dt][s]:
					data[dt][s]=jkeys

		for dt in data:			#constroi o obejcto de dados de saida
			for s in data[dt]:
				d=json.loads('{}')
				if not s in self.data:
					self.data[s]=[]
				for k in data[dt][s]:
					d[ks[k]]=data[dt][s][k]
					d["dt"]='isoDate('+dt+')'
				self.data[s].append(d)
		await self.writeSyncDt()
		#print(self.data) #TODO adicionar data maxima e minima por estacao

		print("IPMA BOT - DATA COLLECT")
		await self.maxMinDt()

	async def writeSyncDt(self):
		''' ESCREVE syncDti E syncDtf'''
		def getMaxdt():
			max_dt=datt(1900, 1, 1, 0,0)
			max_dt_str=""
			for d in self.data[sid]:
				dt=d['dt']
				if datt.strptime(str(dt[8:-1]), '%Y-%m-%dT%H:%M') > max_dt:
					max_dt=datt.strptime(str(dt[8:-1]), '%Y-%m-%dT%H:%M')
					max_dt_str=dt[8:-1]
			return max_dt_str

		async def verifyMinSyncDt():
			async for s in self.db.lsSystems_sig.find({"data_src":{"$eq":"ipma"}},{"_id":0}):
				if not "syncDti" in s or s["syncDti"]=='':
					col=s["data_src"]+"_"+s["id"]+"_sig"
					print(col)
					async for dti in self.db[col].find({}).sort("dt",1).limit(1):
						self.syncDts[s["id"]].append(dti["dt"][8:-1])

		for sid in self.data:
			maxDt=getMaxdt()
			self.syncDts[sid]=[maxDt]

		await verifyMinSyncDt()
	'''
	async def putSync(self):
		await self.db.lsSystems_sig.delete_many({"data_src":{"$eq":"ipma"}})
		for s in self.systems:
			if not "syncDti" in s:
				print(s)
			d=json.loads('{}')
			for k in s:
				if not k=="_id":
					d[k]=s[k]
			d["sensors"]={"ra":"","rh":"","ap":"","ws":"","wd":"","wskm":"","at":"","sun":""}
			self.syncSystems.append(d)
		await self.db.lsSystems_sig.insert_many(self.syncSystems)
		print("IPMA BOT - System add to Syncronizer")
		#print(self.syncSystems)
	'''
	async def putSync(self):
		dbcli = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
		db=dbcli.daphi_signals
		for s in self.systems:
			if "syncDti" not in s:
				print(s)
			d = {k: v for k, v in s.items() if k != "_id"}
			d["sensors"] = {"ra": "","rh": "","ap": "","ws": "","wd": "","wskm": "","at": "","sun": ""}
			await db.lsSystems_sig.update_one({"id": d["id"]}, {"$set": d},upsert=True)
		print("IPMA BOT - Systems sincronizados/atualizados")

	async def getAllSystems(self): #lista e insere sistemas na lista de sistemas por rede netwSystems
		#await self.db.netwSystems.delete_many({"data_src":{"$eq":"ipma"}})
		ks=kd["ipmasys"]
		t_syst=requests.get(self.UrlSystems).text
		syst=json.loads(t_syst)
		for s in syst:
			t_sy=json.loads('{}')
			for k in s:
				if k in ks:
					if type(ks[k]) is dict:
						for kk in s[k]:
							if kk in ks[k] and (type(s[k][kk]) is str) or (type(s[k][kk]) is int):
								t_sy[ks[k][kk]]=s[k][kk]
							elif kk in ks[k] and (type(s[k][kk]) is list):
								idx=0
								for kkk in s[k][kk]:
									t_sy[ks[k][kk][str(idx)]]=s[k][kk][idx]
									idx+=1
					else:
						t_sy[ks[k]]=s[k]
			t_sy["netw_name"]="ipma"
			t_sy["data_src"]="ipma"
			t_sy["name"]=t_sy["local"]
			t_sy["type"]="Meteo"
			t_sy["sync"]="-1"
			for i in t_sy:
				t_sy[i]=str(t_sy[i])
				
			self.systems.append(t_sy)
		#print(self.systems)
		##DECOMENTAR PARA PRIMEIRA VEZ
		#await self.db.syncSystems.insert_many(self.systems)

		#print("IPMA BOT - List "+str(len(self.systems))+" Systems")
		await self.putSync()


#asyncio.run(ipmaBot().getAllSystems())

print("IPMA BOT - Execution time %s seconds" % round((time.time() - start_time),2))
loop = asyncio.get_event_loop()
def main():
	args = parser.parse_args()
	if args.updatenet:    #Update lista de networks
		#apadBot().getNetWorks()
		#loop.run_until_complete(ipmaBot().getAllSystems())
		asyncio.run(ipmaBot().getAllSystems())
		print("Excuta listagem de systemas")
	else:
		loop.run_until_complete(ipmaBot().dataCollect())
		#asyncio.run(ipmaBot().dataCollect())
if __name__ == "__main__":
	main()
