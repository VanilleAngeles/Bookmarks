#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Source:
FTP: https://www.thepythoncode.com/article/download-and-upload-files-in-ftp-server-using-python
Loop on files: https://gayerie.dev/docs/python/python3/fichier.html#actions-sur-les-fichiers-et-les-repertoires
File charactéristics: https://waytolearnx.com/2019/04/comment-recuperer-la-date-de-creation-modification-dun-fichier-en-python.html
File characteristics Integer: https://askcodez.com/comment-comparer-la-date-de-modification-de-deux-fichiers-en-python.html
"""
try:
	import argparse,sys,time,os,datetime,json,shutil,math,CryptMac,wget,ftplib,PIL
	from ftplib import FTP
	from PIL import Image, ImageFont, ImageDraw
except:
	print('[E] arror in import statement')
	exit()

def start():
	script_version = "0.1"
	python_version = sys.version.split(' ')[0]
	
	print("-" * 70)
	print('[I] Signets (SCRIPT V{:s} - PYTHON V{:s}) - {:s}'.format(script_version, python_version,time.strftime('%I:%M:%S %p')))
	print("-" * 70)

	parser = argparse.ArgumentParser(prog='JSON')
	gArgs = parser.add_mutually_exclusive_group()
	gArgs.add_argument('-a', '--add', dest='Add', action='store_true', required=False,help="Element to add.")
	gArgs.add_argument('-d', '--del', dest='Delete', action='store_true', required=False,help="Element to delete.")
	gArgs.add_argument('-l', '--list', dest='List', action='store_true', required=False,help="List elements.")
	gArgs.add_argument('-g', '--generate', dest='Generate', action='store_true', required=False,help="Generate Html file.")
	gArgs.add_argument('-f', '--ftp', dest='Ftp', action='store_true', required=False,help="Copy html & image files on target via Ftp.")

	args, unknown = parser.parse_known_args()
	if args.List: List()
	if args.Add: Add()
	if args.Delete: Delete()
	if args.Generate: Generate()
	if args.Ftp: Ftp()

def List():
	filein = 'link.json'
	with open(filein, 'r') as f:
		Links = json.load(f)
	f.close()
	iLink = -1
	for Item in Links:
		Category = Item['Category']
		Name = Item['Name']
		Link = Item['Link']
		iLink += 1
		print('[I] Index ', iLink, ' Category ', Category,' Name ', Name)
	exit()

def Delete():
	filein = 'link.json'
	with open(filein, 'r') as f:
		Links = json.load(f)
	f.close()
	iLink = -1
	for Item in Links:
		Category = Item['Category']
		Name = Item['Name']
		Link = Item['Link']
		iLink += 1
		print('Index ', iLink, ' Category ', Category,' Name ', Name)
	iDelete = input('[R] item to delete: ')
	try:
		int(iDelete)
	except:
		print('[E] your input is not an integer')
		exit()
	if (int(iDelete) < 0 or int(iDelete) > int(iLink)):
		print('[E] your input is out of range')
		exit()
	print('[I]', Links[int(iDelete)])
	iConfirm = input('[R] Is it this item you want to delete ? (Y/[N])')
	yes = {'yes','y', 'YES', 'Y'}
	if iConfirm in yes:
		del Links[int(iDelete)]
		SavedFile = './sav/' + filein + datetime.datetime.now().strftime("%y%m%d%H%M%S")
		shutil.copy(filein, SavedFile)
		f = open(filein,'w')
		json.dump(Links, f, indent=4)
		f.close()
		print('[I] item deleted')
		Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
		f = open(filein,'w')
		json.dump(Links, f, indent=4)
		f.close()
	exit()

def Add():
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
	font = ImageFont.truetype("Ubuntu-M.ttf", 18)
	filein = 'link.json'
	JsonVersion = str(datetime.datetime.now().time())
	with open(filein, 'r') as f:
		Links = json.load(f)
	f.close()
	prevCategory = ''
	for Item in Links:
		if Item['Category'] != prevCategory:
			prevCategory = Item['Category']
			print('[I] Known category: ', Item['Category'])
	Category = input('[R] Item category: (Return = Exit) ')
	if not Category: exit()
	Name = input('[R] Item name: (Return = Exit) ')
	if not Name: exit()
	Link = input('[R] Item link: (Return = Exit) ')
	if not Link: exit()
	Icon = input('[R] Icon file name: (Return = Favicon will be uploaded)')
	SavedFile = './sav/' + filein + datetime.datetime.now().strftime("%y%m%d%H%M%S")
	shutil.copy(filein, SavedFile)

	if not Icon:
		a=b=c=0
		for i in Link:
			if i == '/':
				c+=1
				if c == 3:
					b=a
			a+=1
		if b == 0:
			b = a
		urlName = Name
		urlRoot = Link[0:b]
		paraSentence="https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url="
		paraSentence += urlRoot
		paraSentence += "&size=64"
		icoFile = "./ico/"
		urlName = urlName.replace(" ","")
		urlName = urlName.replace("/","")
		icoFile += urlName
		icoFile += ".png"
		try:
			FN=wget.download(url=paraSentence,out=icoFile)
			img = Image.open(icoFile)
			if (img.size != 64):
				img=img.resize((64,64))
				img.save(icoFile)
		except:
			print(urlName, ' not found')
			img = Image.new('RGB', (64, 64), color = 'red')
			draw = ImageDraw.Draw(img)
			draw.text((3, 23),urlName,(0,0,0),font=font)
			img.save(icoFile)
	addRecord = {'Category': Category , 'Name': Name, 'Link': Link, 'Icon': Icon}
	Links.append(addRecord)
	Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
	f = open(filein,'w')
	json.dump(Links, f, indent=4)
	f.close()
	exit()

def Generate():
	"""
	Source: https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/
	Generate the Html file from Json file. In a future relaese, this file nals will be required
	"""
	filein = 'link.json'
	fileout = open("link.html", "w")
	with open(filein, 'r') as f:
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
	maxLines = round(math.sqrt(iLink/16*9)+0.5)
	print(iCategory,iLink, maxLines,tabCategory)
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
					table += "    </tr><tr><td><img src=\"./img/null.png\"></td>"
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
			table += "./ico/"
			table += Name
			table += ".png\"></a> </td>\n"
		else:
			table += "./img/"
			table += Icon
			table += "\"></a> </td>\n"
	# close the last category
	while iLines < maxLines:
		table += "    </tr><tr><td><img src=\"./img/null.png\"></td>"
		iLines += 1
	table += "  </tr>\n"
	table += "</td></tr></table>"

	fileout.writelines(table)
	fileout.close()
	f.close()
	exit()

def Ftp():
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
	f=open('link.html', 'rb')
	ftp.storbinary('STOR index.html', f)
	f.close()
	ftp.cwd('./ico')
	listFilesToTransfer = list()
	listFiles = os.listdir('./ico')
	refDate = os.path.getctime(os.path.join('./ico/LastUpdateDate.txt'))
	for File in listFiles:
		fileDate = os.path.getctime(os.path.join('./ico/'+File))
		if fileDate >= refDate:
			listFilesToTransfer.append('./ico/'+File)
			print('Fichier: ',File,' plus récent')
			f=open('./ico/'+File, 'rb')
			ftp.storbinary('STOR '+File, f)
			f.close()
	print(listFilesToTransfer)
	listFilesToTransfer = list()
	listFiles = os.listdir('./img')
	refDate = os.path.getctime(os.path.join('./ico/LastUpdateDate.txt'))
	for File in listFiles:
		fileDate = os.path.getctime(os.path.join('./img/'+File))
		if fileDate >= refDate:
			listFilesToTransfer.append('./img/'+File)
			print('Fichier: ',File,' plus récent')
			f=open('./img/'+File, 'rb')
			ftp.storbinary('STOR '+File, f)
			f.close()
	print(listFilesToTransfer)
	ftp.quit()	


if __name__ == '__main__':
	start()