#!/usr/bin/python2

try: 
	import re
	import requests
	from bs4 import BeautifulSoup 
	import sys
	import os
        import binascii
except Exception as err:
	print "[!] "+str(err)
	sys.exit(0)

baseUrl = "https://factordb.com/"
def interact(n):
    n = str(n)
    myVars = []
    r = requests.get(baseUrl+"index.php?query="+n)
    html = r.content
    mylist =[]
    soup = BeautifulSoup(html,"lxml")
    tables = soup.findAll("table")
    for table in tables:
         if table.findParent("table") is None:
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                mylist.append(str(cells))
    data = mylist[3]
    data = data.split(",")
    soup2 = BeautifulSoup(data[0],"lxml")
    for row in soup2.findAll("td"):
        status = row.text # Get the status

    links = []
    soupLinks = BeautifulSoup(data[2],"lxml")
    for row in soupLinks.findAll("a"):
        links.append(row["href"])
    l = len(links)
    myVars.append([status,links[l-2],links[l-1]])
    return myVars


def get_prime(p):
    r = requests.get(baseUrl+p)
    html = r.content
    soup = BeautifulSoup(html,"lxml")
    try:
        value = soup.find('input', {'name': 'query'}).get('value')
        return value
    except:
        print "Fail"

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def padded_hex(v):
  s = hex(v)[2:].strip('L')
  return s if len(s) % 2 == 0 else '0' + s

if len(sys.argv) < 3 or len(sys.argv) > 7:
    print "Uso:",sys.argv[0],"c e n [p q] [outfile]"
    print "Onde:\n"+\
          "    C: decimal do texto cifrado\n"+\
          "    E: decimal da chave publica\n"+\
          "    N: modulo para as chaves\n"+\
          "    P: fator de N\n"+\
          "    Q: fator de N\n"+\
          "    outfile: arquivo de saida"
    sys.exit()
else:
    c = int(sys.argv[1])
    e = int(sys.argv[2])
    n = int(sys.argv[3])
    if len(sys.argv) >= 6:
        p = int(sys.argv[4])
        q = int(sys.argv[5])
    else:
        print "\nProcurando fatores de N no factordb"
        s,P,Q = interact(n)[0]
        if P == Q:
            print "Nao foram encontrados fatores prontos :("
            sys.exit(0)
        else :
            print "Fatores encontrados!!"
            p = int(get_prime(P))
            q = int(get_prime(Q))

d = modinv(e, n-(p+q-1))
m = padded_hex(pow(c, d, n)).rstrip("L")

if len(sys.argv) == 7 or len(sys.argv) == 5:
    with open(sys.argv[len(sys.argv)-1],'wb') as out:
        out.write(binascii.unhexlify(m))
    print "\nsaida salva em "+sys.argv[len(sys.argv)-1]
else:
    print "\nOUTPUT:",m.decode('hex'),"\n"
