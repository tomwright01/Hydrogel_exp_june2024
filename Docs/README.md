# Data and analysis scripts for Hydrogel ERG experiment.

Data is stored as espion export files. Python scripts require [espion_tools package V0.0.6](https://pypi.org/project/espion-tools/).
`pip install espion_tools`.

## Files

- [**extract_markers.py**](../extract_markers.py) Python script to extract maker data (a-wave, b-wave etc.) from export files. 
- [**plot_all.py**](../plot_all.py) Python script to read trace and plot data from espion export files. Output files are named __subject_____timepoint_____step_____eye__.png
- [**marker_analysis.Rmd**](../marker_analysis.Rmd) [R](https://www.r-project.org) scripts for statistical analysis of experiment data.

- [**Presentation1.pptx**](Presentation1.pptx) Powerpoint presentation with selected ERG trace data and statistical analysis.

- [**transfer_instructions.jpg**](transfer_instructions.jpg) Instructions for creating a data transfer file, from the espion user manual.