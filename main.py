import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

def plot_xrd_pattern(wavelength, lattice_constants_list, planes_list):
    fig = go.Figure()

    for i in range(len(lattice_constants_list)):
        lattice_constants = lattice_constants_list[i]
        planes = planes_list[i]

        a, b, c = lattice_constants
        alpha = 90
        beta = 90
        gamma = 90

        alpha_rad = math.radians(alpha)
        beta_rad = math.radians(beta)
        gamma_rad = math.radians(gamma)

        s11 = b**2 * c**2 * math.sin(alpha_rad)**2
        s22 = a**2 * c**2 * math.sin(beta_rad)**2
        s33 = a**2 * b**2 * math.sin(gamma_rad)**2
        s12 = a * b * c**2 * (math.cos(alpha_rad) * math.cos(beta_rad) - math.cos(gamma_rad))
        s23 = c * b * a**2 * (math.cos(beta_rad) * math.cos(gamma_rad) - math.cos(alpha_rad))
        s13 = a * c * b**2 * (math.cos(gamma_rad) * math.cos(alpha_rad) - math.cos(beta_rad))

        v = a * b * c * math.sqrt((1 - math.cos(alpha_rad)**2 - math.cos(beta_rad)**2 - math.cos(gamma_rad)**2 + 2 * math.cos(alpha_rad) * math.cos(beta_rad) * math.cos(gamma_rad)))
        d_values = []

        for plane, hkldata in planes.items():
            h, k, l = map(int, [x.split('=')[1] for x in hkldata.split(',')])
            numerator = s11 * h**2 + s22 * k**2 + s33 * l**2 + 2 * s12 * h * k + 2 * s23 * k * l + 2 * s13 * l * h
            d = v / math.sqrt(numerator)
            d_values.append(d)

        theta_values = []

        for d in d_values:
            theta = np.arcsin(wavelength / (2 * d))
            theta_degrees = np.degrees(2 * theta)
            theta_values.append(theta_degrees)

        x_coordinates = np.arange(90)
        y_coordinates = np.ones_like(x_coordinates)

        for theta in theta_values:
            index = int(theta)
            if index < len(y_coordinates):
                y_coordinates[index] = 5

        fig.add_trace(go.Scatter(x=x_coordinates, y=y_coordinates, mode='lines', name=f'XRD Pattern {i+1}'))

    fig.update_layout(title='XRD Patterns',
                      xaxis_title='2 theta',
                      yaxis_title='Intensity',
                      hovermode='closest')

    return fig

st.title('XRD Pattern Visualization')

wavelength = st.number_input('Wavelength', min_value=1.0, max_value=2.0, value=1.6, step=0.1)

bravais_lattices = ['Cubic', 'Tetragonal', 'Hexagonal', 'Orthorhombic', 'Rhombohedral', 'Monoclinic', 'Triclinic']
selected_lattice = st.selectbox('Select Bravais lattice', bravais_lattices)

num_patterns = st.number_input('Number of XRD Patterns', min_value=1, value=1, step=1)

lattice_constants_list = []
planes_list = []

for i in range(num_patterns):
    lattice_a = st.number_input(f'Lattice constant a (Pattern {i+1})', value=4.05, key=f'a_{i}')
    lattice_b = st.number_input(f'Lattice constant b (Pattern {i+1})', value=4.05, key=f'b_{i}')
    lattice_c = st.number_input(f'Lattice constant c (Pattern {i+1})', value=4.05, key=f'c_{i}')

    lattice_constants_list.append((lattice_a, lattice_b, lattice_c))

    planes = {}

    if selected_lattice == 'Cubic':
        planes = {
            '100': 'h=1,k=0,l=0',
            '110': 'h=1,k=1,l=0',
            '111': 'h=1,k=1,l=1',
            '200': 'h=2,k=0,l=0',
            '210': 'h=2,k=1,l=0'
        }
    elif selected_lattice == 'Tetragonal':
        planes = {
            '100': 'h=1,k=0,l=0',
            '110': 'h=1,k=1,l=0',
            '200': 'h=2,k=0,l=0',
            '210': 'h=2,k=1,l=0',
            '001': 'h=0,k=0,l=1'
        }

    planes_list.append(planes)

fig = plot_xrd_pattern(wavelength, lattice_constants_list, planes_list)
st.plotly_chart(fig, use_container_width=True)
