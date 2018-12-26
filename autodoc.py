import re
from sys import argv
import os
from os import rename as mv

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def autodoc(filename):
    with open(filename) as f:
        lines = f.readlines()
    lidx = 0
    for lidx in range(len(lines)):
        line = lines[lidx]
        if re.match('[_a-zA-Z].*\(.*\) *;.*', line) is not None: # matches anything not indented that has a letter, parens, then a semicolon, then other stuff at the end
            docparts = []
            line = line.strip()
            print '\n\n' + line + '\n'
            desc = raw_input('Description of this function:\n')
            if desc.strip() == '': # skip if no input given
                continue
            docparts.append(desc)
            docparts.append('') # will add a newline
            
            # now iterate through args and get descriptions
            argstart = line.find('(')+1
            argend = line.find(')')
            args = line[argstart:argend].split(',')
            for arg in args:
                if arg == '':
                    continue
                argdesc = raw_input('\nDescription of argument "%s":\n' % (arg))

                # the name will be the last word in arg, so find the last word
                argparts = arg.split(' ')
                i = -1
                while argparts[i] == '': # handle spaces before commas
                    i -= 1
                arglast = argparts[i]

                # if we have other symbols in front/behind the name, such as *s for pointers or [] for an array, we want to strip those, so find the actual name
                match = re.search('[_a-zA-Z][_a-zA-Z0-9]*', arglast)
                if match is not None:
                    argname = arglast[slice(*match.span())]
                else:
                    argname = raw_input('\nCould not determine function name. Enter function name: ').strip()
                docparts.append('@param %s %s' % (argname, argdesc))
                
            retdesc = raw_input('\nDescription of return value:\n')
            if retdesc.strip() != '':
                docparts.append('') # newline again to separate
                docparts.append('@returns ' + retdesc.strip())

            # now just build the actual doc comment from all the parts
            comment = '\n/**\n'
            for part in docparts:
                comment += starAndCap(part)
            comment += ' */\n'
            # change the original line to contain the comment
            lines[lidx] = comment + lines[lidx]            
    return ''.join(lines)

def starAndCap(st):
    ''' this function adds the * to the beginning of each line and also ensures 
    no line of the doc comment is >80 words by breaking up large lines.
    idea: read from string into new buf word by word until len of new buf
    >= 77, then add buf into new string with a newline and star attached'''
    buf = ''
    newst = ''
    words = st.split(' ')
    for word in words:
        if len(buf) + len(word) >= 77: # overrunning line
            newst += ' * ' + buf.strip() + '\n' # kill hanging space and push full buffer to the new string
            buf = ''
        while len(word) >= 77: # if we have a super long word, split it up
            newst += ' * ' + word[:77] + '\n'
            word = word[77:]
        buf += word + ' '
        
    # add remainder of buf
    newst += ' * ' + buf.strip() + '\n'
    return newst

if __name__ == '__main__':
    for arg in argv[1:]:
        mv(arg, arg+'.bak') # keep a backup just in case
        with open(arg, 'w') as f:
            cls()
            print 'FILE', arg, '\n\n\n\n'
            f.write(autodoc(arg+'.bak'))
                
