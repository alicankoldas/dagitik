__author__ = 'AKOLDAS'

import matplotlib.pyplot as plt
import numpy as np


n = 10000

sayi_cifti_1 = np.random.normal(3,1,n)
# ilk dizimiz icin sayilari cekiyoruz
sayi_cifti_2 = np.random.normal(-1,1.2,n)
# ikinci dizimiz icin sayilari cekiyoruz

print(sayi_cifti_1)
print(sayi_cifti_2)

var_arrondi_1 = np.around(sayi_cifti_1)
# ilk dizimiz icin cektigimiz degerleri en yakin tamsayiya yuvarliyoruz
print(var_arrondi_1)
var_arrondi_2 = np.around(sayi_cifti_2)
# ikinci dizimiz icin cektigimiz degerleri en yakin tamsayiya yuvarliyoruz
print(var_arrondi_2)

bin_1 = np.array([-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
degisken_1 = np.digitize(var_arrondi_1, bin_1)
# digitize metodu sayesinde yuvarlanmis sayilarimizin hangi indeks uzerinde oldugunu buluyoruz
bin_2 = np.array([-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
degisken_2 = np.digitize(var_arrondi_2, bin_2)

print(degisken_1)
degisken_1 = degisken_1 - 1
print(degisken_2)
degisken_2 = degisken_2 - 1

zarray_1 = np.zeros(41)
zarray_2 = np.zeros(41)
# 41 elemanli 0dan olusan iki dizi tanimliyoruz

print(len(degisken_1))
print(len(degisken_2))

print(len(zarray_1))
print(len(zarray_2))

for i in range(len(zarray_1)):
    for j in range(len(degisken_1)):
      if degisken_1[j] == i:
            zarray_1[i] = zarray_1[i] + 1

for i in range(len(zarray_2)):
    for j in range(len(degisken_2)):
      if degisken_2[j] == i:
            zarray_2[i] = zarray_2[i] + 1
# yeni tanimlamis oldugumuz bos diziler uzerine yuvarlanmis sayilarimizi yerlestiriyoruz

print(zarray_1)
print(zarray_2)

for i in range(len(zarray_1)):
    zarray_1[i] = zarray_1[i]/n

print(zarray_1)

for i in range(len(zarray_2)):
    zarray_2[i] = zarray_2[i]/n
# ustte normalizasyon islemini gerceklestiriyoruz
#print(zarray_2)

i = 0
j = 0
k = 0
l = 0
mesafe = 0
mesafe_1 = 0
mesafe_2 = 0


for i in range (len(zarray_1)):
    for j in range(len(zarray_2)):
            if((zarray_2[j] > zarray_1[i]) and zarray_1[i] != 0 and zarray_2[j] != 0  ):
                zarray_2[j] = zarray_2[j] - zarray_1[i]
                mesafe = mesafe + zarray_1[i]*abs(j-i)
                print(mesafe)
                print('*')#mekanizmayi anlamaniz icin bu yildizlar konuldu. donguyu takip edebilin diye
                zarray_1[i] = 0
                i = i + 1
            if((zarray_2[j] == zarray_1[i])  and zarray_1[i] != 0 and zarray_2[j] != 0):
                zarray_2[j] = zarray_2[j] - zarray_1[i]
                mesafe_1 = mesafe_1 + zarray_1[i]*abs(j-i)
                print(mesafe_1)
                print('**')#mekanizmayi anlamaniz icin bu yildizlar konuldu. donguyu takip edebilin diye
                zarray_1[i] = 0
                zarray_2[j] = 0
                i = i + 1
                j = j + 1
            elif((zarray_2[j] < zarray_1[i])  and zarray_1[i] != 0 and zarray_2[j] != 0):
                mesafe_2 = mesafe_2 + zarray_2[j]*abs(j-i)
                print(mesafe_2)
                print('***')#mekanizmayi anlamaniz icin bu yildizlar konuldu. donguyu takip edebilin diye
                zarray_1[i] = zarray_1[i] - zarray_2[j]
                zarray_2[j] = 0
                j = j + 1
# ustteki buyuk for dongusunde ise Wasserstein metric metodunu gerceklestirmis bulunuyoruz
mesafe_3 = mesafe + mesafe_1 + mesafe_2
# mesafe_3 de hesaplamanin sonucunu vermektedir

print(zarray_1)
print(zarray_2)
# gordugunuz gibi iki dizi de sifirlaniyor
print(mesafe_3)

x = var_arrondi_1
y = var_arrondi_2


# histogrami cizdirmek icin yazilmis bir kod
lin = np.linspace(-20,20,41)
plt.hist(x,lin, alpha = 0.5)
plt.hist(y,lin, alpha = 0.5)
plt.show()