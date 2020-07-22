import time
import threading

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def mandelbrot_image(xmin, xmax, ymin, ymax, iters, size):
    x = np.linspace(xmin, xmax, size, dtype=np.float64)
    y = np.linspace(ymin, ymax, size, dtype=np.float64)
    c = x[np.newaxis, :] + y[:, np.newaxis] * 1j
    z = c
    image = np.zeros(c.shape, dtype=np.int32)
    with np.errstate(over="ignore", invalid="ignore"):
        for i in range(1, iters):
            image[np.less(np.abs(z), 2)] = i
            z = z**2 + c
    image[image == iters - 1] = 0
    return image


class Viewer(object):

    def __init__(self, x0, x1, y0, y1, size=400, zoom=1.1):
        self.default_xy = (x0, x1, y0, y1)
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.size = size
        self.zoom = zoom
        w, h = matplotlib.figure.figaspect(1.)
        self.figure, self.ax = plt.subplots(figsize=(w, h))
        self.figure.canvas.mpl_connect("scroll_event", self.onscroll)
        self.figure.canvas.mpl_connect('key_press_event', self.onkey)

    def event_to_xy(self, event):
        x, y = event.x, event.y
        x, y = self.ax.transData.inverted().transform((x, y))
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return None, None
        x = x * (self.x1 - self.x0) / self.size + self.x0
        y = y * (self.y1 - self.y0) / self.size + self.y0
        return x, y
    
    def onscroll(self, event):
        x, y = self.event_to_xy(event)
        if None in {x, y}:
            return
        if event.button in ["up", "down"]:
            w = self.x1 - self.x0
            h = self.y1 - self.y0        
            if event.button == "up":
                w /= self.zoom
                h /= self.zoom
            elif event.button == "down":
                w *= self.zoom
                h *= self.zoom
            self.x0 = x - w / 2
            self.x1 = x + w / 2
            self.y0 = y - h / 2
            self.y1 = y + h / 2            
            self.draw()

    def onkey(self, event):
        if event.key == "r":
            self.x0, self.x1, self.y0, self.y1 = self.default_xy
            self.draw()
        
    def draw(self):
        image = mandelbrot_image(
            self.x0, self.x1, self.y0, self.y1, iters=150, size=self.size)
        self.ax.imshow(image,
                       cmap=plt.cm.hot,
                       norm=matplotlib.colors.PowerNorm(0.2))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.figure.tight_layout(pad=0)
        self.figure.show()


if __name__ == "__main__":
    print("Use scroll to zoom-in/out at a position."
          "Type 'r' to reset the view.")
    viewer = Viewer(-1.5, 0.5, -1.0, 1.0, size=800)
    viewer.draw()
    plt.show()
    
