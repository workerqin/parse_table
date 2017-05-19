#!/usr/bin/env python

import os
import sys
import re

def get_files(path):
    file_set = ['.c', '.h']
    for root, dirs, files in os.walk(path):
        for filename in files:
            if os.path.splitext(filename)[-1] in file_set:
                yield os.path.join(root, filename)

def parse(content):
    prefix = 'MDL_'
    single_quote = "'"
    double_quote = '"'
    pat = re.compile(r'Import\([\'|"].*?[\'|"]\)', re.MULTILINE)
    partion = lambda x, y: x.split(y)[1]
    for group in pat.findall(content):
        if double_quote in group:
            module_name = prefix + partion(group, double_quote)
        else:
            raise SyntaxError('can not found double quote in pattern: %r' % group)
        content = content.replace(group, module_name)
    return content

def main():
    if len(sys.argv) < 2:
        print '%s dirpath' % sys.argv[0]
        sys.exit(1)
    path = sys.argv[1]
    for fp in get_files(path):
        print 'parse file %s' % fp
        fb = open(fp) 
        #print parse(fb.read())
        content = parse(fb.read())
        fb = open(fp, 'wb')
        fb.write(content)
       
def test():
    '''
    >>> content = 'Import("xxxxx")'
    >>> parse(content)
    'MDL_xxxxx'
    >>> content = """Import("xxxxx") line1 line2 Import('singlequote')"""
    >>> parse(content)
    'MDL_xxxxx line1 line2 MDL_singlequote
    '''
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()
