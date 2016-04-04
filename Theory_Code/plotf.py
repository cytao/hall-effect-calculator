import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.05,0.8,0.05)
y1 = np.copy(x)
y2 = np.power(x,2)/np.power(np.log(1-x),2)*((1/np.power(1-x,2))-1)/2
y3 = np.log(1/(1-x))

fig = plt.figure()
plt.plot(x,y1,label="$x$")
plt.plot(x,y2,label=r"$\frac{x^2}{2\ln^2(\frac{1}{1-x})}(\frac{1}{(1-x)^2}-1)$")
plt.plot(x,y3,label=r"$ln(\frac{1}{1-x})$")
plt.xlabel("x = w/R")
plt.ylabel("f(x)")
plt.legend(loc=2)
#plt.show()
plt.savefig("models.png",dpi=300,format="png")
plt.close(fig)
