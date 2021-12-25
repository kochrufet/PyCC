def ReadBinary(file):
	response = None

	with open(file,"rb") as f:
		response = f.read()

	return response

def Hexify(binaryData):
	response = []
	for _byte in binaryData:
		_hexvalue = hex(_byte)[2:]
		if len(_hexvalue) < 2:
			_hexvalue = '0' + _hexvalue
		response.append(_hexvalue)

	return response

def ConvertToPythonComment(data,col = 32):
	_str_ = ""
	for i in range(0, len(data)):
		if not i%col:
			if i:
				_str_ += '\n'

			_str_ += '#'

		_str_ += data[i]

	return _str_

q = Hexify(ReadBinary("typesofhackers.jpg"))
res = "#push\n#jpg\n" + ConvertToPythonComment(q,48) + "\n#end"

with open("typesofhackerimage.py", "w") as f:
	f.write(res)







################################################################
import sys

if sys.byteorder == "little":
	OS_ORDER = "little"
else:
	OS_ORDER = "big"

def ExtractFilesFromPyComment(pyfile):
	with open(file,"r") as f:
		code = f.read()
		
	i = code.find("#push\n") + 7
	if i == -1+7:
		return None
	e = code.rfind("\n#end")
	if e == -1:
		raise "END of file is not specified!"
	package = code[i:e].split("\n#end\n")

	fileextentions = package[0].split()
	j = -1
	for metadata in package[1:]:
		print(1)
		j += 1
		data = metadata.split('\n')
		container = b""
		for parsing in data:
			for i in range(1,len(parsing),2):
				_byte = int(parsing[i:i+2], 16).to_bytes(1, OS_ORDER)
				container += _byte

		with open(fileextentions[j], "wb") as out:
			out.write(container)
