"""
Run FAN_voltage vs FAN_tach test for a long time.

Usage:
python aging_com.py

2017/10/20, Kevin, V0.1 for fan_aging test.
2017/10/24, Kevin, V0.2 add sensor temp reading 
"""
import serial
import visa
import re
import sys
import time
#import matplotlib.pylot as plt

COM_PORT = 15

# Function to open the serial port
def open_serial_port(port=1, baudrate=9600, timeout=None):
    #opens the serial port and sends several endlines
    try:
        ser = serial.Serial(
            port=port,              # number of device, numbering starts at
                                    # zero. if everything fails, the user
                                    # can specify a device string, note
                                    # that this isn't portable anymore
                                    # if no port is specified an unconfigured
                                    # an closed serial port object is created
                baudrate=baudrate,      # baud rate
                bytesize=8,             # number of databits
                parity=serial.PARITY_NONE,     # enable parity checking
                stopbits=1,             # number of stopbits
                timeout=timeout,        # set a timeout value, None for waiting forever
                xonxoff=0,              # enable software flow control
                rtscts=0,               # enable RTS/CTS flow control
                interCharTimeout=None   # Inter-character timeout, None to disable
        )
    except:
        print "\nCOULD NOT OPEN SERIAL COM PORT {0}!".format(port + 1)
        print "Make sure it is connected and not being used by another resource."
        sys.exit(-1)
    return ser
	
# Function to read data on the serial port
def send_and_read(ser, command="v\n", token=None, wait_time = 1):
    #sends one command and waits for the response
    response=""
    character=""
    ser.flushInput()    
    cmd_time = stopwatch.Timer()
    ser.timeout = wait_time + 1
    
    ser.write(command)
    print command
    while not response.endswith(token) and (token != None):
        character = ser.read(1)
        sys.stdout.write(character)        
        response = response + character
        if character == "":
            print response+"\nError: did not find token='"+token+"'"
            sys.exit(-1)
        if cmd_time.elapsed >= wait_time:
            break
    return response
	
def open_logfile(name='NONAME', testname='TEST'):
    global logfile
    
    ct = time.ctime()
    all_time = ct[0:3] + '_' + ct[4:7] + '_' + ct[8:10] + '_' + ct[11:19] + '_' +  ct[20:24]
    current_time = ct[4:7] + '_' + ct[8:10] + '_' + ct[11:13] + ct[14:16] + ct[17:19] + '_' +  ct[20:24]
    filename = name + '__' + testname + '__' + current_time + '.txt'
    logfile = open(filename, 'w')

def dmm_setting():
    dmm = rm.open_resource ("GPIB5::1：：INSTR") #setting the dmm GPIB address

def counter_setting():
    freq_counter = rm.open_source ("GPIB5::0：：INSTR")	#setting the freq_counter GPIB address  

def get_board_temp():
    temp = send_and_read(ser, 'testbox board_temp\r', token='C')

    return temp 

if __name__=='__main__':
    
    ser = open_serial_port(port = COM_PORT - 1, timeout = 3, baudrate=115200)
    print ser
    rm = visa.ResourceManager()
    dmm_setting()   
    counter_setting()
	
	
	

    # open log file here!
    open_logfile('BB6502', 'FAN_TACH')
    f = logfile
	
    print "LOGGING START"
    f.write ('Date,Time,FAN_voltage,FAN_tach,Sensor1_temp\n')
	
    for cycle in range (1,10000,1):
	# Connect the GPS UART to front panel
        temp = get_board_temp()
        sensor1_temp = temp[-5:-3]
        Date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        Time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        fan_volt = dmm.query_ascii_values("MEASURE:VOLTage:DC?")
        fan_tach = freq_counter.query_ascii_values("READ:FREQ?")
                                   
        f.write('{0},{1},{2},{3},{4}\n'.format(Date,Time,fan_volt,str(float(fan_tach)*30),sensor1_temp))
        
        print (Time)
        print ("FAN_voltage is : %s"%fan_volt)
        print("FAN_Tach is : %s"%fan_tach)

        time.sleep(60)
	
    f.close

    

