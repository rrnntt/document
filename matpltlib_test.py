import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.text(1, 100, r'Hello',family='sans')

def ondraw(event):
    print 'Hello',event.renderer

#fig = plt.figure()
plt.connect('draw_event', ondraw)

plt.show()