# __author__: Ashlyn DSouza (ashlynselena@gmail.com)


import argparse
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos
import matplotlib.tri as mtri

class Object_3D:
    '''Class of the 3D object'''

    def __init__(self, vertices, faces, vertex_index_mapping):
        self.vertices = vertices
        self.triangles = np.empty((faces.shape[0],3), dtype="int")
        for i, face in enumerate(faces):
            self.triangles[i] = [vertex_index_mapping[face[0]],vertex_index_mapping[face[1]],vertex_index_mapping[face[2]]]
    def rotate(self, rx, ry):
        '''
        Arguments:
            rx: angle of rotation around x axis(in radians)
            ry: angle of rotation around y-axis(in radians)
        Returns:
            new vertex positions and faces of the object after rotating in both x and y directions
        '''
        self.rotate_x(rx)
        self.rotate_y(ry)
        return self.vertices

    def rotate_x(self, rx):
        '''
            Arguments:
                rx: angle of rotation around x axis(in radians)
            
            Updates vertex positions after rotating around x-axis using rotation matrix
        '''
        #Rx is the rotation matrix around the x-axis
        Rx = np.array([[1,0,0],[0,cos(rx), -sin(rx)],[0,sin(rx),cos(rx)]])
        self.vertices = np.matmul(self.vertices, Rx.T)

    def rotate_y(self, ry):
        '''
            Arguments:
                ry: angle of rotation around y axis(in radians)
            
            Updates vertex positions after rotating around y-axis using rotation matrix
        '''
        #Ry is the rotation matrix around the y-axis
        Ry = np.array([[cos(ry),0,sin(ry)],[0,1,0],[-sin(ry), 0, cos(ry)]])
        self.vertices = np.matmul(self.vertices, Ry.T)



#source: https://matplotlib.org/stable/users/explain/event_handling.html
class InteractiveWindow:
    '''class to detect and process mouse events'''
    def __init__(self, obj, ax, fig, ax_lim):
        self.press = None
        self.obj = obj
        self.ax = ax
        self.fig = fig
        self.ax_lim = ax_lim

        #initialize object plot
        self.update_plot()

    def connect(self):
        '''connect to mouse press, move and release events'''
        self.cidpress = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        '''on mouse press, set self.press to mouse location'''

        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata

    def on_motion(self, event):
        ''' When mouse is moved while being pressed, update the plot'''

        #if mouse is not pressed or is outside the window bounds
        if self.press is None or event.inaxes != self.ax:
            return

        #change in x and y axis is the difference of mouse coordinates when pressed and after moving
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        self.press = event.xdata, event.ydata

        #angles of rotation around x and y axes based on the change in mouse location
        rx = (-dy) * np.pi/6
        ry = (dx) * np.pi/6

        #rotate the object
        self.obj.rotate(rx,ry)

        self.update_plot()

    def update_plot(self):
        '''Update plot after rotation'''
        #clear previous plot from window
        self.ax.clear()
        v = self.obj.vertices

        #plot the faces of the object
        triang = mtri.Triangulation(v[:,0], v[:,1], triangles=self.obj.triangles)
        triangles = self.ax.triplot(triang, color="blue", marker="o")[0]

        self.ax.set_xlim(-self.ax_lim,self.ax_lim)
        self.ax.set_ylim(-self.ax_lim,self.ax_lim)

        self.fig.canvas.draw()

    def on_release(self, event):
        '''clear self.press when mouse is released'''
        self.press = None
        self.fig.canvas.draw()

    def disconnect(self):
        """Disconnect all callbacks."""
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidmotion)



def read_file(filename):
    ''' reads and parses the object file and returns the vertices and faces'''
    f = open(filename)
    num_vertices, num_faces = f.readline().split(",")
    vertex_index_mapping = {}
    vertices = []
    faces = []

    for i in range(int(num_vertices)):
        v = f.readline().strip().split(",")
        vertices.append([float(v[1]),float(v[2]),float(v[3])])
        vertex_index_mapping[int(v[0])] = i

    for i in range(int(num_faces)):
        face = f.readline().strip().split(",")
        faces.append(face)

    vertices = np.array(vertices)
    faces = np.array(faces, dtype="int")
    return vertices, faces, vertex_index_mapping


if __name__ == "__main__":

    #CLI argument parser to get filepath with object data
    parser = argparse.ArgumentParser(
        description="Process file name", allow_abbrev=False
    )
    parser.add_argument(
        'filepath', metavar='Filepath', type=str,
                    help='file path for object file')

    args = parser.parse_args()  

    vertices, faces, vertex_index_mapping = read_file(args.filepath)

    axis_lim = np.absolute(vertices).max()*1.5

    #create instance of object 3d
    obj  = Object_3D(vertices, faces, vertex_index_mapping)

    fig, ax = plt.subplots(figsize=(10, 8))

    iw = InteractiveWindow(obj, ax, fig, axis_lim)
    iw.connect()

    plt.xlim([-axis_lim, axis_lim])
    plt.ylim([-axis_lim, axis_lim])
    plt.show()


