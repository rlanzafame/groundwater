# Groundwater Demonstration Book

Created by Nick Sitar to experiment with TeachBooks and share code for groundwater applications.

## Building the Book Locally for Editing

Robert Lanzafame is building the book locally using `teachbooks` in a terminal with a conda environment using Python 3.14 and packages added to `requirements.txt`. For example:
- `conda create -n <name> python=3.14`
- `conda activate <name>`
- `pip install -r requirements.txt`
- `teachbooks build book`
- `teachbooks serve`

## Zone of Caputure Notebook

_Written by GitHub Copilot, summarizing modifications to run Zone of Capture analysis in both browser and local Jupyter environments._

- The Sphinx-Thebe kernel runs in Pyodide. NumPy and Matplotlib are available there; Plotly is installed by the live notebook with `micropip` and requires network access.
- Files written by `savefig`, `PdfPages`, or Plotly's offline exporter stay in the browser's temporary filesystem and are not automatically downloaded.
- The live Plotly view loads JavaScript from a CDN, so it may not render in a static build or offline session.
- Use [the browser notebook](book/Zone_of_Capture_Analysis/03-Zone_of_Capture_-_Steady_State_-_Contours.ipynb) for inline live plots, and [the local notebook](book/Zone_of_Capture_Analysis/03-Zone_of_Capture_-_Steady_State_-_Contours_Local.ipynb) in desktop Jupyter for JPG, PDF, and HTML exports.

### Standalone Python Script

[zone_of_capture_steady_state.py](book/Zone_of_Capture_Analysis/zone_of_capture_steady_state.py) runs the same analysis from a terminal, prompting for model settings and well data. It supports any number of wells and creates JPG, PDF, and interactive HTML plots. From its directory, run `python zone_of_capture_steady_state.py` in an environment with NumPy, Matplotlib, and Plotly installed.

#### Changes

This is a list of the lines of code in the py file that were changed, relative to the notebook:
- Line 1: `#!/usr/bin/env python` and line 2's module docstring identify the file as a standalone script.
- Line 13: `def read_float(prompt):` and line 21: `def read_pair(prompt):` add reusable, validated terminal input helpers; the notebook instead specifies values in its input cell.
- Line 32: `def main():` wraps the analysis in a callable entry point. Lines 37, 43, 47, and 52 prompt for model settings; line 59 reads the well count; lines 69-73 collect each well. These replace the notebook's fixed input-variable cell and add range/transmissivity validation.
- Line 79: `drawdown = np.zeros_like(X, dtype=float)` renames the notebook's `S`; line 83 iterates over separate well-coordinate/rate lists with `zip`, and line 87 uses `np.errstate` around the well calculations.
- Line 106: `axes.scatter(well_x, well_y, ...)` plots the prepared coordinate lists directly instead of building lists from `wells` in the plotting call.
- Line 148: `if __name__ == "__main__":` starts `main()` only when the file is run as a script.
- The notebook's inward tick-direction settings and extra Plotly x/y axis-title update are omitted; the JPG, PDF, and HTML exports and core drawdown/velocity equations are otherwise retained.