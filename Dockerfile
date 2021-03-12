FROM continuumio/miniconda3

# For Slackbot Dockerfile

PWD

ENV APP_HOME /app

PWD

ENTRYPOINT []
CMD [ "/bin/bash" ]

PWD

# RUN conda config --add channels http://conda.anaconda.org/gurobi
# RUN conda install gurobi
# RUN conda install -y pandas numpy matplotlib 
# RUN pip install Pillow
# RUN pip install unidecode
# RUN pip install flask

CD

PWD

CMD python api.py
