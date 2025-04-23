
import pyvista as pv

filename = "final_skull_median.stl"
mesh = pv.read(filename)

plotter = pv.Plotter(lighting='light_kit')
plotter.add_mesh(
    mesh,
    color=[222, 184, 135],
    show_edges=False,
    smooth_shading=True 
)
plotter.background_color = 'white'
plotter.add_axes()
plotter.show()