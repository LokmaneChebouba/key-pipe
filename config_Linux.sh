#!/bin/bash

# Install Miniconda (including Python 3) and setup the pip-env environment for the pipeline
# GNU/Linux version

# Download Miniconda
command -v conda >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1 || {
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh
  source ~/.bashrc
}

# Create environment
cd key-pipeline
conda env create -f environment.yml

