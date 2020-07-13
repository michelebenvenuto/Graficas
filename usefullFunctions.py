import struct

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def color(r,g,b):
	if (0>r>1 or 0>g>1 or 0>b>1):
		raise Exception("Color inputs must be values between 0 and 1")
	else: 
		r *= 255
		g *= 255
		b *= 255
		return bytes([b,g,r])