# 2017-Nov-07 18:07
# WNixalo
# HPFEM01.1x - High Performace Finite Element Modeling - FEniCS tutorials
# https://fenicsproject.org/pub/tutorial/sphinx1/._ftut1003.html

# from fenics import *
from dolfin import *
import numpy as np

parameters['plotting_backend'] == 'matplotlib'
# parameters['plotting_backend'] == 'x3dom'
# import matplotlib.pyplot as plt

# Create mesh and define the function space
mesh = UnitSquareMesh(8, 8)
V = FunctionSpace(mesh, 'P', 1)

# Define boundary condition
u_D = Expression('1 + x[0]*x[0] + 2*x[1]*x[1]', degree=2)

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary)

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(-6.0)
a = dot(grad(u), grad(v))*dx
L = f*v*dx

# Compute solution
u = Function(V)
solve(a == L, u, bc)

# Plot solution and mesh
plot(u, title='Finite Element Solution')
plot(mesh, title='Finite Element Mesh')


# Save soltuion to file in VTK format
vtkfile = File('poisson/solution.pvd')
vtkfile << u

# Compute error in L2 norm
error_L2 = errornorm(u_D, u, 'L2')

# Compute maximum error at vertices
vertex_values_u_D = u_D.compute_vertex_values(mesh)
vertex_values_u   = u.compute_vertex_values(mesh)
error_max = np.max(np.abs(vertex_values_u_D - vertex_values_u))

# Print errors
print('error_L2  =', error_L2)
print('error_max =', error_max)

# Hold plot
interactive()