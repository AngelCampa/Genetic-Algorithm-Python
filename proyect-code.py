from fastquant import get_stock_data
from fastquant import backtest
import math
import numpy as np
import random
import matplotlib.pyplot as plt

df = get_stock_data("BIMBOA.MX", "2020-01-01", "2021-01-01")

#Se pregunta al usuario los n invididuos de la poblacion inicial y el numero de generaciones
n = int(input("Ingrese n: "))

gen = int(input("Ingrese el numero de generaciones: "))
Po = []
Winners = []
Winners_Ap = []
Son = []
#Se inicia cierto numero de  generaciones
for i in range(gen):

    Father = []
    Son_Binary = []
    #Si Po esta vacio, se genera el arreglo inicial de n valores. Si es la 2 o mas iteracion se toma el Po que ya se genero al final
    if Po == []:
        for i in range(n):
            Po_Temp = []
            Po_Temp.append(random.randint(3, 100))
            Po_Temp.append(random.randint(51, 100))
            Po_Temp.append(random.randint(3, 50))
            Po.append(Po_Temp)
    else:
        pass
    Po.sort()
    #La funcion objetivo calculada sobre la poblacion inicial
    Ap = []
    for i in Po:
        strat1 = backtest('rsi', df, rsi_period=i[0], rsi_upper=i[1], rsi_lower=i[2], plot=False, verbose = 0)
        Ap.append(list(strat1['final_value'])[0])

    #Se juntan los 2 arreglos
    Po_Ap = np.column_stack((Po, Ap))
    #    #Empieza el torneo que se repetira n veces hasta que el arreglo padres sea igual o mayor a n
    for i in range(n):
        if len(Father) >= n:
            break
        else:
            #Se reordenan los valores aleatoriamente, y compiten en un for loop
            #El primero con el segundo, el tercero con el cuarto, se escoge al que tenga la aptitud mas alta
            #Y se agrega al arreglo Padres
            np.random.shuffle(Po_Ap)
            for j in range(0, n+1, 2):
                #El try esta porque cuando es impar marca error, si es impar se rompe el loop
                try:
                    if len(Father) >= n:
                        break
                    elif Po_Ap[j, 3] >= Po_Ap[j+1, 3]:
                        Father.extend([[int(Po_Ap[j, 0]), int(Po_Ap[j, 1]), int(Po_Ap[j, 2])]])
                    elif Po_Ap[j, 3] <= Po_Ap[j+1, 3]:
                        Father.extend([[int(Po_Ap[j+1, 0]), int(Po_Ap[j+1, 1]), int(Po_Ap[j+1, 2])]])
                except IndexError:
                    pass
    #Se van a aparear los padres n/2 veces
    for i in range(int(n/2)):
        Fathers_mate = []
        for j in range(n**3):
            #Se escoge aleatoriamente un nuevo arreglo para los 2 padres que se van a aparear
            #Si el arreglo tiene 2 o mas, se acaba el loop
            #Se escoge aleatoriamente del arreglo Father, los 2 padres que procrearan
            random_father = random.choice(Father)
            if len(Fathers_mate) >= 2:
                break
            # elif random_father not in Fathers_mate:
            else:
                Fathers_mate.append(random_father)
        #Ya escogidos los padres, se escoge un numero aleatorio de 0 a 1, si es mayor que 0.2 se aparean y tienen 2 hijos
        #Se convierten los padres a aprearse a binario, y luego se toman los primeros 2 bits del primero,
        #los 4 bits de en medio del segundo, y los ultimos 2 bits del primero para el primer hijo
        #Para el segundo hijo se escogen los primeros 2 bits del segundo, siguientes 4 del primero, y ultimos 2 del segundo
        Fathers_mate_bin = []

        if random.random() > 0.5:
            try:
                for i in range(len(Fathers_mate)):
                    Fathers_mate_bin_temporary = [np.binary_repr(int(j), width=8) for j in Fathers_mate[i]]
                    Fathers_mate_bin.append(Fathers_mate_bin_temporary)
                Son_Binary_Temp = []
                Son_Binary_Temp.append(Fathers_mate_bin[0][0][:2] + Fathers_mate_bin[1][0][2:6] + Fathers_mate_bin[0][0][6:])
                Son_Binary_Temp.append(Fathers_mate_bin[0][1][:2] + Fathers_mate_bin[1][1][2:6] + Fathers_mate_bin[0][1][6:])
                Son_Binary_Temp.append(Fathers_mate_bin[0][2][:2] + Fathers_mate_bin[1][2][2:6] + Fathers_mate_bin[0][2][6:])
                Son_Binary.append(Son_Binary_Temp)

                Son_Binary_Temp = []
                Son_Binary_Temp.append(Fathers_mate_bin[1][0][:2] + Fathers_mate_bin[0][0][2:6] + Fathers_mate_bin[1][0][6:])
                Son_Binary_Temp.append(Fathers_mate_bin[1][1][:2] + Fathers_mate_bin[0][1][2:6] + Fathers_mate_bin[1][1][6:])
                Son_Binary_Temp.append(Fathers_mate_bin[1][2][:2] + Fathers_mate_bin[0][2][2:6] + Fathers_mate_bin[1][2][6:])
                Son_Binary.append(Son_Binary_Temp)
            except IndexError:
                pass
        else:
            pass

    #Mutacion
    #Si la prob es mayor a 0.2, muta. Se escoge un valor aleatorio dentro del hijo convertido a binario, y se cambia el valor
    #Si es 0, sera 1. Si es 1, sera 0
    #Se inserta el nuevo hijo mutado al arreglo de hijos en binario
    for i in range(len(Son_Binary)):
        for j in range(len(Son_Binary[i])):
            if random.random() < 0.2:
                i_value = Son_Binary[i][j]
                rand_index_from_i_value = random.randrange(-5, len(i_value))
                if i_value[rand_index_from_i_value] == '1':
                    mutation = '0'
                else:
                    mutation = '1'
                new_i_value = i_value[:rand_index_from_i_value] + mutation + i_value[rand_index_from_i_value+1:]
                Son_Binary[i][j] = new_i_value

    #Se convierte de nuevo hijos en binario a valores enteros
    try:
        for i in range(len(Son_Binary)):
            Son_Temp = []
            for j in Son_Binary[i]:
                if int(j, 2) <= 100 and int(j, 2) > 3:
                    Son_Temp.append(int(j, 2))
                else:
                    Son_Temp = []
                    break
            if Son_Temp != []:
                Son.append(Son_Temp)
            else:
                pass
                
    except:
        pass
    #Se suman hijos y padres para generar el arreglo ganadores
    G = Father + Son
    #se calcula aptitud
    G_Ap = []
    for i in G:
        strat2 = backtest('rsi', df, rsi_period=i[0], rsi_upper=i[1], rsi_lower=i[2], plot=False, verbose = 0)
        G_Ap.append(list(strat2['final_value'])[0])
    #Se juntan los valores y su aptitud
    G_Po_Ap = np.column_stack((G, G_Ap))
    #Se ordena segun su aptitud
    G_Po_Ap_sorted = G_Po_Ap[G_Po_Ap[:, -1].argsort()]
    #Se consiguen los n mejores valores segun su aptitud
    n_best = G_Po_Ap_sorted[:][len(G_Po_Ap_sorted)-n:]
    #Se selecciona al mejor valor junto con su aptitud
    the_best = n_best[:][-1:]
    #Los n mejores valores se convierten en la nueva poblacion inicial
    Po = []
    for row in n_best:
        Po_temp = [int(row[value]) for value in range(3)]
        Po.append(Po_temp)
    Winners.append(the_best[-1][:-1].tolist())
    Winners_Ap.append(int(the_best[-1][-1]))
    print(Winners)
    print(Winners_Ap)


# plt.plot(Winners_Ap)
# plt.show()
# plt.plot(Winners)
# plt.show()
