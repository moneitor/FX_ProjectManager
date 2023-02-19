node = hou.pwd()
geo = node.geometry()

import numpy

matrix = geo.pointFloatAttribValues('__invInertiaTensor')

matrixA = [matrix[0], matrix[1], matrix[2]]
matrixB = [matrix[3], matrix[4], matrix[5]]
matrixC = [matrix[6], matrix[7], matrix[8]]

a = numpy.array([matrixA, matrixB , matrixC])
w,v = numpy.linalg.eig(a)

# The eigenvectors are the columns of the matrix stored on "v"
eigenvec1 = v[:,0]
eigenvec2 = v[:,1]
eigenvec3 = v[:,2]

geo.addAttrib(hou.attribType.Point, "eigen1", eigenvec1)
geo.addAttrib(hou.attribType.Point, "eigen2" , eigenvec2)
geo.addAttrib(hou.attribType.Point, "eigen3" , eigenvec3)

