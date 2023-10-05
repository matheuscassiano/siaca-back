from functools import reduce

def days_overlap(aula_dias1, aula_dias2):
    # Converte a representação de dias da semana em números inteiros
    days_mapping = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}

    # Cria listas de números inteiros para os dias da semana de ambas as ofertas
    days_list1 = [days_mapping[day] for day in aula_dias1]
    days_list2 = [days_mapping[day] for day in aula_dias2]

    # Verifica se há interseção entre as listas de dias
    return bool(set(days_list1) & set(days_list2))