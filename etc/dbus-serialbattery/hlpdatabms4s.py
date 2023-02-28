# -*- coding: utf-8 -*-
from battery import Protection, Battery, Cell
from utils import *
from struct import *
import locale




class HLPdataBMS4S(Battery):
    def __init__(self, port, baud, address):
        super(BatteryTemplate, self).__init__(port, baud, address)
        self.type = self.BATTERYTYPE

    BATTERYTYPE = "HLPdataBMS4S"
    # how does the length check work???
    LENGTH_CHECK = 0
    LENGTH_POS = 0

    def test_connection(self):
        # call a function that will connect to the battery, send a command and retrieve the result.
        # The result or call should be unique to this BMS. Battery name or version, etc.
        # Return True if success, False for failure
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        result = False
        try:
            result = self.read_status_data()
        except:
            pass

        return result

    def get_settings(self):
        # After successful  connection get_settings will be call to set up the battery.
        # Set the current limits, populate cell count, etc
        # Return True if success, False for failure

        self.cell_count = 4
        self.capacity = 100
        # self.max_battery_charge_current = 1000
        # self.max_battery_discharge_current = 1000
        self.max_battery_voltage = 3.65 * self.cell_count
        self.min_battery_voltage = 3.0 * self.cell_count
        self.hardware_version = "HLPdataBMS4S x.x"        
        self.poll_interval = 8000
        
        return True

    def refresh_data(self):
        # call all functions that will refresh the battery data.
        # This will be called for every iteration (1 second)
        # Return True if success, False for failure
        result = self.read_status_data()

        return result

    def read_status_data(self):
        status_data = self.read_serial_data_HLPdataBMS4S("m1")
        # check if connection success
        if status_data is False:
            return False
 
        par = status_data.split(",").
        if len(par) < 8:
            return False
        
        par[0] = par[0].replace("m1\n", "");
        
# v1,v2,v3,v4,current,soc,chargeoff,loadoff,vbat2,socnow,adj,beep,led,temp1,temp2...         
# 0  1  2  3  4       5   6         7       8     9      10  11   12  13    14...
		
		self.voltage = atof(par[0]) + atof(par[1]) + atof(par[2]) + atof(par[3])
		self.current = atof(par[4])
		self.soc = atoi(par[5])
		if atoi(par[6] == "0":
			self.control_allow_charge = 1;
		else:
			self.control_allow_charge = 0;
		if atoi(par[7] == "0": 
			self.control_allow_discharge = 1;
		else: 
			self.control_allow_discharge = 0;
    
		# logger.info(self.hardware_version)
        return True


    def read_serial_data_HLPdataBMS4S(self, command):
        # use the read_serial_data() function to read the data and then do BMS spesific checks (crc, start bytes, etc)
        data = read_serial_data(
            command, self.port, self.baud_rate, self.LENGTH_POS, self.LENGTH_CHECK
        )
        if data is False:
            return False

        return data

	def atof(string):
		return locale.atof(string);
	
	
	def atoi(string):
	start = 0
    res = 0
	if string[0] == '-':
		start = 1
    for i in xrange(start, len(string)):
		res = res * 10 + (ord(string[i]) - ord('0'))
	if start == 0:
		return res
	else:
		return -res