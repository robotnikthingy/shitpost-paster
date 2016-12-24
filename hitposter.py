#!/usr/bin/env python3

import json
import os
import pickle
import re
import sys

import urllib.error
import urllib.request

import ctypes
from ctypes import wintypes
import ctypes.wintypes
#import win32con
import time

import pyperclip

from system_hotkey import SystemHotkey
from pymarkovchain import MarkovChain
from random import choice
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice here too
user32 = ctypes.windll.user32

html_rep = {
    '&amp;' : '&',
    '&quot;' : '"',
    '&#039;' : "'",
    '&gt;' : '>',
    '&lt;' : '<'
}

def sanitize( com ):
    retval = re.sub( r'\<.+\>', '', com )
    
    for sym in html_rep:
        retval = retval.replace( sym, html_rep[sym] )
    
    return retval

def load_or_train_board2( thread, board ):
    mc_path = './data/{}-data'.format( thread + board )

    mc = MarkovChain( mc_path )
    
    if not os.path.isfile( mc_path ):
      analyze_thread( mc , thread, board )

    return mc

def train_bot_from_file(filename, botID):
    mc_path = './data/{}-data'.format(botID)
      
    mc = MarkovChain( mc_path )
    
    
    if not os.path.isfile( mc_path ):
      analyze_file(mc, filename )
          
    return mc

def load_or_train_bot_from_file(filename, botID):

		mc_path = './data/' + botID
      
      
		mc = MarkovChain( mc_path )


		if not os.path.isfile( mc_path ):
			analyze_file(mc, filename )
          
		return mc
    
def train_bot_from_thread(thread, board, botID):
    mc_path = './data/' + botID 

    mc = MarkovChain( mc_path )
    
    analyze_thread( mc, thread, board )

    return mc    
		
def train_bot_from_url(botID):
		mc_path = './data/' + botID 
		
		done = False
		
		while(done == False):
			print('input url or type shitpost to generate shitposts when ready')
			url = input()
						
			if url == "shitpost":
				break

			mc = MarkovChain( mc_path )
			analyze_url( mc, url)
			

		shitpost_loop( mc)
			
		return mc
    
def load_bot( botID ):
    mc_path = './data/' + botID

    mc = MarkovChain( mc_path )

    return mc
    
def analyze_thread( mc, thread, board ):
		train_string = u''

		print( 'Training... (may take a while)' )

		train_string += thread_prop2( 'http://a.4cdn.org/'+ board + '/thread/' + thread + '.json' )

		mc.generateDatabase( train_string )

    # Save database and images so we can load them later without rebuilding
		mc.dumpdb()

def analyze_url( mc, url):
		train_string = u''

		print( 'Training... (may take a while)' )
		jsonurl = url.replace( 'boards.4chan.org', 'a.4cdn.org/' )
		train_string += thread_prop2( jsonurl + '.json' )
		mc.generateDatabase( train_string )

    # Save database and images so we can load them later without rebuilding
		mc.dumpdb()

def analyze_file( mc, filename ):
    print( 'Training... (may take a while)' )

    with open(filename, 'r') as myfile:
      data=myfile.read().replace('\n', '')
      
    mc.generateDatabase( data )

    # Save database and images so we can load them later without rebuilding
    mc.dumpdb() 
    
def thread_prop2( threadurl ):
    retval = u''
    
    try:
        response = urllib.request.urlopen( threadurl )
    except ( urllib.error.HTTPError ):
        return retval
    
    data = json.loads( response.read().decode('utf-8') )

    for post in data['posts']:
        if 'com' in post:
            sanitized = sanitize( post['com'] )
            retval += u' {}'.format( sanitized )
    
    return retval    

def shitpost_loop( mc ):
    read = ''
    
    print( 'Hit enter to generate a shitposts. Shitposts will be loaded into clipboard' )

    while read != 'exit':
        read = input()
        r = Tk()
        x = 0
        while x == 0:
          print(x)
          shitpost = mc.generateString()
          pyperclip.copy(shitpost + ' ')
          time.sleep(0.05)
    
def main( args ):
		board = ''
		thread = ''
		botname = ''
		selection = ''
		botname = ''
    
		if not os.path.exists('./data/' ):
			os.makedirs('./data/' )
		
		print("what do you want to do: new, train, open")
		selection = input()
    
		if selection == 'new':
			print('name the bot')
			botname = input()
#			os.path.isfile(fname) 
		
			print ("from where? thread or file?")
			selection = input()
      
			if selection == "thread":
				train_bot_from_url(botname)		
				
			elif selection == 'file':
				print('input filename')
				filename = input()
				
				mc = load_or_train_bot_from_file(filename,botname)
				shitpost_loop( mc )
    
		elif selection == 'train':
			print('train which bot?')
			botname = input()
    
			print('train from where? thread or file?')
			selection = input()
      
			if selection == 'file':
				print('input filename')
				filename = input()
				train_bot_from_file(filename, botname)
      
			elif selection == 'thread':
				train_bot_from_url(botname)			
        
				
		elif selection == 'open':
			print('what bot do you want to open?')
			selection = input()
			mc = load_bot(selection)
			shitpost_loop( mc)
    
    
    
if __name__ == '__main__':
    main( sys.argv[1:] )