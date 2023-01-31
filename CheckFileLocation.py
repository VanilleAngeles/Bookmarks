#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
This program is checking the current directory.
If P1 file is present:
	ask if we use current directory
	else check P1 location from $HOME and inquire the new location
Source:
Manage files and directories: https://python.doctor/page-gestion-fichiers-dossiers-python
Find directory: https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
Looking for files: https://www.developpez.net/forums/d1946193/autres-langages/python/contribuez/chercher-fichiers-arborescence-version-recursive-glob-glob/
Translate $HOME: https://stackoverflow.com/questions/4028904/what-is-a-cross-platform-way-to-get-the-home-directory
"""
from pathlib import Path
import os, glob, json, sys
from colorama import Fore, Back, Style
script_version = "0.1"
script_name    = 'CheckFileLocation.py'
python_version = sys.version.split(' ')[0]

def check(FileName):
	# Looking for file on current directory
	currentDirectory = os.getcwd()
	# Check if File is present
	boolJsonFile = True
	try:
		open(FileName, 'r')
	except:
		boolJsonFile = False
	yes = {'yes','y', 'YES', 'Y'}
	# If JsonFile present, ask for use the current directory; else ask for new directory
	if boolJsonFile:
		print(script_name, '[R] Current directory is ', currentDirectory)
		JsonFileRequest = script_name
		JsonFileRequest += ' [I] Do you want to change Y[N]'
		iDirectory = input(JsonFileRequest)
		if iDirectory in yes:
			chgtDir(FileName)
	else:
		chgtDir(FileName)
	return()

def chgtDir(JsonFileName):
	# Change directory location
	# First, go to $HOME directory
	Home = str(Path.home())
	os.chdir(Home)
	# Locate JsonFile in directory tree
	listJsonFiles = []
	for fileName in glob.iglob(os.path.join(Home, "**", JsonFileName), recursive=True):
		listJsonFiles += [fileName]
	# Print JsonFiles located with list index
	iJsonFiles = -1
	for jsonFile in listJsonFiles:
		iJsonFiles += 1
		print (script_name, '[I]', Style.BRIGHT + Fore.RED + str(iJsonFiles) + Style.RESET_ALL, jsonFile)
	JsonFileRequest = script_name
	JsonFileRequest += ' [R] Json file to update (Return = Exit)'
	iJsonFile = input(JsonFileRequest)
	if not iJsonFile: exit()
	# Check the answer
	try:
		int(iJsonFile)
	except:
		print(script_name, '[E] your input is not an integer')
		exit()
	if (int(iJsonFile) < 0 or int(iJsonFile) > int(iJsonFiles)):
		print(script_name, '[E] your input is out of range')
		exit()
	# Go to new directory 
	pathJsonFile = listJsonFiles[int(iJsonFile)]
	os.chdir(os.path.dirname(pathJsonFile))

if __name__ == '__main__':
	if not sys.argv[1]:
		print (script_name, '[E] need a parameter')
	else:
		check(sys.argv[1])
	exit()