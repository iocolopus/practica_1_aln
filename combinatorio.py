lista = [0, 1, 2, 3, 4]

for i in range(len(lista)):
    for j in range(i+1, len(lista)):
        print((lista[i],lista[j]))