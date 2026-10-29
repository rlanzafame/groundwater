#!/usr/bin/env python
"""Plot steady-state groundwater flow and capture zones for multiple wells."""

from math import cos, pi, radians, sin

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py
from matplotlib.backends.backend_pdf import PdfPages


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a valid number.")


def read_pair(prompt):
    while True:
        try:
            values = [float(value.strip()) for value in input(prompt).split(",")]
            if len(values) != 2:
                raise ValueError
            return values
        except ValueError:
            print("Enter exactly two comma-separated numbers.")


def main():
    print("Well Superposition - Zone of Capture")
    print("By N. Sitar, UC Berkeley, 09/2022")
    print("Use consistent units: time in seconds or days, and length in m or ft.\n")

    xmin, xmax = read_pair("Enter Xmin, Xmax: ")
    while xmax <= xmin:
        print("Xmax must be greater than Xmin.")
        xmin, xmax = read_pair("Enter Xmin, Xmax: ")

    ymin, ymax = read_pair("Enter Ymin, Ymax: ")
    while ymax <= ymin:
        print("Ymax must be greater than Ymin.")
        ymin, ymax = read_pair("Enter Ymin, Ymax: ")

    transmissivity = read_float("Transmissivity - T [L^2/T]: ")
    while transmissivity <= 0:
        print("Transmissivity must be greater than zero.")
        transmissivity = read_float("Transmissivity - T [L^2/T]: ")

    gradient, azimuth_degrees = read_pair(
        "Regional gradient [dimensionless], azimuth from x [degrees]: "
    )
    azimuth = radians(azimuth_degrees)

    while True:
        try:
            number_of_wells = int(input("Number of wells (positive integer): "))
            if number_of_wells < 1:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive integer.")

    pumping_rates = []
    well_x = []
    well_y = []
    for index in range(number_of_wells):
        print(f"Well {index + 1}:")
        pumping_rates.append(read_float("  Pumping rate Q [L^3/T]: "))
        well_x.append(read_float("  X-coordinate [L]: "))
        well_y.append(read_float("  Y-coordinate [L]: "))

    x = np.arange(xmin, xmax, (xmax - xmin) / 75.0)
    y = np.arange(ymin, ymax, (ymax - ymin) / 75.0)
    X, Y = np.meshgrid(x, y)

    drawdown = np.zeros_like(X, dtype=float)
    ux = np.zeros_like(X, dtype=float)
    uy = np.zeros_like(Y, dtype=float)

    for rate, x_well, y_well in zip(pumping_rates, well_x, well_y):
        dx = X - x_well
        dy = Y - y_well
        radius_squared = dx**2 + dy**2
        with np.errstate(divide="ignore", invalid="ignore"):
            drawdown += (rate / (2 * pi * transmissivity)) * np.log(
                np.sqrt(radius_squared)
            )
            ux -= (rate / (2 * pi * transmissivity)) * dx / radius_squared
            uy -= (rate / (2 * pi * transmissivity)) * dy / radius_squared

    drawdown -= gradient * (X * cos(azimuth) + Y * sin(azimuth))
    ux += gradient * cos(azimuth)
    uy += gradient * sin(azimuth)

    width = 10.0
    height = (ymax - ymin) / (xmax - xmin) * width
    figure, axes = plt.subplots(figsize=(width, height))
    axes.set_xlabel("x", fontsize=16)
    axes.set_ylabel("y", fontsize=16)
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.streamplot(x, y, ux, uy, density=1, linewidth=1, arrowsize=2, arrowstyle="->")
    axes.scatter(well_x, well_y, color="#CD2305", s=80, marker="o")
    axes.contour(X, Y, drawdown, 15)
    axes.set_title(
        "Zone of Capture, Number of Wells = {}, Gradient = {}, Azimuth = {}".format(
            number_of_wells, gradient, azimuth_degrees
        )
    )
    figure.savefig("Zone of Capture.jpg")
    with PdfPages("Zone of Capture.pdf") as pdf:
        pdf.savefig(figure)

    plot_3d = go.Figure(
        go.Surface(
            x=x,
            y=y,
            z=drawdown,
            contours={
                "z": {
                    "show": True,
                    "highlight": True,
                    "color": "white",
                    "highlightcolor": "limegreen",
                }
            },
        )
    )
    plot_3d.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Drawdown",
        ),
        margin=dict(r=20, b=10, l=10, t=10),
    )
    py.plot(plot_3d, filename="Contour.html", auto_open=False)

    print("\nCreated Zone of Capture.jpg, Zone of Capture.pdf, and Contour.html.")
    plt.show()
    plot_3d.show()
    plt.close(figure)


if __name__ == "__main__":
    main()
