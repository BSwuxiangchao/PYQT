# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 14:04:49 2015

@author: iceyu
"""



_patterns = {
    0   :   'BaBbBb',    1   :   'BbBaBb',    2   :   'BbBbBa',
    3   :   'AbAbBc',    4   :   'AbAcBb',    5   :   'AcAbBb',
    6   :   'AbBbAc',    7   :   'AbBcAb',    8   :   'AcBbAb',
    9   :   'BbAbAc',    10  :   'BbAcAb',    11  :   'BcAbAb',
    12  :   'AaBbCb',    13  :   'AbBaCb',    14  :   'AbBbCa',
    15  :   'AaCbBb',    16  :   'AbCaBb',    17  :   'AbCbBa',
    18  :   'BbCbAa',    19  :   'BbAaCb',    20  :   'BbAbCa',
    21  :   'BaCbAb',    22  :   'BbCaAb',    23  :   'CaBaCa',
    24  :   'CaAbBb',    25  :   'CbAaBb',    26  :   'CbAbBa',
    27  :   'CaBbAb',    28  :   'CbBaAb',    29  :   'CbBbAa',
    30  :   'BaBaBc',    31  :   'BaBcBa',    32  :   'BcBaBa',
    33  :   'AaAcBc',    34  :   'AcAaBc',    35  :   'AcAcBa',
    36  :   'AaBcAc',    37  :   'AcBaAc',    38  :   'AcBcAa',
    39  :   'BaAcAc',    40  :   'BcAaAc',    41  :   'BcAcAa',
    42  :   'AaBaCc',    43  :   'AaBcCa',    44  :   'AcBaCa',
    45  :   'AaCaBc',    46  :   'AaCcBa',    47  :   'AcCaBa',
    48  :   'CaCaBa',    49  :   'BaAcCa',    50  :   'BcAaCa',
    51  :   'BaCaAc',    52  :   'BaCcAa',    53  :   'BaCaCa',
    54  :   'CaAaBc',    55  :   'CaAcBa',    56  :   'CcAaBa',
    57  :   'CaBaAc',    58  :   'CaBcAa',    59  :   'CcBaAa',
    60  :   'CaDaAa',    61  :   'BbAdAa',    62  :   'DcAaAa',
    63  :   'AaAbBd',    64  :   'AaAdBb',    65  :   'AbAaBd',
    66  :   'AbAdBa',    67  :   'AdAaBb',    68  :   'AdAbBa',
    69  :   'AaBbAd',    70  :   'AaBdAb',    71  :   'AbBaAd',
    72  :   'AbBdAa',    73  :   'AdBaAb',    74  :   'AdBbAa',
    75  :   'BdAbAa',    76  :   'BbAaAd',    77  :   'DaCaAa',
    78  :   'BdAaAb',    79  :   'AcDaAa',    80  :   'AaAbDb',
    81  :   'AbAaDb',    82  :   'AbAbDa',    83  :   'AaDbAb',
    84  :   'AbDaAb',    85  :   'AbDbAa',    86  :   'DaAbAb',
    87  :   'DbAaAb',    88  :   'DbAbAa',    89  :   'BaBaDa',
    90  :   'BaDaBa',    91  :   'DaBaBa',    92  :   'AaAaDc',
    93  :   'AaAcDa',    94  :   'AcAaDa',    95  :   'AaDaAc',
    96  :   'AaDcAa',    97  :   'DaAaAc',    98  :   'DaAcAa',
    99  :   'AaCaDa',    100 :   'AaDaCa',    101 :   'CaAaDa',
    102 :   'DaAaCa',    103 :   'BaAdAb',    104 :   'BaAbAd',
    105 :   'BaAbCb',    106 :   'BcCaAaB'
}

starta, startb, startc, stop = 103, 104, 105, 106

seta = {
        ' ' :   0,        '!' :   1,        '"' :   2,        '#' :   3,
        '$' :   4,        '%' :   5,        '&' :   6,       '\'' :   7,
        '(' :   8,        ')' :   9,        '*' :  10,        '+' :  11,
        ',' :  12,        '-' :  13,        '.' :  14,        '/' :  15,
        '0' :  16,        '1' :  17,        '2' :  18,        '3' :  19,
        '4' :  20,        '5' :  21,        '6' :  22,        '7' :  23,
        '8' :  24,        '9' :  25,        ':' :  26,        ';' :  27,
        '<' :  28,        '=' :  29,        '>' :  30,        '?' :  31,
        '@' :  32,        'A' :  33,        'B' :  34,        'C' :  35,
        'D' :  36,        'E' :  37,        'F' :  38,        'G' :  39,
        'H' :  40,        'I' :  41,        'J' :  42,        'K' :  43,
        'L' :  44,        'M' :  45,        'N' :  46,        'O' :  47,
        'P' :  48,        'Q' :  49,        'R' :  50,        'S' :  51,
        'T' :  52,        'U' :  53,        'V' :  54,        'W' :  55,
        'X' :  56,        'Y' :  57,        'Z' :  58,        '[' :  59,
       '\\' :  60,        ']' :  61,        '^' :  62,        '_' :  63,
     '\x00' :  64,     '\x01' :  65,     '\x02' :  66,     '\x03' :  67,
     '\x04' :  68,     '\x05' :  69,     '\x06' :  70,     '\x07' :  71,
     '\x08' :  72,     '\x09' :  73,     '\x0a' :  74,     '\x0b' :  75,
     '\x0c' :  76,     '\x0d' :  77,     '\x0e' :  78,     '\x0f' :  79,
     '\x10' :  80,     '\x11' :  81,     '\x12' :  82,     '\x13' :  83,
     '\x14' :  84,     '\x15' :  85,     '\x16' :  86,     '\x17' :  87,
     '\x18' :  88,     '\x19' :  89,     '\x1a' :  90,     '\x1b' :  91,
     '\x1c' :  92,     '\x1d' :  93,     '\x1e' :  94,     '\x1f' :  95,
     '\xf3' :  96,     '\xf2' :  97,    'SHIFT' :  98,     'TO_C' :  99,
     'TO_B' : 100,     '\xf4' : 101,     '\xf1' : 102
}

setb = {
        ' ' :   0,        '!' :   1,        '"' :   2,        '#' :   3,
        '$' :   4,        '%' :   5,        '&' :   6,       '\'' :   7,
        '(' :   8,        ')' :   9,        '*' :  10,        '+' :  11,
        ',' :  12,        '-' :  13,        '.' :  14,        '/' :  15,
        '0' :  16,        '1' :  17,        '2' :  18,        '3' :  19,
        '4' :  20,        '5' :  21,        '6' :  22,        '7' :  23,
        '8' :  24,        '9' :  25,        ':' :  26,        ';' :  27,
        '<' :  28,        '=' :  29,        '>' :  30,        '?' :  31,
        '@' :  32,        'A' :  33,        'B' :  34,        'C' :  35,
        'D' :  36,        'E' :  37,        'F' :  38,        'G' :  39,
        'H' :  40,        'I' :  41,        'J' :  42,        'K' :  43,
        'L' :  44,        'M' :  45,        'N' :  46,        'O' :  47,
        'P' :  48,        'Q' :  49,        'R' :  50,        'S' :  51,
        'T' :  52,        'U' :  53,        'V' :  54,        'W' :  55,
        'X' :  56,        'Y' :  57,        'Z' :  58,        '[' :  59,
       '\\' :  60,        ']' :  61,        '^' :  62,        '_' :  63,
        '`' :  64,        'a' :  65,        'b' :  66,        'c' :  67,
        'd' :  68,        'e' :  69,        'f' :  70,        'g' :  71,
        'h' :  72,        'i' :  73,        'j' :  74,        'k' :  75,
        'l' :  76,        'm' :  77,        'n' :  78,        'o' :  79,
        'p' :  80,        'q' :  81,        'r' :  82,        's' :  83,
        't' :  84,        'u' :  85,        'v' :  86,        'w' :  87,
        'x' :  88,        'y' :  89,        'z' :  90,        '{' :  91,
        '|' :  92,        '}' :  93,        '~' :  94,     '\x7f' :  95,
     '\xf3' :  96,     '\xf2' :  97,    'SHIFT' :  98,     'TO_C' :  99,
     '\xf4' : 100,     'TO_A' : 101,     '\xf1' : 102
}

setc = {
    '00': 0, '01': 1, '02': 2, '03': 3, '04': 4,
    '05': 5, '06': 6, '07': 7, '08': 8, '09': 9,
    '10':10, '11':11, '12':12, '13':13, '14':14,
    '15':15, '16':16, '17':17, '18':18, '19':19,
    '20':20, '21':21, '22':22, '23':23, '24':24,
    '25':25, '26':26, '27':27, '28':28, '29':29,
    '30':30, '31':31, '32':32, '33':33, '34':34,
    '35':35, '36':36, '37':37, '38':38, '39':39,
    '40':40, '41':41, '42':42, '43':43, '44':44,
    '45':45, '46':46, '47':47, '48':48, '49':49,
    '50':50, '51':51, '52':52, '53':53, '54':54,
    '55':55, '56':56, '57':57, '58':58, '59':59,
    '60':60, '61':61, '62':62, '63':63, '64':64,
    '65':65, '66':66, '67':67, '68':68, '69':69,
    '70':70, '71':71, '72':72, '73':73, '74':74,
    '75':75, '76':76, '77':77, '78':78, '79':79,
    '80':80, '81':81, '82':82, '83':83, '84':84,
    '85':85, '86':86, '87':87, '88':88, '89':89,
    '90':90, '91':91, '92':92, '93':93, '94':94,
    '95':95, '96':96, '97':97, '98':98, '99':99,

    'TO_B' : 100,    'TO_A' : 101,    '\xf1' : 102
}

setmap = {
    'TO_A' : (seta, setb),
    'TO_B' : (setb, seta),
    'TO_C' : (setc, None),
    'START_A' : (starta, seta, setb),
    'START_B' : (startb, setb, seta),
    'START_C' : (startc, setc, None),
}

CODE128A  =  0
CODE128B  =  1
CODE128C  =  2



class code128_encode:
    set_x = CODE128A
    def __init__(self, settype = CODE128A):
        self.set_x = settype
        
    def set_setx(self,settype):
        if(settype!=CODE128A)&(settype!=CODE128B)&(settype!=CODE128C):
            self.set_x = settype 

          
    def encode(self,code):
        print(self.set_x)
        #Calculate Total
        if(self.set_x==CODE128A):
            start = starta 
            total = starta       
            setx  = seta     
        elif(self.set_x==CODE128B):
            start = startb 
            total = startb       
            setx  = setb          
        elif(self.set_x==CODE128C):
            start = startc
            total = startc       
            setx  = setc
        else:
            return False

        for i,n in enumerate(list(code)):
            total = total+setx[n]*(i+1)
        
        remainder = total % 103
        

        if (remainder < 95):
            remainder =remainder+ 32
        else:
            remainder =remainder +100
            
        encode =chr(100+start) + code + chr(remainder) + chr(100+stop)
        return encode