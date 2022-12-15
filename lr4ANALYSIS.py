import json
import math
import numpy as np
import matplotlib.pyplot as plt

with open('resMmod4.json') as json_file:
    data4 = json.load(json_file)
titles = list(data4.keys())[1:-2]
data4_bar = list(data4.values())[1:-2]
print(data4)
with open('resMmod3.json') as json_file:
    data3 = json.load(json_file)
# titles = list(data4.keys())[1:-2]
data3_bar = list(data3.values())[1:-2]
print(data3)

barWidth = 0.3
r1 = np.arange(len(data3_bar))
r2 = [x + barWidth for x in r1]
# print(list(data.keys())[1:-2], list(data.values())[1:-2])
plt.bar(r1, data3_bar, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')

# Create cyan bars
plt.bar(r2, data4_bar, width=barWidth, color='orange', edgecolor='black',  capsize=7, label='4')

# general layout
plt.xticks([r + barWidth for r in range(len(data3_bar))], titles,rotation=90,fontsize=5)
plt.ylabel('height')
plt.subplots_adjust(bottom=0.5, top=0.99)

plt.legend()

# Show graphic
plt.show()
