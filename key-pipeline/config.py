import sys
import os

os.system('wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh')
os.system('bash Miniconda3-latest-Linux-x86_64.sh')
os.system('conda env create -f environment.yml')


