__author__: Ashlyn DSouza (ashlynselena@gmail.com)


# READ ME

## Requirements:  
* numpy  
* matplotlib

## File Contents:  
1. Assignment_part1.py
2. Assignment_part2.py
3. object.txt

To run code,  
1. Extract code to a folder.  
2. To view wireframe object, run "python assigment_part1.py <path to txt file containing 3D object description>"  
3. To view shaded object, run "python assignment_part2.py <path to txt file containing 3D object description>".


## Detailed function description by file.
### 1. assignment_part1.py
	
	**Overview:** To display the wireframe of a 3D object described by the passed file and rotate it around the x and y axes 
			by clicking and dragging the mouse
		
		function read_file(filename)

			parameters:
				filename: path to text file containing 3D object description in following format
					Number of vertices, Number of Triangles
					Vertex a, x_coord, y_coord, z_coord
					Vertex b, x_coord, y_coord, z_coord
					Vertex c, x_cord, y_coord, z__cord
					Vertex d, x_coord, y_coord, z_coord 
					Edge connections of form: Vertex a, Vertex b, Vertex c
					Vertex a, Vertex c, Vertex d 

			return:
				vertices: numpy array containing vertices

				faces: numpy array containing faces

				vertex_index_mapping: mapping from vertex ID to index in the array

		class Object_3D
			# class which holds the 3D object.
			end_user_facing:
				
				function rotate(rx, ry)
					parameters:
						rx: Angle of rotation along x-axis
						ry: Angle of rotation along y-axis

					return:
						vertices: updated coordinates of vertices after rotation

					Algorithm:
						1) Create Rotation matrix Rx for x axis based on input angle of rotation
						2) vertices <- vertices x Rx.T
						3) Create Rotation matrix Ry for y axis based on input angle of rotation
						4) vertices <- vertices x Ry.T

			helper functions:
				
				function rotate_x(rx)
				function rotate_y(ry)


		class InterativeWindow:
			# class to detect and process mouse events

			helper functions:
				function on_press(event)
					# Detects mouse button press.
					# Initializes x and y coordinates of mouse in Interactive Window 

				function on_motion(event)
					# Computes delta change from previous mouse position before mouse button press
					# Computes corresponding angle rotation with respect to change in mouse coordinates.
					# Calls Rotate function in Object3D class to apply rotation.

				function on_release(event)
					# Clears x and y coordinates of mouse from memory

				function update_plot()
					# plots updated object based on mouse movement using matplotlib.pyplot.triplot to plot edges of each triangle


### 2. assignment_part2.py

		**Overview:** To display a solid 3D object described by the passed file and rotate it around the x and y axes 
			by clicking and dragging the mouse. The color of each surface is determined by its angle to the z-axis.

		class Object_3D_solid
		# inherits Object_3D class from part1.
			end_user_facing:

				function normalize_array(arr)
					parameters:
						arr: input array to normalize
					return:
						norm_array: unit normalized array


				function angle_from_z()
					# Computes angle from z axis of each surface using dot product formula.

				function face_color_values(angle)
					# return the shader color value for each triangle based on angle from z axis. 
					#This is done through simple unitary method for angle range from 0 to pi/2.
					parameters: 
						angles: array angles of each triangle from z axis.

					return:
						col_values: Shader color value of each triangle based on its angle from z axis.

				function triangle_centroid()
					# returns the centroid of each triangle.
					# computes the mean of the coordinates of the vertices of each triangle.

				function object_centroid()
					# returns centroid of entire 3D object
					# computes mean coordinate of all vertices.

				function compute_normals()
					# returns approximate normal vector to each triangle surface of the object
					# Algorithm: 
						Computer vector from centroid of object to centroid of triangle.
						return normalized vector	
					### Limitation: Since only approximate vectors are calculated, sometimes triangles are masked
						before they go out of view

		class InteractiveWindow
		#inherits InteractiveWindow from part1.
			helper functions
				update_plot()
					# calculates angles of each surface from z axis.
					# surfaces with angles greater than 90 degrees are masked to hide from view.
					# plots updates object based on mouse movement using matplotlib.pyplot.tripcolor to color in
						each triangle surface based on its angle from the z-axis

References:
https://learning.oreilly.com/library/view/python-graphics-a/9781484233788/html/456962_1_En_7_Chapter.xhtml
https://matplotlib.org/stable/users/explain/event_handling.html






