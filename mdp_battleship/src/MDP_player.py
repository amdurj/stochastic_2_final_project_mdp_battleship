# Script used to pull in R MDP toolbox and use MDP as a battleship solver program. 
# This first script will be act as the solving player (the machine).
# Final script will have a function to be run by the MDP player. 

# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# These will let us use R packages:
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Convert pandas.DataFrames to R dataframes automatically.
pandas2ri.activate()

# R package
MDPtoolbox = importr("MDPtoolbox")

# Set plotting theme:
primary = "#404040"
accent = "#24B8A0"
pal = sns.color_palette([primary, accent])
style = {
    "axes.edgecolor": primary,
    "axes.labelcolor": primary,
    "text.color": primary,
    "xtick.color": primary,
    "ytick.color": primary,
}

sns.set_palette(pal)
sns.set_context("talk")
sns.set_style("ticks", style)