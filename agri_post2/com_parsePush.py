# -*- coding: utf-8 -*- 
import requests
import json
import com_appConst

#com_parsePush
class parsePushClass:

	def __init__(self):
		print ""
		
	def is_sendValid(self, dict ,max):
		ret=False
		
		bSen1= False
		bSen2= False
		bSen3= False
		bSen4= False
		nSen1= int(dict["snum_1"])
		nSen2= int(dict["snum_2"])
		nSen3= int(dict["snum_3"])
		nSen4= int(dict["snum_4"])
		sMsg= "s1="+dict["snum_1"] +",s2="+ dict["snum_2"] +",s3="+ dict["snum_3"] +",s4="+ dict["snum_4"]
		print sMsg
		if (nSen1 < max):
			bSen1=True
		if (nSen2 < max):
			bSen2=True
		if (nSen3 < max):
			bSen3=True
		if (nSen4 < max):
			bSen4=True
			
		if((bSen1==True) or (bSen2==True) or (bSen3==True) or (bSen4==True)):
			ret=True
		
		return ret

	def send_push(self, dict ):
		clsConst  = com_appConst.appConstClass()
		
		headers = {
		  "X-Parse-Application-Id": clsConst.mParse_APP_ID ,
		  "X-Parse-REST-API-Key": clsConst.mParse_REST_ID ,
		  "Content-Type": "application/json"
		}
		if( self.is_sendValid(dict, clsConst.mLimitValue )==True):
			from datetime import datetime
			sTime = datetime.now().strftime("%m-%d %H:%M")
			#print "sTime="+ sTime
			nMc = int(dict["mc_id"])
			sMsg="Water require, MC="+ str(nMc) + " [" +sTime+ "]"
			
			dtParam = {}
			dtParam["where"] ={'objectId': {"$exists": True }  }
			dtParam["data"] ={'alert': sMsg }
			#print json.dumps(dtParam)
			try:
				r = requests.post('https://api.parse.com/1/push', headers=headers , data=json.dumps(dtParam), timeout=30)
				print r.status_code
				print r.json()
			except:
				print "failue, send_push"
				raise			
			finally:
				print "End ,send_push"
			

