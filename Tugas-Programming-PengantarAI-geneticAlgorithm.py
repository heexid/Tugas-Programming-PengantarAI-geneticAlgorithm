import math # untuk operasi math cos sin
import random # untuk random number

#h
def h(x1,x2):
    return math.cos(x1) *  math.sin(x2) - (x1 / (x2**2 + 1))

#fungsi fitness minimal
def f(x1,x2):
    return 1/(h(x1,x2) + 0.01)

#Batasan -1 <= x1 <= 2, -1 <= x2 <= 1
upper_x1 = 2
lower_x1 = -1
upper_x2 = 1
lower_x2 = -1

#Kromosom
class Kromosom:
    def __init__(self, bit = None):
        if bit == None:
            #random bit dengan panjang k
            self.bit = random.choices([0 , 1], k=8)
        else:
            self.bit = bit
            
        #decode 
        self.x1 = self.decode(upper_x1, lower_x1, self.bit[:4])
        self.x2 = self.decode(upper_x2, lower_x2, self.bit[4:])
    
    #decode
    def decode(self, ra, rb, g):
        sum1,sum2 = 0, 0
        j = 0
        for i in range(1, len(g) + 1):
            sum1 = 2**-i + sum1
        for i in range(len(g)):
            j = j - 1
            sum2 = g[i] * 2**j + sum2
        return rb + (((ra - rb) / sum1) * sum2 )

#test Kromosom and Decode
'''
test = Kromosom()
print(test.bit)
print(test.x1)
print(test.x2)
'''
'''
#create populasi
populasi = []
batasPopulasi = 10
generasi = 1
while len(populasi) != batasPopulasi:
    k = Kromosom()
    #cek Kromosom ada yang sama atau tidak didalam populasi 
    found = False
    for i in populasi:
        if i.bit == k.bit:
            found = True
            break
    if not found:
        populasi.append(k)
'''

'''
#print populasi
for i in range(len(populasi)):
    print(populasi[i].bit, ' x1 =', populasi[i].x1, ' x2 =', populasi[i].x2, ' ',)
'''

#pemilihan orangtua Roulette Wheel pilih kromosom dipopulasi dengan probabilitas terpilih
def seleksiOrangtua(k):
    orangtua = []
    #menyimpan nilai fitness dari semua k di populasi
    fitness = []
    weight = []
    for i in range(len(populasi)):
        fitnessValue = f(populasi[i].x1,populasi[i].x2)
        fitness.append(fitnessValue)
    for i in range(len(populasi)):
        weightValue = fitness[i] / sum(fitness)
        weight.append(weightValue)
    while len(orangtua) != k:
        #memilih secara random dari populasi
        calon = random.choices(populasi, weights = weight)[0]
        #cek agar tidak ada calon dengan bit yang sama
        found = False
        for i in orangtua:
            if i.bit == calon.bit:
                found = True
                break
        if not found:
            orangtua.append(calon)
    return orangtua


'''
orangtua = seleksiOrangtua(2)
for i in orangtua:
    print(i.bit)
'''

#mutasi
def mutasi(anak1,anak2):
    #chance mutasi 0.9%
    chance = 0.9 * (1/100)
    if random.uniform(0,100) <= chance:
        titik = random.randint(0, len(anak1))
        if anak1[titik] == 0:
            anak1[titik] = 1
        else:
            anak1[titik] = 0

    if random.uniform(0,100) <= chance:
        titik = random.randint(0, len(anak2))
        if anak2[titik] == 0:
            anak2[titik] = 1
        else:
            anak2[titik] = 0

#Rekombinasi 1 titik
def rekombinasi(ortu1,ortu2):
    titik = random.randint(1, len(ortu1.bit) - 1)

    anak1 = ortu1.bit[:titik] + ortu2.bit[titik:]
    anak2 = ortu2.bit[:titik] + ortu1.bit[titik:]

    mutasi(anak1,anak2)

    #print(anak1,anak2)

    populasi.append(Kromosom(anak1))
    populasi.append(Kromosom(anak2))

    
#test rekombinasi mutasi
#rekombinasi(orangtua[0],orangtua[1])

#Seleksi survivor
#Membuang kromosom yang tidak diinginkan berdasarkan nilai h (h positif terbesar yang dibuang)
def seleksiSurvivor():
    #sorting dengan parameter nilai h terkecil -> terbesar 
    populasi.sort(key = lambda x :h(x.x1,x.x2))

    #mempop list
    while len(populasi) != batasPopulasi:
        populasi.pop()

#test
#seleksiSurvivor()

#preview sort
'''
for i in range(len(populasi)):
    print(populasi[i].bit, ' x1 =', populasi[i].x1, ' x2 =', populasi[i].x2, ' ', ' h =',h(populasi[i].x1,populasi[i].x2))
print(len(populasi))
'''

#Main
#create populasi
populasi = []
batasPopulasi = 10

generasi = 1
while len(populasi) != batasPopulasi:
    k = Kromosom()
    #cek Kromosom ada yang sama atau tidak didalam populasi 
    found = False
    for i in populasi:
        if i.bit == k.bit:
            found = True
            break
    if not found:
        populasi.append(k)

#batasan generasi (terminasi iterasi)
batasGenerasi = 20
while generasi <= batasGenerasi:
    
    print("Generasi ke ", generasi)
    for i in range(len(populasi)):
        '''
        #print setiap populasi digenerasi
        print(populasi[i].bit, ' x1 = ', populasi[i].x1, ' x2 = ', populasi[i].x2, ' h = ',h(populasi[i].x1,populasi[i].x2), ' f = ',f(populasi[i].x1,populasi[i].x2))
        '''
        #print populasi generasi = 1 dan populasi generas ke-terminasi
        if generasi == 1 or generasi == 20:
            print(populasi[i].bit, ' x1 = ', populasi[i].x1, ' x2 = ', populasi[i].x2, ' h = ',h(populasi[i].x1,populasi[i].x2), ' f = ',f(populasi[i].x1,populasi[i].x2))
    
    orangtua = seleksiOrangtua(2)
    seleksiSurvivor()
    rekombinasi(orangtua[0],orangtua[1])
    generasi = generasi + 1