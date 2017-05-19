# -*- coding: utf-8 -*-
import os
import sys
import shutil
import re

filePattern = re.compile(".+?_(.+).fani")

def usage():
    print 'python clearup.py [path]'
    
def doClearup(path):
    files = os.listdir(path)
    for f in files:
        if os.path.isdir(f):
            continue
        result = filePattern.match(f)
        if result:
            destPath = os.path.join(path,result.group(1))
            filePath = os.path.join(path,f)
            if os.path.exists(destPath):
                shutil.move(filePath, destPath)
            else:
                os.makedirs(destPath)
                shutil.move(filePath, destPath)
            print "Moved file(%s) to %s" % (filePath,destPath)

def clearup(path):
    if not os.path.exists(path) or os.path.isfile(path):
        return
    
    files = os.listdir(path)
    for f in files:
        if not re.match("^\d+$", f):
            continue
        #print "file(%s) match" % f
        
        workPath = os.path.join(path,f,"ani")
        #print "workPath(%s) match" % workPath
        if not os.path.exists(workPath) or os.path.isfile(workPath):
            continue
        
        doClearup(workPath)
    
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage();
    else:
        clearup(sys.argv[1])
