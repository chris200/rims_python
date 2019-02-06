import serial
from  time import sleep
import mysql.connector


	
def getUpdatefreq():
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="SELECT `seconds` FROM `updatefreq` order by timestamp desc limit 0,1";
	mycursor.execute(sql)
	result=mycursor.fetchone();
	mydb.close()
	return result[0]	

def getAT():
	roger=sendcmd("R_AT:"+"\r\n")
	#print "roger " + roger
	postATToDb(roger)		
	
def getTT():
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="SELECT `targettemperature` FROM `targettemperaturelog` order by timestamp desc limit 0,1";
	mycursor.execute(sql)
	result=mycursor.fetchone();
	for x in result:
		print x
		#ser.write(("W_TT:"+str(x)+"\r\n"))
		sendcmd("W_TT:"+str(x)+"\r\n")
	sql="UPDATE `targettemperaturelog` set `flag` =0, `modified`= CURRENT_TIMESTAMP() where `flag`=1";	
	mycursor.execute(sql)
	mydb.commit()
	mydb.close()
	

	
def getKP():
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="SELECT `kpvalue` FROM `kpvalues` order by timestamp desc limit 0,1";
	mycursor.execute(sql)
	result=mycursor.fetchone();
	for x in result:
		print x
		#ser.write(("W_TT:"+str(x)+"\r\n"))
		sendcmd("W_KP:"+str(x)+"\r\n")	
	mydb.close()
	
def getKI():
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="SELECT `kivalue` FROM `kivalues` order by timestamp desc limit 0,1";
	mycursor.execute(sql)
	result=mycursor.fetchone();
	for x in result:
		print x
		#ser.write(("W_TT:"+str(x)+"\r\n"))
		sendcmd("W_KI:"+str(x)+"\r\n")		
	mydb.close()
	
def getKD():
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="SELECT `kdvalue` FROM `kdvalues` order by timestamp desc limit 0,1";
	mycursor.execute(sql)
	result=mycursor.fetchone();
	for x in result:
		print x
		sendcmd("W_KD:"+str(x)+"\r\n")		
	mydb.close()
	
def postATToDb(roger):
	val=roger.split(":")
	val=val[1]
	mydb=mysql.connector.connect(
		host='127.0.0.1',
		user='myuser',
		password='mypassword',
		database='rims')
	mycursor=mydb.cursor()
	sql="INSERT INTO  atlog (temperature) VALUES (%s);" %(val)
	mycursor.execute(sql)
	mydb.commit()	
	#print val
	mydb.close()	
	
	
	
	
	
def writeserial(cmd):
	#sleep(2)
	#print "Writing Serial";
	ser.write(cmd)

def sendcmd(cmd):
	writeserial(cmd)
	#print "cmd in: " + cmd
	output=readserial()
	#print "cmd out : " + output
	return output

def readserial():
	while True:
			data=ser.readline()
			return data;
	

	

somedata=12
ser=serial.Serial("/dev/ttyACM0",9600)
sleep(1)
updatefreq=getUpdatefreq();
#print updatefreq;
# getTT();
# getKP();
# getKI();
# getKD();
print("RIMS RUNNING")

while True:
	sleep(updatefreq-1)
	getTT()
	
	updatefreq=getUpdatefreq();
	
	
	
	
