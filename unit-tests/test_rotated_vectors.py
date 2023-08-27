"""
Test the formulae for rotating spherical vectors.
"""
import numpy as np
from gusto.coord_transforms import *

tol = 1e-12


def test_rotated_lonlatr_vectors_firedrake():

    from firedrake import (CubedSphereMesh, pi, SpatialCoordinate, Function,
                           VectorFunctionSpace, as_vector, grad, sqrt, dot)

    new_pole = (pi/4, pi/4)

    radius = 10.0
    mesh = CubedSphereMesh(radius)

    xyz = SpatialCoordinate(mesh)

    rot_axis, rot_angle = pole_rotation(new_pole)
    new_xyz = rodrigues_rotation(xyz, as_vector(rot_axis), rot_angle)

    new_lonlatr = lonlatr_from_xyz(new_xyz[0], new_xyz[1], new_xyz[2])

    answer_e_lon = grad(new_lonlatr[0])
    answer_e_lat = grad(new_lonlatr[1])
    answer_e_r = grad(sqrt(dot(xyz, xyz)))

    new_e_lon, new_e_lat, new_e_r = rotated_lonlatr_vectors(xyz, new_pole)

    # Check answers
    V = VectorFunctionSpace(mesh, "CG", 1)

    for new_vector, answer_vector, component in zip([new_e_lon, new_e_lat, new_e_r],
                                                    [answer_e_lon, answer_e_lat, answer_e_r],
                                                    ['lon', 'lat', 'r']):

        new_field = Function(V).interpolate(new_vector)
        answer_field = Function(V).interpolate(as_vector(answer_vector))

        assert np.allclose(new_field.dat.data, answer_field.dat.data), \
            f'Incorrect answer for firedrake rotated {component} vector'
