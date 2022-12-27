# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import des librairies utiles a l'application
import pandas as pd
import numpy as np
from color import colors_site, colors_monuments,colors,colors_avant_pendant,colors_et_ou, colors_monuments_rome, colors_monuments_venise
import plotly.express as px
import plotly 
import random 
import plotly.graph_objs as go 
from collections import deque 
import json
from flask import Flask,render_template
import psycopg2

#instanciation Flask
app = Flask(__name__)


#premiere page : racine
@app.route('/')
def index():
    return render_template("acces.html")


#page d'accueil

#lancement de l'instance Flask
if __name__ == "__main__":
    app.run(debug=True)
