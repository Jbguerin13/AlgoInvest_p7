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

#Function to fetch max profit
def max_profit(actions: list, max_budget: int) -> list:
    best_profit = 0
    best_combination = []

    for i in range(1, 2**len(actions)):
        combination = []
        total_cost = 0
        total_profit = 0

        for j in range(len(actions)):
            if (i >> j) & 1:
                combination.append(actions[j])
                total_cost += actions[j]['cost']
                total_profit += actions[j]['profit']

        if total_cost <= max_budget and total_profit > best_profit:
            best_profit = total_profit
            best_combination = combination  
    return best_combination

def convert_profit_to_percent(profit: str) -> str:
    profit_converted = int(profit)/100
    return profit_converted

#Main processus
actions = []
with open('data_part1.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        price = row['price'].replace(',', '.')
        profit = row['profit']
        actions.append({
            'action': row['name'],
            'cost': int(row['price']),
            'profit': convert_profit_to_percent(profit)
        })


max_budget = 500
best_combination = max_profit(actions, max_budget)

# print result
print("Best action combine :")
for action in best_combination:
    print(action['action'], '- Coût:', action['cost'], '€ - Bénéfice:', action['profit'])

end = time.time()

total_profit = round(sum(round(float(action['profit']) * round(float(action['cost']), 2), 2) for action in best_combination), 2)
print("Profit total :", total_profit)
print("depense:", sum(action['cost'] for action in best_combination))
print(f"execution time : {round(end, 2) - round(start,2)} secondes")

cpu_after = psutil.cpu_percent(interval=1, percpu=True)
ram_usage_after = psutil.virtual_memory().used
ram_usage_after_go = ram_usage_after / (1024*1024*1024)

print(f"CPU used after running processus : {cpu_after} %")
print(f"RAM used after running processus : {ram_usage_after_go}, giga octets")
