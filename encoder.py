from enum import Enum
import epitran

vowel_symbol=["i","ɪ","ɛ","æ","u","ʊ","ʌ","ə","ɹ̩","ɔ","ɑ","e","a","o"]
consonant_symbol=["p","b","t","d","k","ɡ","m","n","ŋ","w","j","l","f","v","θ","ð","s","z","ʃ","ʒ","ɹ","h","ʧ","ʤ"]

epi=epitran.Epitran("eng-Latn",ligatures=True)

class Vowel(Enum):
    i  = 0b111110
    ɪ  = 0b110000
    ɛ  = 0b111100
    æ  = 0b001111
    u  = 0b011111
    ʊ  = 0b011100
    ʌ  = 0b000011
    ə  = 0b000011
    ɹ̩  = 0b111101
    ɔ  = 0b001110
    ɑ  = 0b110011
    ej = 0b000010
    aj = 0b000001
    oj = 0b010000
    aw = 0b100000
    ow = 0b111111
    ɪɹ = 0b101110
    ɛɹ = 0b101100
    ɔɹ = 0b101111

class Consonant(Enum):
    p  = 0b1010001000000
    b  = 0b1100010000000
    t  = 0b1010101000000
    d  = 0b1101010000000
    k  = 0b1100011000000
    ɡ  = 0b1110001000000
    m  = 0b0101000000000
    n  = 0b0101100000000
    ŋ  = 0b1111111000000
    w  = 0b0000101000000
    j  = 0b1010110000000
    l  = 0b1010010000000
    f  = 0b1011001000000
    v  = 0b1100110000000
    θ  = 0b1010111000000
    ð  = 0b1111010000000
    s  = 0b1011011000000
    z  = 0b1110110000000
    ʃ  = 0b1111101000000
    ʒ  = 0b1101111000000
    ɹ  = 0b1010011000000
    h  = 0b1110010000000
    ʧ  = 0b1010100000000
    ʤ  = 0b1001010000000

def preprocess(phonetic_list):
    length=len(phonetic_list)
    ret_list=[]
    idx=0
    while True:
        if idx >= length:
            break
        if phonetic_list[idx] in consonant_symbol:
            ret_list.append(Consonant[phonetic_list[idx]])
        elif phonetic_list[idx] in vowel_symbol:
            if phonetic_list[idx] == "e":
                if (idx+1)<length and phonetic_list[idx+1] == "j":
                    ret_list.append(Vowel["ej"])
                    idx+=1
                else:
                    raise Exception(phonetic_list[idx]+" is not standard English phonetic symbol")
            elif phonetic_list[idx] == "a": 
                if (idx+1)<length and phonetic_list[idx+1] == "j":
                    ret_list.append(Vowel["aj"])
                    idx+=1
                elif (idx+1)<length and phonetic_list[idx+1] == "w":
                    ret_list.append(Vowel["aw"])
                    idx+=1
                else:
                    raise Exception(phonetic_list[idx]+" is not standard English phonetic symbol")
            elif phonetic_list[idx] == "o": 
                if (idx+1)<length and phonetic_list[idx+1] == "j":
                    ret_list.append(Vowel["oj"])
                    idx+=1
                elif (idx+1)<length and phonetic_list[idx+1] == "w":
                    ret_list.append(Vowel["ow"])
                    idx+=1
                else:
                    raise Exception(phonetic_list[idx]+" is not standard English phonetic symbol")
            elif phonetic_list[idx] == "ɪ": 
                if (idx+1)<length and phonetic_list[idx+1] == "ɹ":
                    ret_list.append(Vowel["ɪɹ"])
                    idx+=1
                else:
                    ret_list.append(Vowel["ɪ"])
            elif phonetic_list[idx] == "ɛ": 
                if (idx+1)<length and phonetic_list[idx+1] == "ɹ":
                    ret_list.append(Vowel["ɛɹ"])
                    idx+=1
                else:
                    ret_list.append(Vowel["ɛ"])
            elif phonetic_list[idx] == "ɔ": 
                if (idx+1)<length and phonetic_list[idx+1] == "ɹ":
                    ret_list.append(Vowel["ɔɹ"])
                    idx+=1
                else:
                    ret_list.append(Vowel["ɔ"])
            else:
                ret_list.append(Vowel[phonetic_list[idx]])
        else:
            raise Exception(phonetic_list[idx]+" is not standard English phonetic symbol")
        idx+=1
    return ret_list

def encode(token_list):
    length=len(token_list)
    ret_list=[]
    idx=0
    while True:
        if idx >= length:
            break
        if (idx+1) == length:
            ret_list.append(token_list[idx].value)
            break
        if isinstance(token_list[idx],Consonant):
            if isinstance(token_list[idx+1],Consonant):
                ret_list.append(token_list[idx].value)
                idx+=1
                continue
            else:
                ret_list.append(token_list[idx].value | token_list[idx+1].value)
                idx+=2
                continue
        elif isinstance(token_list[idx],Vowel):
            if isinstance(token_list[idx+1],Vowel):
                ret_list.append(token_list[idx].value)
                idx+=1
                continue
            else:
                ret_list.append(token_list[idx].value | token_list[idx+1].value | 0b10000000000000)
                idx+=2
                continue
    return ret_list
        
def translate_word(str):
    phonetic_list=epi.trans_list(str)
    #print(phonetic_list)
    token_list=preprocess(phonetic_list)
    #print(token_list)
    code_list=encode(token_list)
    return code_list

def translate_string(line):
    line=line.replace('，',',').replace(',',' , ')
    line=line.replace('。','.').replace('.',' . ')
    line=line.replace('？','?').replace('?',' ? ')
    line=line.replace('！','!').replace('!',' ! ')
    str_list = line.split()
    ret_list=[]
    for item in str_list:
        if item.isalpha():
            ret_list.append(translate_word(item)) #word_code
            ret_list.append(-1) #space
        elif item == ',':
            if len(ret_list)!=0 and ret_list[-1] == -1:
                ret_list.pop()
            ret_list.append(-2) #comma
        elif item == '.':
            if len(ret_list)!=0 and ret_list[-1] == -1:
                ret_list.pop()
            ret_list.append(-3) #full stop
        elif item == '!':
            if len(ret_list)!=0 and ret_list[-1] == -1:
                ret_list.pop()
            ret_list.append(-4) #exclamation mark
        elif item == '?':
            if len(ret_list)!=0 and ret_list[-1] == -1:
                ret_list.pop()
            ret_list.append(-5) #question mark
        else:
            raise Exception(item + " is not supported yet")
    if len(ret_list)!=0 and ret_list[-1] == -1:
        ret_list.pop()
    ret_list.append(-10) #\n
    
    return ret_list

