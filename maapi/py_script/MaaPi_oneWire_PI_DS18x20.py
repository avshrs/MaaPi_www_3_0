#!/usr/bin/python
from MaaPi_Settings import *
import psycopg2
import sys



class MaaPi_OneWire_PI(object):

    def _debug(self, level, msg):
        if self._dbg >= level:
            print "DEBUG {} {:.9f}, {}".format(level, time.time(), msg)
    

    def w1_get_temp(rom_id):
      try:
        w1_file = open('/sys/bus/w1/devices/' + rom_id + '/w1_slave', 'r')
        w1_line = w1_file.readline()
        w1_crc = w1_line.rsplit(' ',1)
        w1_crc = w1_crc[1].replace('\n', '')
        if w1_crc=='YES':
           w1_line = f.readline()
           w1_temp = line.rsplit('t=',1)
           self._debug()
        else:
           w1_temp = 99999
           f.close()
        return int(w1_temp[1])
      except:
        return int(99998)
