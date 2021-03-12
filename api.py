import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
import subprocess
from main import protocol
import re
import sys
import json
import unidecode

app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()

# First model
parser.add_argument("budget")
parser.add_argument("budget_wage")
#parser.add_argument("players")
parser.add_argument("gk")
parser.add_argument("defs")
parser.add_argument("mid")
parser.add_argument("att")
parser.add_argument("max_age")

# Second model
parser.add_argument("max_overall")

# Stats
parser.add_argument("playerid")

# Formation
parser.add_argument("team")

@app.route('/')
class Overall(Resource):
        
    def post(self):
        args = parser.parse_args()

        ret =  subprocess.check_output("python3 main.py overall --budget {0} --budget_wage {1}  --gk {2} --defs {3} --mid {4} --att {5} --max_age {6}".format(
            args["budget"],
            args["budget_wage"],
            #args["players"],
            args["gk"],
            args["defs"],
            args["mid"],
            args["att"],
            args["max_age"]
        ), shell=True)

        #result = re.search("INIT>>>>>(.*)<<<<<END", ret).group(0)
        result =  re.findall(r'INIT>>>>>\\n(.*)\\n<<<<<END',str(ret))[0]
        
        # Solution
        solution = re.findall(r'SOL>>>>>>(.*)<<<<<<SOL', str(ret))[0]

        res = list(result.split(","))

        players = len(res)

        final_list = []
        for i in res[:int(players)-1]:#res[:10]:
            final_list.append(str(i)[1:])

        final_list.append(str(res[-1])[1:].rstrip(']'))

        return {"overall": final_list, "solution": solution}
        

api.add_resource(Overall, "/overall")


@app.route('/')
class Potential(Resource):
        
    def post(self):
        args = parser.parse_args()

        ret =  subprocess.check_output("python3 main.py potential --budget {0} --budget_wage {1}  --gk {2} --defs {3} --mid {4} --att {5} --max_age {6} --max_overall {7}".format(
            args["budget"],
            args["budget_wage"],
           # args["players"],
            args["gk"],
            args["defs"],
            args["mid"],
            args["att"],
            args["max_age"],
            args["max_overall"]
        ), shell=True)

        #result = re.search("INIT>>>>>(.*)<<<<<END", ret).group(0)
        result =  re.findall(r'INIT>>>>>\\n(.*)\\n<<<<<END',str(ret))[0]


        solution = re.findall(r'SOL>>>>>>(.*)<<<<<<SOL', str(ret))[0]

        res = list(result.split(","))
        players = len(res)


        final_list = []
        for i in res[:int(players)-1]:#res[:10]:
            final_list.append(str(i)[1:])

        final_list.append(str(res[-1])[1:].rstrip(']'))

        return {"overall": final_list, "solution": solution}

api.add_resource(Potential, "/potential")

@app.route("/")
class Stats(Resource):
    def post(self):
        args = parser.parse_args()

        console = subprocess.check_output("python3 main.py stats --playerid={0}".format(args["playerid"]), shell=True)

        re_console = re.findall(r'INIT>>>>>\\nb(.*)\\n<<<<<END', str(console))[0]

        image_code = re_console.lstrip("'").rstrip("'")

        return {"image":image_code}

api.add_resource(Stats, "/stats")



@app.route("/")
class Formation(Resource):
    def post(self):
        args = parser.parse_args()

        console = subprocess.check_output("python3 main.py formation --team={0} --defs={1} --mid={2} --att={3}".format(
            args["team"],
            args["defs"],
            args["mid"],
            args["att"]), shell=True)

        re_console = re.findall(r'INIT>>>>>\\nb(.*)\\n<<<<<END', str(console))[0]

        image_code = re_console.lstrip("'").rstrip("'")
        #print(console)

        return {"formation":image_code}

api.add_resource(Formation, "/formation")

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')