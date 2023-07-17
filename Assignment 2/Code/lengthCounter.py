import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv = pd.read_csv('csv/cargurusCars.csv')

print(csv)

totalLength = 0
lengths = []
min = float('inf')
max = -1

for row in csv['Price']:
    # totalLength += len(row)
    # lengths.append(len(row))
    # if len(row) > max:
    #     max = len(row)
    # if len(row) < min:
    #     min = len(row)
    row = int(row.replace('$', ''))
    totalLength += row
    lengths.append(row)
    if row > max:
        max = row
    if row < min:
        min = row

print('Mean: {}'.format(totalLength / len(csv)))
print('Min: {}'.format(min))
print('Max: {}'.format(max))

num_buckets = 15

plt.hist(lengths, bins=np.linspace(min, max, num_buckets))
plt.title('Price')
plt.ylabel('Number of Cars')
plt.xlabel('Price')
plt.show()


