import json
import random
import sys

with open('mmo_items.json', 'r') as mmo_items_fp:
    mmo_items = json.load(mmo_items_fp)

common_items = mmo_items['items']['common']
rare_items = mmo_items['items']['rare']
ultra_items = mmo_items['items']['ultra-rare']

common_prob = mmo_items['probabilities']['common']
rare_prob = mmo_items['probabilities']['rare']
ultra_prob = mmo_items['probabilities']['ultra-rare']

if not (1 - 1e-7 <= common_prob + rare_prob + ultra_prob <= 1 + 1e-7):
    print('Sum of probabilities should be equal to 1')
    sys.exit()

message = 'Press enter to open a case or print `exit` to leave: '
while (choice := input(message)) != 'exit':
    items = list()
    rare_exists = False
    ultra_exists = False
    while len(items) != 5:
        val = random.random()
        accum = 0

        accum += rare_prob
        if val <= accum:
            if rare_exists:
                continue
            items.append(('rare', random.choice(rare_items)))
            rare_exists = True
            continue

        accum += ultra_prob
        if val <= accum:
            if ultra_exists:
                continue
            items.append(('ultra rare', random.choice(ultra_items)))
            ultra_exists = True
            continue

        accum += common_prob
        if val <= accum:
            items.append(('common', random.choice(common_items)))
            continue

    print('Your items:')
    i = 0
    for rarity, item in items:
        i += 1
        print(f'{i}: {rarity: <10} {item}')
