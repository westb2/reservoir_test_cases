This repo contains contains test cases for the implementation of reservoirs in ParFlow. It is currently underconstruction to add documentation and to make it possible to run more of the test cases without needing to download a prohibitvely large amount of files. Check back in a couple weeks if you want to use it.

This repo contains the idealized and performance test cases for [this paper](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-965/).

Build instructions:

First you must have a working copy of Parflow installed recently enough to have reservoirs. You can check by looking at the copy of the manual you have to see if reservoir keys exist if you are not sure.
You also need python, and [conda](https://www.anaconda.com/download/).

To download the python packages you need open a terminal and navigate into the reservoir_test_cases folder.

Then, create and activate a conda environment

'''conda env create -f environment.yml && activate parflow_reservoir_test_cases'''

Lastly, you need a place to run a jupyter notebook. When running the notebooks, you will need to select the conda environment you just made when it asks you to select an interpreter.

Once you have this each folder in the test cases folder contains a figures.ipynb file that you can use to run the simulations and generate the figures.
For the performance test case, there is an additional file run_ensemble.py you need to run first. 



