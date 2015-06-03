#!/usr/bin/env python

'''
    Copyright 2014 Simon Mouradian, Frank Milthaler
    This file is part of Colour Pagecount.

    Colour Pagecount is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Colour Pagecount is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Colour Pagecount.  If not, see <http://www.gnu.org/licenses/>.
'''

# Contributors
# Simon Mouradian (slmouradian)
# Frank Milthaler (fmilthaler)

import sys
import os

#add check for file tmp.dat, in order to avoid overwritting a file
def count_pages(arg1):
    command = 'gs -o - -sDEVICE=inkcov '+arg1+'>./tmp.dat'
    os.system(command)
    
    f = open('tmp.dat', 'r')
    
    cyan = []
    magenta = []
    yellow = []
    
    for line in f:
        if line.startswith(' '):
            cyan.append(float(line.strip().split(' ')[0]))
            magenta.append(float(line.strip().split(' ')[2]))
            yellow.append(float(line.strip().split(' ')[4]))

    f.close()

    colour_pages = 0
    for i in range(len(cyan[:])):
        if (cyan[i] > 0.0) or (magenta[i] > 0.0) or (yellow[i] > 0.0):
            colour_pages += 1
    os.system('rm ./tmp.dat')
    return colour_pages

def print_pages(filename, colour_pages):
    if (colour_pages > 1 or colour_pages == 0):
        be = 'are'
        page = 'pages'
    else:
        be = 'is'
        page = 'page'
    formatted_print = 'There '+be+' '+str(colour_pages)+' colour '+page+' in "'+filename+'".'
    return formatted_print

def bad_version():
    gs_version = float(os.popen('gs --version').read())
    if gs_version < 9.05:
        return True
    else:
        return False

if __name__=='__main__':

    if bad_version():
        print 'Wrong gs version.'
        print 'Need version > 9.05'
        sys.exit(1)

    arg1 = str(sys.argv[1])

    colour_pages = count_pages(arg1)
    print print_pages(arg1, colour_pages)
