FROM continuumio/miniconda3

# For Slackbot Dockerfile

echo %CD%

ENV APP_HOME /app

echo %CD%

ENTRYPOINT []
CMD [ "/bin/bash" ]

echo %CD%

# RUN conda config --add channels http://conda.anaconda.org/gurobi
# RUN conda install gurobi
# RUN conda install -y pandas numpy matplotlib 
# RUN pip install Pillow
# RUN pip install unidecode
# RUN pip install flask


CMD python api.py
