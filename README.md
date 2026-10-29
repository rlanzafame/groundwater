# Groundwater Demonstration Book

Created by Nick Sitar to experiment with TeachBooks and share code for groundwater applications.

## Building the Book Locally for Editing

Robert Lanzafame is building the book locally using `teachbooks` in a terminal with a conda environment using Python 3.14 and packages added to `requirements.txt`. For example:
- `conda create -n <name> python=3.14`
- `conda activate <name>`
- `pip install -r requirements.txt`
- `teachbooks build book`
- `teachbooks serve`