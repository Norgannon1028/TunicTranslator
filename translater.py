import argparse 
from encoder import *
from painter import *

if __name__=="__main__":
    parser = argparse.ArgumentParser() 

    parser.add_argument('-i',"--input", help='read the input from <file>, where input should be English in plain text',default='input.txt',metavar='<file>')
    parser.add_argument('-o',"--output", help='place the output into <file>, where ouput should be either jpg or png',default='output.jpg',metavar='<file>')

    parser.add_argument('-l',"--line", help='set the number of lines in the canvas, affect the canvas height',type=int,default=8,metavar='<int>')
    parser.add_argument('-c',"--char", help='set the number of characters per line, affect the canvas width',type=int,default=25,metavar='<int>')

    args = parser.parse_args()

    fileObject = open(args.input, 'r')
    fileLines = fileObject.readlines()
    rune_list=[]
    for line in fileLines:
        rune_list.extend(translate_string(line))
    
    fox=Fox(args.line,args.char)
    fox.draw(rune_list)
    fox.save(args.output)
    
    print("Successfully generated Runes!")
