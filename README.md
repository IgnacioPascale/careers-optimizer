
# FIFACareers Optimizer

Finding the right people for your FIFA team can be a tall order. Especially when working with limited budgets. In the following documents, we try to devise the ultimate FIFA team using linear programming. 

The dataset used contains data from FIFA19 players. It was originally scrapped from sofifa and cleaned by us in the document `data-cleaning_careers-optimizer_SG15.ipynb.ipynb`. The original dataset can be found in this [kaggle link.](https://www.kaggle.com/karangadiya/fifa19)

![](https://i.ytimg.com/vi/x9HAml8kOCs/maxresdefault.jpg)

# Academic Purposes

This is an academic project to use linear and integer programming. We do not intend to make any profit whatsoever through the use of this project.

# Jupyter Notebooks and Data

The Data used for this project was taken from [kaggle](https://www.kaggle.com/karangadiya/fifa19). This data was previously scrapped from [sofifa](https://sofifa.com/). In the data cleaning, the column "photo" was taken from the dataset of FIFA 21 from [kaggle](https://www.kaggle.com/bryanb/fifa-player-stats-database)

The jupyter notebooks are not uploaded in this repository as they are confidential and part of an ongoing academic submission.

# Deployment and Architecture

The front end is developed on `vue.js` and `css`. It's in the folder `app_vue`. This was deployed using `surge` and it can be found in the [following link](http://fifacareers-optimizer.surge.sh/)

We can find the API and back end in the folder `api`. However, in order for the front-end  to work, the API will have to run locally. We previously tried deploying the API to heroku using dockerfile. The problem is that in order to use GUROBI optimization one would need a license in their local computer. Since this is an academic project, we are working on it using a free student academic license. Unfortunately, this license **cannot** be used in a different computer, hence making deployment of the API Flask and back end more difficult.

![](https://i.ibb.co/pQcvBsp/Screenshot-2021-03-12-at-16-33-32.png)

# Setting up virtual environment

You may need to set up a virtual environment if you don't have the correct dependencies. These dependencies are specified in `environment.yml` and `requirements.txt` in the `api` folder. The steps are as follows:

First go to the api directory

```
cd ./api
```

Create a conda environment by running the following. This will install the dependencies specified in `environment.yml`.

```
create conda env
```

*This environment will also install `pip` as we will need it for one of flasks dependencies.*

Once this is done, activate the environment:

```
conda activate condaenv2
```

*condaenv2 is the name specified in `environment.yml`*

Install `flask_restful`

```
pip install flask_restful
```

Now run the API

```
python api.py
```

If you want to use the app, go to the website:

http://fifacareers-optimizer.surge.sh/

# Troubleshooting

A possible issue is that, since the “api.py” runs subprocesses using “python”, if the user runs python files doing “python3” the api would not work. In this case, this should be changed from the api.py file.



