#-*- coding:utf-8 -*-

import sys
from xml.sax import ContentHandler
from xml.sax import make_parser

reload(sys)
sys.setdefaultencoding('utf8')

USAGE = "python main.py path xml_file output_file"

INSTURCTION = u'''
//------------------------------------------------------------
//此文件导表生成，无需手动添加
//------------------------------------------------------------\n
'''

ifndef = u"#ifndef __REASON__\n"
define = u"#define __REASON__\n"
endif = u"#endif\n"


def write_file(reason_info, desc, output_file):
	try:
		with open(output_file, "w+b") as fd:
			fd.write(INSTURCTION.encode("utf-8"))
			fd.write(ifndef + define + "\n" + "static mapping TLogReason = {" + "\n")
			data = []
			for info in sorted(reason_info.items(), key = lambda item: item[1]):
				line = '''"%s":%d,'''%(info[0], info[1]) + "\t" + "//" + desc[info[1]]
				data.append(line)
			fd.write("\n".join(data) + "\n" + "}" + "\n")
			fd.write(endif)
	except:
		print "cant open file :%s" % output_file
		raise 
	pass	

class TlogHandler(ContentHandler):
	def __init__(self):
		self.reason_flag = False
		self.reason_info = {}
		self.desc = {}
		pass	

	def startElement(self, name, attrs):
		if name == "macrosgroup" and attrs.has_key("name") and attrs["name"] == "Reason":
			self.reason_flag = True
		if name == "macro" and self.reason_flag is True:
			reason = attrs["name"]
			value = attrs["value"]
			self.reason_info[reason] = int(value)
			self.desc[int(value)] = attrs["desc"]
		pass

	def character(self, data):
		pass

	def endElement(self, name):
		if name == "macrosgroup":
			self.reason_flag = False 
		pass

def handler_xml(xml_file, output_file):
	parser = make_parser()
	handler = TlogHandler()
	parser.setContentHandler(handler)
	parser.parse(xml_file)

	#print len(handler.reason_info)
	
	write_file(handler.reason_info, handler.desc, output_file)
	pass

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print USAGE
		exit(1)
	
	path, xml_file, output_file = sys.argv[1:]
	handler_xml(xml_file, output_file)
