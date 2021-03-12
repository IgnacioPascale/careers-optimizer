FROM continuumio/miniconda3

# For Slackbot Dockerfile

ENTRYPOINT []

# Remove (large file sizes) MKL optimizations.
RUN conda config --add channels http://conda.anaconda.org/gurobi
RUN conda install gurobi
RUN conda install -y pandas numpy matplotlib 
RUN pip install Pillow
RUN pip install unidecode
RUN pip install flask

ENTRYPOINT ["python api.py"]
