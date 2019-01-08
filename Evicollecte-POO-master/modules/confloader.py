import csv

"""
data = open("data.csv",'rb')
header = data.readline()
data.seek(len(header))

headers = [h.strip('.') for h in header.split()]
headers = ['idpi'] + headers[2:]  # Replace ['SRC', 'V2.0'] with a Date field instead

headers = [h.strip(';') for h in header.split()]

for line in csv.DictReader(data,filednames=headers,delimiter=';'):
    print(row['0'])
          
          
line=reader.next()
len(line)
line.keys()
#cli , nom, idpi, p_guard,p_alarm,p_fx,p_erreur,p_hy3
"""

""" fonctionne
path = 'data.csv'
list=[]
with open(path,'r') as csvfile:
    for lines in csvfile:
        temp_lines=lines.strip().split(';')
        list.append(temp_lines)
        
print(list[0])
print(list[1])

"""
"""
##Reading Methode
path = 'data.csv'
list=[]
with open(path,'r') as csvfile:
    for lines in csvfile:
        for item in lines.split(';'):
            
            list.append(item)

print(list[1])
print(list[3])
print(list)
#Fin Reading Méthode

# Debut Writing Méthode
list = []
with open('writed.csv','w') as csvfile:
    write = csv.writer(csvfile,delimiter=';')
    write.writerow(['abv','youyouu'])

with open('writed.csv','r') as csvfile:
    for lines in csvfile:
        for item in lines.split(';'):
            list.append(item)

print(" ")
print(list)
print(list[1])
#Fin Methode Writing
"""
path = 'config/data.csv'
def VerifConf():
    list = []
    try:
        print("Verification d'un fichier de conf existant")
        list=[]
        with open(path,'r') as csvfile:
            for lines in csvfile:
                for item in lines.split(';'):
                    list.append(item)
        return list
    except:
        print("pas de config existante")
        return False
        

def RecordConf(tab):
    try:
        print("Enregistrement de la conf")
        
        with open('writed.csv','w') as csvfile:
            write = csv.writer(csvfile,delimiter=';')
            write.writerow([tab[0],tab[1],tab[2],tab[3],tab[4],tab[5],tab[7]])
    except:
        print("Erreur d'enregistrement")

VerifConf()


