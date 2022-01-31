
class PythonCommentCipherByKoch:
	"""
		Description about my project
		
		Forward:
			fbin -> fhex -> fwrap -> fpycomment -> RESULT AS Python Comment
		
		Backward:
			fupackcomment -> fuwrap -> fuhex -> fubin -> .decode() -> RAW Data an object ( file,... )

		Method:
			convert( string )

			Converts given string to python comment package data

			RETURN value : a string

		Method:
			convertFromFile( filename )

			Reads data of the file and converts it to python comment package data

			RETURN value : a string

		Method:
			convertFromFileAndSaveAs( filename, pyfilename )

			Converts given file to python comment package file

			[ pyfilename ] is name of new python script where data will save

			RETURN value : a succes message

		Method:
			extract( string )

			Extracts object from given string which is python comment package

			If package data is STRING, return value will be a string
			else, method will save package as file and return succes message

			RETURN value : a string or a succes message

		Method:
			extractFromPythonFile( pyfilename )

			Extracts package from given pyfile

			RETURN value : same as extract method

	"""
	
	# Unique key by Koch
	# You can change this carefully !
	# This keys must be UNIQUE !
	# !!! You must not use this strings in other comment places !!!
	# UNIQUE Keys block 2 string below
	
	UNIQUE_KEY_1 = "package"
	UNIQUE_KEY_2 = "end"

	
	# For encoding in binary
	from sys import byteorder
	from os import path
	
	# Don't call this methods other places !
	# Actually you don't need this methods !
	# This methods are only for 5 main useful methods:
	#
	# 	> convert()
	#	> convertFromFile()
	#	> convertFromFileAndSaveAs()
	#
	#	> extract()
	#	> extractFromPythonFile()
	#
	#

	def fbin(self, x):
		return x.encode()

	def fhex(self, x):
		res = ""
		for char in x:
			res += hex(char)[2:].zfill(2)
		return res

	def fwrap(self, x, w = 30):
		res = ""
		for i in range(len(x)):
			if i and i%w == 0:
				res += '\n'
			res += x[i]
		return res

	def fpycomment(self, x, filename):
		return "\"\"\"\n" + self.UNIQUE_KEY_1 + '\n' + filename + '\n' + x + '\n' + self.UNIQUE_KEY_2 + "\n\"\"\""

	def fupackcomment(self, x):
		if self.UNIQUE_KEY_1 in x:
			_1 = x.find( self.UNIQUE_KEY_1 ) + len( self.UNIQUE_KEY_1 ) + 1
		else:
			raise "[Error] :: Unique :: Package damaged !"
		if self.UNIQUE_KEY_2 in x[_1:]:
			_2 = x.find( self.UNIQUE_KEY_2 )
		else:
			raise "[Error] :: Unique :: Package damaged !"
		
		return x[_1:_2]

	def fuwrap(self, x):
		data = x.splitlines()
		filename = data[0]
		container = "".join( data[1:] )
		return filename, container

	def fuhex(self, x):
		return [ int( x[i:i + 2], 16) for i in range(0, len(x), 2) ]

	def fubin(self, x):
		return b"".join( [ c.to_bytes(1, self.byteorder) for c in x ] )
	
	
	
	def convert(self, x, _mode = "STRING" ):
		# fbin -> fhex -> fwrap -> fpycomment -> RESULT AS Python Comment
		
		if _mode == "STRING":
			x = self.fbin( x )

		x = self.fhex(x)
		x = self.fwrap(x)
		x = self.fpycomment(x, _mode)

		return x
	
	def convertFromFile(self, filefullname):
		__, filename = self.path.split(filefullname)
		
		with open(filefullname, 'rb') as f:
			container = f.read()
		
		return self.convert( container, filename )

	def convertFromFileAndSaveAs(self, filefullname, pyfilename):
		container = self.convertFromFile(filefullname)

		with open(pyfilename, 'w') as f:
			f.write(container)

		return "[INFO] : " + pyfilename + " saved."
	
	def extract(self, x):
		# fupackcomment -> fuwrap -> fuhex -> fubin -> .decode() -> RAW Data an object ( file,... )
		x = self.fupackcomment(x)
		filename, x = self.fuwrap(x)
		x = self.fuhex(x)
		x = self.fubin(x)
		if filename == "STRING":
			return x.decode()
		else:
			with open(filename, 'wb') as f:
				f.write(x)

			return "[INFO] : ", filename, "saved."

	def extractFromPythonFile(self, x):
		with open(x, 'r') as f:
			container = f.read()

		return self.extract(container)

# end of koch codes