#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import librairies
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from dash.dependencies import Output, Input
import plotly 
import random 
import plotly.graph_objs as go 
from collections import deque 


# In[2]:


#Instanciation de l'odjet dash
app = dash.Dash(__name__)


# In[ ]:


# ============================= GRAPH 1 =============================


# In[60]:


#Import dataset
df = pd.read_csv("Nb_visites_tot-monuments.csv", sep=";")
df = np.array(df)
df


# In[62]:


#Preparation des données
valeurs = []
monuments = []
for i in range(0,6):
    valeurs.append(df[i][1])
    monuments.append(df[i][0])

data = pd.DataFrame({
    "Monuments": monuments,
    "Nombre de visites": valeurs,
    "Sites": ["Rome", "Rome", "Rome", "Venise", "Venise", "Venise"]
})

data
  


# In[77]:


#Présentation du nombre de visite total de chaque monument regroupé par sites
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.bar(data, x="Sites", y="Nombre de visites", color="Monuments", barmode="group") #typage du graphe

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Nombre de visites de chaque monument',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='Présentation du nombre de visite total de chaque monument regroupé par sites', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Nb_vistes_par_monument-sites',
        figure=fig
    )
])


#Sortie
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


# In[75]:


# ============================= GRAPH 2 =============================


# In[80]:


df


# In[85]:


df[0][1],df[1][1],df[2][1])


# In[89]:


#Preparation des données
valeurs = []
for i in range(0,6,3):
    valeurs.append(df[i][1]+df[i+1][1]+df[i+2][1])
    #print(df[i][1],df[i+1][1],df[i+2][1])

data = pd.DataFrame({
    "Nombre de visites": valeurs,
    "Sites": ["Rome", "Venise"]
})

data


# In[90]:


#Présentation du nombre de visite total de chaque sites
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.bar(data, x="Sites", y="Nombre de visites", color="Sites") #typage du graphe

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Nombre de visites de chaque site',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='Présentation du nombre de visites total pour chaque site', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Nb_vistes_par_site',
        figure=fig
    )
])


#Sortie
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


# In[ ]:


# ============================= GRAPH 3 =============================


# In[ ]:


#Présentation de la part de voyages Rome et Venise liés 
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig.update_traces() = px.pie(data, x="Sites", y="Nombre de visites", color="Sites") #typage du graphe

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Nombre de visites de chaque site',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='Présentation du nombre de visites total pour chaque site', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Nb_vistes_par_site',
        figure=fig
    )
])


#Sortie
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

