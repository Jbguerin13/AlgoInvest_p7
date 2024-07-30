import csv
import time
import os, psutil

start = time.time()

# Calculate CPU and RAM resources
cpu_before = psutil.cpu_percent(interval=1, percpu=True)
ram_usage = psutil.virtual_memory().used
ram_usage_go = ram_usage / (1024 * 1024 * 1024)

print(f"CPU used before: {cpu_before} %")
print(f"RAM used before: {ram_usage_go} GB")

# Function to fetch max profit using knapsack algorithm with weighting to cancel calculation repeat
def knapsack(actions, max_budget):
    n = len(actions)
    scale_factor = 100  # Factor to convert costs to integers
    max_budget = int(max_budget * scale_factor)  # Convert budget to integer

    #initialize a table for dp to  keep in memory each profit_max calculated before
    profit_max = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = int(actions[i-1]['cost'] * scale_factor)
        profit = actions[i-1]['profit']

        for j in range(max_budget + 1):
            if cost <= j:
                profit_max[i][j] = max(profit_max[i-1][j], profit_max[i-1][j - cost] + profit)
            else:
                profit_max[i][j] = profit_max[i-1][j]

    j = max_budget
    best_combination = []
    for i in range(n, 0, -1):
        cost = int(actions[i-1]['cost'] * scale_factor)
        if profit_max[i][j] != profit_max[i-1][j]:
            best_combination.append(actions[i-1])
            j -= cost

    return best_combination

# Main process
actions = []
with open("dataset2_Python.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        if float(row['price']) > 0 and float(row['profit']) > 0:
            price = float(row['price'])
            profit = float(row['profit'])
            if profit < 1:
                profit = profit * 100
            actions.append({
                'action': row['name'],
                'cost': price,
                'profit': profit
            })

# Sort actions by profit-to-cost ratio for better efficiency
actions.sort(key=lambda x: x['profit'] / x['cost'], reverse=True)

max_budget = 500
best_combination = knapsack(actions, max_budget)

# Print result
print("Best action combination:")
for action in best_combination:
    print(f"{action['action']} - Cost: {action['cost']}€ - Profit: {action['profit']}%")

# Calculate and print total profit and budget spent
total_profit = round(sum(action['profit'] * action['cost'] / 100 for action in best_combination), 2)
budget_spent = round(sum(action['cost'] for action in best_combination), 2)
print(f"Total profit: {total_profit}€")
print(f"Budget spent: {budget_spent}€")
print(f"Execution time: {round(time.time() - start, 2)} seconds")

cpu_after = psutil.cpu_percent(interval=1, percpu=True)
ram_usage_after = psutil.virtual_memory().used
ram_usage_after_go = ram_usage_after / (1024 * 1024 * 1024)

print(f"CPU used after running process: {cpu_after} %")
print(f"RAM used after running process: {ram_usage_after_go} GB")
