
tablero =[3,5,-2,1,2,-1,-2]

es_max=False

def minimax (num,es_max, profundidad, alpha, beta):
    if profundidad == 0:
        return num
    
    if es_max:
        mejor = -99
        for nuevo_num in tablero:
            valor=minimax(nuevo_num, False, profundidad-1, alpha, beta)
            mejor = max(mejor, valor)
            alpha = max(alpha, mejor)
            if beta <= alpha:
                print("🌱 Poda en MAX")
                break
        return mejor
    else:
        peor= 99
        for nuevo_num in tablero:
            valor=minimax(nuevo_num, True, profundidad-1, alpha, beta)
            peor= min(peor, valor)
            beta = min(beta, peor)
            if beta <= alpha:
                print("🌱 Poda en MIN")
                break
        return peor

print(minimax(1, es_max, 2, -999, 999))