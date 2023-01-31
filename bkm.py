#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Source:
FTP: https://www.thepythoncode.com/article/download-and-upload-files-in-ftp-server-using-python
Loop on files: https://gayerie.dev/docs/python/python3/fichier.html#actions-sur-les-fichiers-et-les-repertoires
File charactéristics: https://waytolearnx.com/2019/04/comment-recuperer-la-date-de-creation-modification-dun-fichier-en-python.html
File characteristics Integer: https://askcodez.com/comment-comparer-la-date-de-modification-de-deux-fichiers-en-python.html
Colors: https://pypi.org/project/colorama/
"""
try:
	import argparse,sys,time,os,datetime,json,shutil,math,CryptMac,wget,configparser,locale, gettext, tabulate
	from ftplib import FTP
	from colorama import Fore, Back, Style
	from PIL import Image, ImageFont, ImageDraw
	import CheckFileLocation as cfl
	script_version = "0.1"
	script_name    = 'bookmarks.py'
	python_version = sys.version.split(' ')[0]
except:
	print(script_name, '[E] import error')
	exit()

def start():
	print("-" * 70)
	print(script_name, '[I] (SCRIPT V{:s} - PYTHON V{:s}) - {:s}'.format(script_version, python_version,time.strftime('%I:%M:%S %p')))
	print("-" * 70)
	

	
	# Read option
	parser = argparse.ArgumentParser(prog='Bookmark')
	gArgs = parser.add_mutually_exclusive_group()
	gArgs.add_argument('-a', '--add', dest='Add', action='store_true', required=False,help='Element to add.')
	gArgs.add_argument('-d', '--del', dest='Delete', action='store_true', required=False,help='Element to delete.')
	gArgs.add_argument('-r', '--reset', dest='Reset', action='store_true', required=False,help='Reset all icon files.')
	#gArgs.add_argument('-l', '--list', dest='List', action='store_true', required=False,help='List elements.')

	parser.add_argument('-m', '--move', dest='Move', action='store_true', required=False,help='Move to right directory.')
	parser.add_argument('-g', '--generate', dest='Generate', action='store_true', required=False,help='Generate Html file.')
	parser.add_argument('-s', '--send', dest='Send', action='store_true', required=False,help='Copy html & image files on target.')

	parser.add_argument('-c', '--category', nargs=1, dest='Category', type=str, required=False, help='Category in Add/Delete option')
	parser.add_argument('-n', '--name', nargs=1, dest='Name', type=str, required=False, help='Item name in Add/Delete option')
	parser.add_argument('-l', '--link', nargs=1, dest='Link', type=str, required=False, help='Item link')
	parser.add_argument('-i', '--icon', nargs=1, dest='Icon', type=str, required=False, help='Item specific icon')

	# Evaluate option
	args, unknown = parser.parse_known_args()

	# Ask for json file to manage
	if args.Move or not os.path.exists('config.ini'):
		cfl.check('.ini')
	
	# Check for Params file and get them
	Contener = configparser.ConfigParser()	
	if not os.path.exists('config.ini'):
		print(script_name, '[E] No INI file')
		exit()
	Contener.read('config.ini')
	JsonFileName = Contener['Files']['JsonFileName']
	if not JsonFileName: JsonFileName='link.json'
	HtmlFileName = Contener['Files']['HtmlFileName']
	if not HtmlFileName: HtmlFileName='index.html'
	IconSize     = Contener['Pictures']['IconSize']
	if not IconSize: IconSize='128'
	IconDirectory = Contener['Pictures']['IconDirectory']
	if not IconDirectory: IconDirectory = './ico/'
	SpecificIconDirectory = Contener['Pictures']['SpecificIconDirectory']
	if not SpecificIconDirectory: SpecificIconDirectory = './img/'
	SaveDirectory = Contener['Pictures']['SaveDirectory']
	if not SaveDirectory: SaveDirectory = './sav/'
	if not os.path.exists(JsonFileName):
		print(script_name, '[E] No json file')
		exit()
	
	# set default language
	#DefaultLanguage = locale.getdefaultlocale()[0]
	#language_translations = gettext.translation("base", "./locales", languages=[DefaultLanguage])
	#language_translations.install()
	#_ = language_translations.gettext

	# Evaluate options
	if args.Category:
		Category = str(args.Category[0]).lower()
	else:
		Category = ''
	if args.Name:
		Name = str(args.Name[0]).lower()
	else:
		Name = ''
	if args.Link:
		Link = str(args.Link[0])
	else:
		Link = ''
	if args.Icon:
		Icon = str(args.Icon[0])
	else:
		Icon = ''

	# Evaluate actions
	# if args.List: List()
	bArgs = False
	if args.Add: Add(Category, Name, Link, Icon, JsonFileName, IconSize, IconDirectory, SpecificIconDirectory, SaveDirectory); bArgs = True
	if args.Delete: Delete(JsonFileName, IconDirectory, SaveDirectory); bArgs = True
	if args.Reset: Reset(JsonFileName, IconDirectory, IconSize); bArgs = True
	if args.Generate: Generate(JsonFileName, HtmlFileName, IconSize, IconDirectory, SpecificIconDirectory); bArgs = True
	if args.Send: Send(HtmlFileName, IconDirectory, SpecificIconDirectory); bArgs = True
	if bArgs: exit()
	inputRequest = script_name
	inputRequest += ' [R] Option to launch: '
	inputRequest +=  Fore.RED + '1' + Style.RESET_ALL + ' (Add) ' + Fore.RED + '2' + Style.RESET_ALL + ' (Delete) '
	inputRequest += Fore.RED + '3' + Style.RESET_ALL + ' (Generate) ' + Fore.RED + '4' + Style.RESET_ALL + ' (Send) '
	inputRequest += Fore.RED + '5' + Style.RESET_ALL + ' (Reset Icon files) ' + Fore.RED
	ArgValue = input(inputRequest)
	if ArgValue == '1': Add(Category, Name, Link, Icon, JsonFileName, IconSize, IconDirectory, SpecificIconDirectory, SaveDirectory)
	if ArgValue == '2': Delete(JsonFileName, IconDirectory, SaveDirectory)
	if ArgValue == '3': Generate(JsonFileName, HtmlFileName, IconSize, IconDirectory, SpecificIconDirectory)
	if ArgValue == '4': Send(HtmlFileName, IconDirectory, SpecificIconDirectory)
	if ArgValue == '5' : Reset(JsonFileName, IconDirectory, IconSize)
	exit()

def Reset(JsonFileName, IconDirectory, IconSize):
	font = ImageFont.truetype("Ubuntu-M.ttf", 28)
	with open(JsonFileName, 'r') as f:
		Links = json.load(f)
	f.close()
	for Item in Links:
		Name = Item['Name']
		Link = Item['Link']
		icoFile = IconDirectory
		icoFile += Name
		icoFile += '.png'
		try:
			os.remove(icoFile)
		except:
			print(script_name, '[I]', icoFile, 'not removed')
		paraSentence = 'https://www.google.com/s2/favicons?sz='
		paraSentence += str(IconSize)
		paraSentence += '&domain_url='
		paraSentence += Link
		try:
			FN=wget.download(url=paraSentence,out=icoFile)
			img = Image.open(icoFile)
		except:
			print('[I]', Link, ' not found')
			img = Image.new('RGB', (int(IconSize), int(IconSize)), color = 'red')
			draw = ImageDraw.Draw(img)
			draw.text((3, 23),Name,(0,0,0),font=font)
			img.save(icoFile)
	return()	

def Delete(JsonFileName,IconDirectory,SaveDirectory):
	# Source: https://pypi.org/project/tabulate/
	with open(JsonFileName, 'r') as f:
		Links = json.load(f)
	f.close()

	# print header
	print(script_name, '[I] List of items')
	# print list of items
#	print('{:<7} {:<10} {:<10}'.format('Index','Category','Name'))
	iLink = -1
	jLink = 0
	lLink=[]
	nLink = 4
	PrevCategory = ''
	Headers=nLink*['Index','Category','Name']
	for Item in Links:
		if iLink == -1:
			PrevCategory = Item['Category']
		if Item['Category'] != PrevCategory:
			if jLink != 0:
				lLink.append(tLink)
			PrevCategory = Item['Category']
			lLink.append(3*[])
			jLink = 0
		if jLink == 0:
			tLink=[]
		jLink += 1
		iLink += 1
		tLink.append(str(iLink))
		tLink.append(Item['Category'])
		tLink.append(Item['Name'])
		if jLink == nLink: 
			jLink = 0
			lLink.append(tLink)
	if jLink != 0:
		lLink.append(tLink)
	print(tabulate.tabulate(lLink, Headers,tablefmt='rounded_outline'))
	
	# Request item to delete
	inputRequest = script_name
	inputRequest += ' [R] item to delete: [Exit] '
	iDelete = input(inputRequest)
	if iDelete == '': exit()
	try:
		int(iDelete)
	except:
		print(script_name, '[E] your input is not an integer')
		exit()
	if (int(iDelete) < 0 or int(iDelete) > int(iLink)):
		print(script_name, '[E] your input is out of range')
		exit()
	print('[I]', Links[int(iDelete)])
	inputRequest = script_name
	inputRequest += '[R] Is it this item you want to delete ? (Y/[N])'
	iConfirm = input(inputRequest)
	yes = {'yes','y', 'YES', 'Y'}
	if iConfirm in yes:
		# Delete Icon File
		Name = Links[int(iDelete)]['Name']
		icoToDelete = IconDirectory
		icoToDelete += Name
		icoToDelete += '.png'
		try:
			os.remove(icoToDelete)
			print(script_name, '[I] Icon file ', icoToDelete, 'removed')
		except:
			print(script_name, '[I] No icon file to remove')
		
		# remove record from list 
		del Links[int(iDelete)]

		# save previous json file
		SavedFile = SaveDirectory + JsonFileName + datetime.datetime.now().strftime("%y%m%d%H%M%S")
		shutil.copy(JsonFileName, SavedFile)
		f = open(JsonFileName,'w')
		json.dump(Links, f, indent=4)
		f.close()

		# sort and save json file
		print(script_name, '[I] item deleted')
		Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
		f = open(JsonFileName,'w')
		json.dump(Links, f, indent=4)
		f.close()
	return()

def Add(Category,Name,Link,Icon,JsonFileName,IconSize,IconDirectory,SpecificIconDirectory,SaveDirectory):
	"""
	Source: https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/
	Source: https://stackoverflow.com/questions/24346872/python-equivalent-of-a-given-wget-command
	Source: https://www.pcastuces.com/pratique/astuces/6512.htm
	Source: https://fr.moonbooks.org/Articles/Comment-ajouter-du-texte-sur-une-image-avec-pillow-en-python-/
	Source: https://www.web-dev-qa-db-fra.com/fr/python/python-pillow-comment-mettre-lechelle-une-image/1046891181/
	Source; https://apprendrepython.com/comment-utiliser-pillow-pil-python-imaging-library/

	To create an empty picture
	>>> python3
	>>> from PIL import Image, ImageFont, ImageDraw
	>>> img = Image.new('RGB', (64, 64), color = 'red')
	>>> img.putalpha(0)
	>>> img.save('null.png')

	"""
	font = ImageFont.truetype("Ubuntu-M.ttf", 28)
	JsonVersion = str(datetime.datetime.now().time())
	with open(JsonFileName, 'r') as f:
		Links = json.load(f)
	f.close()

	# If no option value, request
	if not Category:
		lCategory = []
		iCategory = -1
		prevCategory = ''
		print(script_name, '[I] Known categories')
		for Item in Links:
			if Item['Category'] != prevCategory:
				iCategory += 1
				eCategory = []
				eCategory.append(str(iCategory))
				eCategory.append(Item['Category'])
				lCategory.append(eCategory)
				prevCategory = Item['Category']
		print(lCategory)
		print(tabulate.tabulate(lCategory, ['Index','Category'],tablefmt='rounded_outline'))
		inputRequest = script_name
		inputRequest += '[R] Item category; use index to select an existing category, full name for new category (Return = Exit) '
		Category = input(inputRequest).lower()
		# Test: if numeric, check range. If text, new category or existing one
		if not Category: exit()
		if Category.isdigit():
			if (int(Category) < 0 or int(Category)) > iCategory:
				print(script_name, '[E] your input is out of range')
				exit()
			Category = lCategory[int(Category)][1]

	if not Name:
		inputRequest = script_name
		inputRequest += '[R] Item name: (Return = Exit) '
		Name = input(inputRequest).lower()
		if not Name: exit()

	if not Link:
		inputRequest = script_name
		inputRequest += '[R] Item link: (Return = Exit) '
		Link = input(inputRequest)
		if not Link: exit()

	if not Icon and __name__ == '__main__':
		inputRequest = script_name
		inputRequest += '[R] Specific Icon: (Return = Favicon) '
		icoFile = input(inputRequest)		# If no Icon value, get favicon of web site. If not exist, create a new one with Name text
	else:
		icoFile = ''

	if not icoFile:
		icoFile = IconDirectory
		icoFile += Name
		icoFile += ".png"
		paraSentence = 'https://www.google.com/s2/favicons?sz='
		paraSentence += str(IconSize)
		paraSentence += '&domain_url='
		paraSentence += Link
		try:
			FN=wget.download(url=paraSentence,out=icoFile)
			img = Image.open(icoFile)
			'''
			if (img.size != 64):
				img=img.resize((64,64))
				img.save(icoFile)
			'''
		except:
			print(script_name, '[I]', Link, ' not found')
			img = Image.new('RGB', (int(IconSize), int(IconSize)), color = 'red')
			draw = ImageDraw.Draw(img)
			draw.text((3, 23),Name,(0,0,0),font=font)
			img.save(icoFile)
	else:
		Icon = icoFile

	# Save previous Json file
	SavedFile = SaveDirectory + JsonFileName + datetime.datetime.now().strftime("%y%m%d%H%M%S")
	shutil.copy(JsonFileName, SavedFile)

	# Add new record in Json file
	addRecord = {'Category': Category , 'Name': Name, 'Link': Link, 'Icon': Icon}
	Links.append(addRecord)
#	Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
	f = open(JsonFileName,'w')
	json.dump(Links, f, indent=4)
	f.close()
	return()

def Generate(JsonFileName, HtmlFileName, IconSize, IconDirectory, SpecificIconDirectory):
	"""
	Source: https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/
	Generate the Html file from Json file.
	"""
	filein = JsonFileName
	fileout = open(HtmlFileName, "w")
	with open(JsonFileName, 'r') as f:
		Links = json.load(f)
	Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
	maxColumn = 8
	nbColumn = 1
	previousCategory = ''
	# Colors are in css file; [l/i/j]Colors for loop on color list
	Colors = ['rose','gold','gris','marron','bleu','jaune','violet','vert','rouge','marine']
	lColors=len(Colors)
	iColors=-1
	iCategory = 0
	iLink = 0
	tabCategory = []
	iLinkPerCategory = 0

	# Count number of Categories, number of Links and Links per Category
	for Item in Links:
		iLink += 1
		Category = Item['Category']
		if (Category != previousCategory):
			iCategory += 1
			if previousCategory != '':
				tabCategory += [previousCategory, iLinkPerCategory]
			iLinkPerCategory = 0
			previousCategory = Category
		iLinkPerCategory += 1

	tabCategory += [previousCategory, iLinkPerCategory]
	# Calculate number of lines/columns et a 16/9 screen format
	maxLines = round(math.sqrt(iLink/14*9)+0.5)
	print(script_name, '[î] ',iCategory,iLink, maxLines,tabCategory)
	previousCategory = ''
	iCategory = 0
	iLines = 1
	# write the Html header
	table = ''
	headerFile = open('header.html', 'r')
	records = headerFile.readlines()
	for record in records:
		table += record
	headerFile.close()
	
	# Javascript in Html - necessary because the number of icons (iLink) is variable
	table+= '<script type=\"text/javascript\">\n'
	table += 'ICONE=Math.round(Math.sqrt(screen.width * screen.height * 0.7 / '
	table += str(iLink)
	table += ') * 0.6)\n'
	table += 'document.write(\"<style>img { border: 0px solid black; margin-left: 0px; margin-right: 0px; width: \"+ICONE+\"px; height: \"+ICONE+\"px } </style>\")\n'
	table += '</script>\n'

	# Main table
	table += "<table  class=\"Coral\"><tr><td>\n"
	# Create the table's row data
	for Item in Links:
		Category = Item['Category']
		Name = Item['Name']
		Link = Item['Link']
		Icon = Item['Icon']
		if (Category != previousCategory):
			if previousCategory != '':
				# Fill empty cells until maxLines for previous Category
				while iLines < maxLines:
					table += "    </tr><tr><td><img src=\"null.png\"></td>"
					iLines += 1
				table += "  </td></table><td>\n"
				iLines = 1
			# Compute number of cells per line for this category
			iCells = tabCategory[iCategory+1]
			iCellsPerLine = int((iCells/maxLines)+0.99)
			iColors += 1
			jColors = iColors%lColors
			table += "  <table class=\""
			table += Colors[jColors]
			table += "\">\n"
			table += "    <tr align=\"center\">\n"
			table += "      <th colspan=\""
			table += str(iCellsPerLine)
			table += "\"><h2><center>"
			table += Category
			table += " </h2></center></th>\n"
			table += "    </tr><tr>\n"
			previousCategory = Category
			iCategory += 2
			iTd = 0
			nbColumn = 0
		if iTd == iCellsPerLine:
			table += "    </tr><tr>\n"
			iLines += 1
			iTd = 1
		else:
			iTd +=1
		table += "        <td><a data-title=\""
		table += Name
		table += "\" href=\""
		table += Link
		table += "\" target=\"_blank\"><img src=\""
		if Icon == '':
			table += IconDirectory
			table += Name
			table += ".png\" ></a> </td>\n"
		else:
			table += SpecificIconDirectory
			table += Icon
			table += "\"></a> </td>\n"
	# close the last category
	while iLines < maxLines:
		table += "    </tr><tr><td><img src=\"null.png\"></td>"
		iLines += 1
	table += "  </tr>\n"
	table += "</td></tr></table>"

	fileout.writelines(table)
	fileout.close()
	f.close()
	return()

def Send(HtmlFileName, IconDirectory, SpecificIconDirectory):
	"""
	General purpose: 
		Generate files list to transfer
	ftp parameters are in a crypted file named .ftp.
		Exemple of file generating: python3 Crypt.py .ftp '{ "Host": "giveYourOwn", "Port": "giveYourOwn", "ftpUsername": "giveYourOwn", "ftpPassword": "giveYourOwn" }'
	"""
	ftpParameters = CryptMac.Uncrypt('.ftp')
	dictParameters = json.loads(ftpParameters)
	ftpHost = dictParameters['Host']
	ftpPort = dictParameters['Port']
	ftpUsername = dictParameters['Username']
	ftpPassword = dictParameters['Password']
	ftp=FTP(ftpHost,ftpUsername,ftpPassword)
	ftp.cwd('b')
	f=open(HtmlFileName, 'rb')
	ftp.storbinary('STOR ' + HtmlFileName, f)
	f.close()
	ftp.cwd(IconDirectory)
	listFilesToTransfer = list()
	listFiles = os.listdir(IconDirectory)
	refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
	for File in listFiles:
		fileDate = os.path.getctime(os.path.join(IconDirectory+File))
		if fileDate >= refDate:
			listFilesToTransfer.append(IconDirectory+File)
			print('Fichier: ',File,' plus récent')
			f=open(IconDirectory + File, 'rb')
			ftp.storbinary('STOR ' + File, f)
			f.close()
	ftp.cwd('..')
	ftp.cwd(SpecificIconDirectory)
	listFilesToTransfer = list()
	listFiles = os.listdir(SpecificIconDirectory)
	refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
	for File in listFiles:
		fileDate = os.path.getctime(os.path.join(SpecificIconDirectory+File))
		if fileDate >= refDate:
			listFilesToTransfer.append(SpecificIconDirectory+File)
			print('Fichier: ',File,' plus récent')
			f=open(SpecificIconDirectory + File, 'rb')
			ftp.storbinary('STOR ' + File, f)
			f.close()
	print(listFilesToTransfer)
	listFilesToTransfer = list()
	listFiles = os.listdir(SpecificIconDirectory)
	refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
	for File in listFiles:
		fileDate = os.path.getctime(os.path.join(SpecificIconDirectory+File))
		if fileDate >= refDate:
			listFilesToTransfer.append(SpecificIconDirectory+File)
			print(script_name, '[I] Fichier: ',File,' plus récent')
			f=open(SpecificIconDirectory+File, 'rb')
			ftp.storbinary('STOR ' + File, f)
			f.close()
	print('Bookmarks  [I] ',listFilesToTransfer)
	ftp.quit()
	os.remove('LastUpdateDate.txt')
	with open('LastUpdateDate.txt', "w") as f:
		f.write('')
	f.close()
	return()

if __name__ == '__main__':
	start()