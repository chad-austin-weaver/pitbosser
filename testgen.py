import csv
from faker import Faker
import numpy

def export_test_to_csv(csv_name, rows):
    with open(csv_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)

#Takes input and generates random test suited for loading casino. avg_games as ratio 0.0-1.0
def generate_random_test(max_relief_tables, game_types, tables, dealers, avg_games):
    fake = Faker()
    
    rows = []
    rows.append([max_relief_tables])
    rows[0] = rows[0] + game_types
    rows.append(tables)

    N = (len(game_types) - 1) * dealers
    K = round((len(game_types)) * dealers * avg_games) - dealers #K ones, N-K zeros
    if K <= 0:
        K = 0
    if K > N:
        K = N

    arr = numpy.array([0] * (N-K) + [1] * K)
    numpy.random.shuffle(arr)
    arr = numpy.split(arr, dealers)
    for i in range(dealers):
        rows.append([fake.name()])
        arr_i = numpy.append([1], arr[i])
        numpy.random.shuffle(arr_i)
        arr_list = arr_i.tolist()
        rows[i+2] = rows[i+2] + arr_list
    
    return rows
        