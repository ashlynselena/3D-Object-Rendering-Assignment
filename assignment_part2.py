# __author__: Ashlyn DSouza (ashlynselena@gmail.com)


import assignment_part1 as p1
from assignment_part1 import read_file

import argparse
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib import cm
from matplotlib.colors import ListedColormap, to_rgb


class Object_3D_solid(p1.Object_3D):

    def normalize_array(self, arr):
        """
        Arguments:
            arr: array of 3d coordinates to be normalized
        Returns:
            unit normalized array
        """
        mag = np.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
        norm_array = (arr.T / mag).T
        return norm_array

    def angle_from_z(self):
        """returns the angles of the surface normals from the z-axis for each triangle"""
        normal_vectors = self.compute_approx_normals()
        dot_product = np.dot(normal_vectors, [0, 0, -1])
        angle = np.arccos(dot_product)
        return angle

    def face_color_values(self, angles):
        """returns the shader color value for each triangle based on its angle from the z-axis"""
        col_values = (angles / (np.pi / 2)) * 256
        return col_values

    def object_centroid(self):
        """returns centroid of the entire object"""
        return np.mean(self.vertices, axis=0)

    def triangle_centroid(self):
        """returns centroid of each triangle surface"""
        return np.mean(self.vertices[self.triangles], axis=1)

    def compute_approx_normals(self):
        """returns the normals to the triangle surfaces as the normalized vector from the object
        centroid to the triangle centroid"""
        centroid = self.object_centroid()
        # print(centroid)
        triangle_centroids = self.triangle_centroid()

        surface_normals = triangle_centroids - centroid
        normalizing_constant = np.linalg.norm(triangle_centroids - centroid)
        return surface_normals / normalizing_constant


class InteractiveWindow(p1.InteractiveWindow):

    def update_plot(self):
        """Update plot after rotation"""
        # clear previous plot from window
        self.ax.clear()

        v = self.obj.vertices

        angles = self.obj.angle_from_z()
        colors = self.obj.face_color_values(angles)

        # mask out triangles that are more than 90 degrees from the z-axis(at the back of the object)
        triangle_mask = np.where(angles <= (np.pi / 2), True, False)

        # plot the new object
        triang = mtri.Triangulation(
            v[:, 0], v[:, 1], triangles=self.obj.triangles, mask=triangle_mask
        )
        ax.tripcolor(triang, cmap=newcmp, facecolors=colors, shading="flat")

        self.ax.set_xlim(-self.ax_lim, self.ax_lim)
        self.ax.set_ylim(-self.ax_lim, self.ax_lim)

        self.fig.canvas.draw()


def create_colormap():
    """creates and returns the colormap for the object shader"""
    color1 = to_rgb("#00005f")
    color2 = to_rgb("#0000ff")
    N = 256
    vals = np.ones((N, 4))
    vals[:, 0] = np.linspace(color1[0], color2[0], N)
    vals[:, 1] = np.linspace(color1[1], color2[1], N)
    vals[:, 2] = np.linspace(color1[2], color2[2], N)
    return ListedColormap(vals)


if __name__ == "__main__":

    # CLI argument parser to get filepath with object data
    parser = argparse.ArgumentParser(
        description="Process file name", allow_abbrev=False
    )
    parser.add_argument(
        "filepath", metavar="Filepath", type=str, help="file path for object file"
    )

    args = parser.parse_args()

    # get vertices and faces from the file
    vertices, faces, vertex_index_mapping = read_file(args.filepath)

    # calculate axis limit for window size
    axis_lim = np.absolute(vertices).max() * 1.5

    newcmp = create_colormap()

    obj = Object_3D_solid(vertices, faces, vertex_index_mapping)
    angles = obj.angle_from_z()
    triangle_mask = np.where(angles <= (np.pi / 2), True, False)

    fig, ax = plt.subplots(figsize=(10, 8))

    iw = InteractiveWindow(obj, ax, fig, axis_lim)
    iw.connect()

    plt.xlim([-axis_lim, axis_lim])
    plt.ylim([-axis_lim, axis_lim])
    plt.show()
