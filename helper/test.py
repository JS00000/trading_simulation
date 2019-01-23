import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 10)
number = 10
cmap = plt.get_cmap('gnuplot')

# colors = [cmap(i) for i in np.linspace(0, 1, number)]

colors = [(i/number, 0, 0, 1) for i in range(number)]

for i, color in enumerate(colors, start=1):
    plt.plot(x, i * x + i, color=color, label='$y = {i}x + {i}$'.format(i=i))
plt.legend(loc='best')
plt.show()