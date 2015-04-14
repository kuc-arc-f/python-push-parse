import serial
import datetime
import sys
import traceback

import com_getparam
import com_func
import com_putParse
import com_logging2
import com_parsePush
import com_appConst

mDevice = "/dev/ttyACM0"

mOK_CODE=1
mNG_CODE=0

def is_validTime(tmBef, tmNow, iMax):
	ret=False
	
	tmSpan     = tmNow - tmBef
	iSpan     = tmSpan.total_seconds()
	print "iSpan="+ str(iSpan)
	if iSpan > iMax:
		ret=True
	return ret

if __name__ == "__main__":
    ser=serial.Serial(mDevice ,9600)
    clsConst  = com_appConst.appConstClass()
    clsParam = com_getparam.getparamClass()
    clsCom  = com_func.funcClass()
    clsParse =com_putParse.putParseClass()
    clsLog = com_logging2.loggingClass()
    clsPush =com_parsePush.parsePushClass()
    
    from datetime import datetime
    tmBef     = datetime.now()
    tmBefPush = datetime.now()

    while True:
        val=ser.readline()
        bFrom = clsParam.Is_fromMC(val)
        if bFrom==True:
        	dic= clsParam.getDict(val)
        	sTime = datetime.now().strftime("%Y%m%d%H%M%S")
        	
        	tmNow = datetime.now()
        	if is_validTime(tmBefPush, tmNow, clsConst.mTimePush):
        		tmBefPush = datetime.now()
        		try:
	        		clsPush.send_push(dic)
	        	except:
					print "--------------------------------------------"
					print traceback.format_exc(sys.exc_info()[2])
					print "--------------------------------------------"
					clsLog.debug( traceback.format_exc(sys.exc_info()[2]) )
        		
        	if is_validTime(tmBef, tmNow, clsConst.mTimeSensor):
        		tmBef = datetime.now()
        		try:
	        		clsParse.send_parse(dic, sTime)
	        	except:
					print "--------------------------------------------"
					print traceback.format_exc(sys.exc_info()[2])
					print "--------------------------------------------"
					clsLog.debug( traceback.format_exc(sys.exc_info()[2]) )
        		
        print("IN :"  + val)
