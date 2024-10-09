import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
from brokenaxes import brokenaxes
import csv
import numpy as np

fname = str(input("Input filename: "))
f = open(fname, "r")
data = csv.reader(f)
next(data)
energy = []
efd = []
organs = ["","","","",""]

for row in data:
    if float(row[3]) > 0 and row[0].replace('logical', '') != 'Trunk':
        efd.append(float(row[3]))
        energy.append(float(row[1]))
        organs.append(row[0].replace('logical', ''))

X_axis = np.arange(len(organs))
bars_energy = plt.bar(X_axis + 0.2, energy, color='#fc6b5d', width=0.4, label='Energy(MeV)')  
bars_efd = plt.bar(X_axis - 0.2, efd, color='#2E9AFE', width=0.4, label='Effective Dose(mSv)')
plt.xticks(X_axis, organs)
plt.title("Energy Deposition")
plt.legend()
plt.grid()
ax = plt.gca()
ax.set_yscale('log')
ax.yaxis.set_major_formatter(LogFormatter(base=10))
for bar in bars_energy:
    for rect in bar.get_children():
        yval = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, yval + 2, round(yval, 2), ha='center', va='bottom', fontsize=8)

for bar in bars_efd:
    for rect in bar.get_children():
        yval = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, yval + 2, round(yval, 2), ha='center', va='bottom', fontsize=8)

plt.show()
