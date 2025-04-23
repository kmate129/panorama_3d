import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from utils import from_folder_to_3d_grid

class InteractiveViewerWithSliders:
    def __init__(self, ct):
        self.ct = ct
        self.coronal_index = ct.shape[1] // 2
        self.sagittal_index = ct.shape[2] // 2

        self.fig, (self.ax_coronal, self.ax_sagittal) = plt.subplots(1, 2, figsize=(12, 8))
       
        self.im_coronal = self.ax_coronal.imshow(
            np.flipud(self.ct[:, self.coronal_index, :]), cmap='gray'
        )
        self.ax_coronal.set_title(f'Koronális metszet: {self.coronal_index}')
        self.ax_coronal.axis('off')

        self.im_sagittal = self.ax_sagittal.imshow(
            np.flipud(self.ct[:, :, self.sagittal_index]), cmap='gray'
        )
        self.ax_sagittal.set_title(f'Szagittális metszet: {self.sagittal_index}')
        self.ax_sagittal.axis('off')

        # coronal slider
        ax_coronal_slider = self.fig.add_axes([0.15, 0.02, 0.3, 0.02])  # left, bottom, width, height
        self.coronal_slider = Slider(
            ax=ax_coronal_slider,
            label="Koronális",
            valmin=0,
            valmax=self.ct.shape[1] - 1,
            valinit=self.coronal_index,
            valstep=1
        )
        self.coronal_slider.on_changed(self.update_coronal_slider)

        # sagittal slider
        ax_sagittal_slider = self.fig.add_axes([0.55, 0.02, 0.3, 0.02])
        self.sagittal_slider = Slider(
            ax=ax_sagittal_slider,
            label="Szagittális",
            valmin=0,
            valmax=self.ct.shape[2] - 1,
            valinit=self.sagittal_index,
            valstep=1
        )
        self.sagittal_slider.on_changed(self.update_sagittal_slider)

        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_key(self, event):
        if event.key == 'up':
            self.coronal_index = min(self.coronal_index + 1, self.ct.shape[1] - 1)
        elif event.key == 'down':
            self.coronal_index = max(self.coronal_index - 1, 0)

        elif event.key == 'right':
            self.sagittal_index = min(self.sagittal_index + 1, self.ct.shape[2] - 1)
        elif event.key == 'left':
            self.sagittal_index = max(self.sagittal_index - 1, 0)

        self.coronal_slider.set_val(self.coronal_index)
        self.sagittal_slider.set_val(self.sagittal_index)

    def update_coronal_slider(self, val):
        self.coronal_index = int(val)
        self.update_plots()

    def update_sagittal_slider(self, val):
        self.sagittal_index = int(val)
        self.update_plots()

    def update_plots(self):
        coronal_slice = np.flipud(self.ct[:, self.coronal_index, :])
        self.im_coronal.set_data(coronal_slice)
        self.ax_coronal.set_title(f'Koronális metszet: {self.coronal_index}')

        sagittal_slice = np.flipud(self.ct[:, :, self.sagittal_index])
        self.im_sagittal.set_data(sagittal_slice)
        self.ax_sagittal.set_title(f'Szagittális metszet: {self.sagittal_index}')

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


ct = from_folder_to_3d_grid('original_png_8bit', 688)
viewer = InteractiveViewerWithSliders(ct)
viewer.show()
