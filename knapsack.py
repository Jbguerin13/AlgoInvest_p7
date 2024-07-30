import csv
import time
import os, psutil

start = time.time()

# Calculate cpu ressources using
cpu_before = psutil.cpu_percent(interval=1, percpu=True)
print(f"CPU used before : {cpu_before} %")

# Get RAM used
ram_usage = psutil.virtual_memory().used
ram_usage_go = ram_usage / (1024*1024*1024)

print(f"RAM used before : {ram_usage_go}, giga octets")

# Function to fetch max profit using knapsack algorithm with weighting to cancel calculation repeat
import csv
import time
import os, psutil

start = time.time()

# Calculate cpu ressources using
cpu_before = psutil.cpu_percent(interval=1, percpu=True)
print(f"CPU used before : {cpu_before} %")

# Get RAM used
ram_usage = psutil.virtual_memory().used
ram_usage_go = ram_usage / (1024*1024*1024)

print(f"RAM used before : {ram_usage_go}, giga octets")

# Function to fetch max profit using knapsack algorithm with weighting to cancel calculation repeat
def knapsack(actions, max_budget):
    n = len(actions)
    #initialize a table for dp to  keep in memory each profit_max calculated before
    profit_max = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1): #browse each actions
        for j in range(max_budget + 1): #budget possible for each action
            if actions[i-1]['cost'] <= j:
                profit_max[i][j] = max(profit_max[i-1][j], profit_max[i-1][j - actions[i-1]['cost']] + actions[i-1]['profit'])
            else:
                profit_max[i][j] = profit_max[i-1][j]

    j = max_budget
    best_combination = []
    for i in range(n, 0, -1):
        if profit_max[i][j] != profit_max[i-1][j]:
            best_combination.append(actions[i-1])
            j -= actions[i-1]['cost']

    return best_combination


def convert_profit_to_percent(profit: str) -> float:
    return int(profit) / 100


#main process
actions = []
with open('data_part1.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        price = row['price']
        profit = row['profit']
        
        # Skip rows with missing data
        if not price  or not profit:
            continue
        
        price = row['price'].replace(',', '.')
        profit = row['profit']
        actions.append({
            'action': row['name'],
            'cost': int(row['price']),
            'profit': convert_profit_to_percent(profit)
        })

# Sort actions by profit-to-cost ratio for better efficiency - reading best ratio then skip the weaks one
actions.sort(key=lambda x: x['profit'] / x['cost'], reverse=True)

max_budget = 500
best_combination = knapsack(actions, max_budget)

# Print result
print("Best action combination:")
for action in best_combination:
    print(f"{action['action']} - Cost: {action['cost']}€ - Profit: {action['profit']}")

end = time.time()

total_profit = round(sum(action['profit'] * action['cost'] for action in best_combination), 2)
print(f"Profit total : {total_profit}")
print(f"budget spent: {sum(action['cost'] for action in best_combination)}")
print(f"Temps d'exécution : {round(end - start, 2)} secondes")

cpu_after = psutil.cpu_percent(interval=1, percpu=True)
ram_usage_after = psutil.virtual_memory().used
ram_usage_after_go = ram_usage_after / (1024*1024*1024)

print(f"CPU used after running processus : {cpu_after} %")
print(f"RAM used after running processus : {ram_usage_after_go}, giga octets")
