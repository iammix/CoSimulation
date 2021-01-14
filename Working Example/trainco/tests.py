import numpy as np
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.transforms as mtransforms

# Create figure
fig, ax = plt.subplots()

# Axes labels and title are established
ax.set_xlabel('x')
ax.set_ylabel('y')

ax.set_ylim(-2,2)
ax.set_xlim(-2,2)
ax.set_aspect('equal', adjustable='box')

N = 20
x = np.linspace(-1,1,N) 
y  = np.linspace(-1,1,N) 
dx = np.sin(x)
dy = np.cos(y)

patch = patches.Arrow(x[0], y[0], dx[0], dy[0])

def init():
    ax.add_patch(patch)
    return patch,

def animate(t):
    L = np.hypot(dx[t], dy[t])

    if L != 0:
        cx = float(dx[t]) / L
        sx = float(dy[t]) / L
    else:
        # Account for division by zero
        cx, sx = 0, 1

    trans1 = mtransforms.Affine2D().scale(L, 1)
    trans2 = mtransforms.Affine2D.from_values(cx, sx, -sx, cx, 0.0, 0.0)
    trans3 = mtransforms.Affine2D().translate(x[t], y[t])
    trans = trans1 + trans2 + trans3
    patch._patch_transform = trans.frozen()
    return patch,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               interval=20,
                               frames=N,
                               blit=False)

plt.show()