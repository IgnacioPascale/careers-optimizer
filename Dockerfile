FROM continuumio/miniconda3

# For Slackbot Dockerfile

ENTRYPOINT []
CMD [ "/bin/bash" ]

# Remove (large file sizes) MKL optimizations.
RUN conda install gurobipy
RUN conda install -y pandas numpy matplotlib 
RUN pip install unidecode subprocess flask flask_restful flask_cors argparse Pillow requests

ENTRYPOINT ["python api.py"]
