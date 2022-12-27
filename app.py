# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import des librairies utiles a l'application
import pandas as pd
import numpy as np
# from color import colors_site, colors_monuments,colors,colors_avant_pendant,colors_et_ou, colors_monuments_rome, colors_monuments_venise
import plotly.express as px
import plotly 
import random 
import plotly.graph_objs as go 
from collections import deque 
import json
from flask import Flask,render_template
import psycopg2






colors_site={
    'Rome': '#14ca1c', #vert
    'rome' : '#14ca1c',
    'Venise': '#ca1414' ,#rouge
    'venise': '#ca1414' #rouge
} 

colors_avant_pendant={
    'Avant': '#14ca1c', #vert
    'Pendant': '#ca1414' #rouge
} 

colors_et_ou={
    'Personnes ayant visité Rome et Venise au cours du même voyage': '#14ca1c', #vert
    'Personnes n\'ayant pas visité Rome et Venise au cours du même voyage': '#ca1414' #rouge
} 

#1a8e93
# colors_monuments={'fontaine_de_trevi': '#e91e63', 
#                   'colisee': '#ffc107',
#                   'pantheon' : '#e80004',
#                   'piazza_san_marco' : '#00bcd4',
#                   'pont_du_raltio':'#2b61fb',
#                   'doges': '#7bca51'}

colors_monuments={
    'Fontaine de Trévi': '#2dd42a', 
    'Colisée': '#77bd76',
    'Panthéon' : '#b3faae',
    
    'Place Saint-Marc' : '#ff3e3e',
    'Pont du Rialto':'#d67b7c',
    'Palais des Doges': '#faaeaf'
}

colors_monuments_rome={
    'Fontaine de Trévi': '#2dd42a', 
    'Fontaine de Trevi': '#2dd42a', 
    'Colisée': '#77bd76',
    'Panthéon' : '#b3faae'
}


colors_monuments_venise={
    
    'Place Saint-Marc' : '#ff3e3e',
    'Pont du Rialto':'#d67b7c',
    'Palais des Doges': '#faaeaf'
}

colors = {
    'background': '#343a40',
    'text': '#cbfaf5'
}


#instanciation Flask
app = Flask(__name__)

#premiere page : racine
#page d'accueil
@app.route('/')
def accueil():
    description = """
        Bienvenue !
        visualisez l'impact du covid19 sur le toursime italien
        """
    #retour de la fonction
    return render_template('accueil.html',
                           description = description)


#page a propos
@app.route('/about/')
def about(): 
    #retour de la fonction 
    return render_template('about.html')

#page de graphiques 1 : description
@app.route('/desc/')
def graphd():
    
    #connection a la base de donnees
    #recuperations des donnees utiles a l'affichage des graphiques d ela page
# =============================================================================
#     try:
#         conn = psycopg2.connect(
#               user = "m101",
#               password = "1999",
#               host = "db-etu.univ-lyon2.fr",
#               port = "5432",
#               database = "m101"
#         )
#         cur = conn.cursor()
#         sql = "SELECT * FROM Nb_visites_tot_monuments"
#         
#         cur5 = conn.cursor()
#         sql5 = "select * from liens_Venise_Rome"
#         cur.execute(sql)
#         res = cur.fetchall()
#         cur5.execute(sql5)
#         res5 = cur5.fetchall() 
#         
#         
#         cur5.close()
#         cur.close()
#         conn.close()
#     except (Exception, psycopg2.Error) as error :
#         print ("Erreur lors de la connexion à PostgreSQL", error)
# =============================================================================

    res =pd.read_csv("Nb_visites_tot-monuments.csv", sep=";")
    res = np.array(res)
    
    res5 =pd.read_csv("liens_Venise_Rome.csv", sep=";")
    res5 = np.array(res5)
    
    #graphique nb_vis_site
    valeurs1 = []
    for i in range(0,6,3):
        valeurs1.append(int(res[i][1])+int(res[i+1][1])+int(res[i+2][1]))
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_nb_vis_site = pd.DataFrame({
            "Nombre de visites": valeurs1,
            "Sites": ["Rome", "Venise"]
    })
    
    #construction de la figure
    fig_nb_vis_site = px.bar(data_nb_vis_site, 
            x="Sites", 
            y="Nombre de visites", 
            text="Nombre de visites", 
            color="Sites",
            color_discrete_map=colors_site
    ) 

    #modification de l'affichage de la figure
    fig_nb_vis_site.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_nb_vis_site.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_nb_vis_site.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #chargement en format JSON de la figure, pour quelle soit interpretable par Flask
    graphJSON_nb_vis_site = json.dumps(fig_nb_vis_site, cls=plotly.utils.PlotlyJSONEncoder)
    titre_nb_vis_site = "Flux touristique par site touristique"
    description_nb_vis_site = "Ce graphique présente le nombre de touristes ayant visité Rome ou Venise."
    interpretation_nb_vis_site = "On remarque sur ce graphique que les touristes qui visitent le site de Rome sont 3 fois plus nombreux que ceux qui visitent  celui de Venise."
    
    #graphique nb_vis_monu
    valeurs2 = []
    monuments2 = []
    for row in res:
        valeurs2.append(int(row[1]))
        monuments2.append(row[0])
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_nb_vis_monu = pd.DataFrame({
            "Monuments": ["Fontaine de Trévi", "Colisée", "Panthéon", "Place Saint-Marc", "Pont du Rialto", "Palais des Doges"],
            "Nombre de visites": valeurs2,
            "Sites": ["Rome", "Rome", "Rome", "Venise", "Venise", "Venise"]
    })
    
    #construction de la figure
    fig_nb_vis_monu = px.bar(data_nb_vis_monu, 
            x="Sites", 
            y="Nombre de visites", 
            text="Nombre de visites",
            color="Monuments", 
            barmode="group", 
            color_discrete_map=colors_monuments
    )
    
    #modification de l'affichage de la figure
    fig_nb_vis_monu.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_nb_vis_monu.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_nb_vis_monu.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_nb_vis_monu = json.dumps(fig_nb_vis_monu, cls=plotly.utils.PlotlyJSONEncoder)
    titre_nb_vis_monu = "Flux touristique par monument"
    description_nb_vis_monu = "Ce graphique présente le nombre de touristes ayant visité les monuments de Rome et de Venise (le Colisée, le Panthéon, la Fontaine de Trevi) et Venise (le palais des Doges, le Pont du Rialto et la place Saint-Marc)."
    interpretation_nb_vis_monu ="On constate que la Fontaine de Trevi est le monument le plus visité, s'ensuit le Colisée puis le Panthéon ce qui est normal car étant des monuments du site de Rome. Quant aux monuments de Venise, ils sont les moins visités."
    
    
    
    #graphique lien_venise_rome
    values = []
    for row in res5:
        values.append(int(row[1]))
        
    labels = ["Personnes ayant visité Rome et Venise au cours du même voyage" ,
              "Personnes n'ayant pas visité Rome et Venise au cours du même voyage"]
    
    #construction de la figure
    colors_pie = ['#14ca1c', '#ca1414']
    fig_lien_venise_rome = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0.2])])
    fig_lien_venise_rome.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    fig_lien_venise_rome.update_traces(
            hoverinfo='label+value', 
            textinfo='percent', 
            textfont_size=20,
            marker=dict(colors=colors_pie))

    #definition des variables de retour de la fonction
    graphJSON_lien_venise_rome = json.dumps(fig_lien_venise_rome, cls=plotly.utils.PlotlyJSONEncoder)
    titre_lien_venise_rome = "Lien entre Venise et Rome"
    description_lien_venise_rome= "Ce graphique présente le pourcentage des touristes ayant visité rome et venise et ceux ayant visité Rome ou Venise."
    interpretation_lien_venise_rome ="On remarque sur ce graphique que les touristes visitent en majorité soit Rome soit Venise, ce qui est le cas pour 98 pourcent des visiteurs, très peu de touristes visitent à la fois Rome et Venise, c'est le cas pour 2 pourcent des personnes. On peut donc dire qu'il n'y a pas vraiment de lien entre Rome et Venise."
    
    
    
    
    description = "Cette page nous présente des graphiques qui nous montrent le flux touristique par site touristique et par monument de 2017 à 2021."
    
    #retour de la fonction
    return render_template('graphed.html',
            description_page_description = description,
            graph_nb_vis_site = graphJSON_nb_vis_site, 
            titre_nb_vis_site = titre_nb_vis_site,
            description_nb_vis_site = description_nb_vis_site,
            interpretation_nb_vis_site = interpretation_nb_vis_site,
            graph_nb_vis_monu = graphJSON_nb_vis_monu,
            titre_nb_vis_monu = titre_nb_vis_monu,
            description_nb_vis_monu = description_nb_vis_monu,
            interpretation_nb_vis_monu = interpretation_nb_vis_monu,
            
            graph_lien_venise_rome = graphJSON_lien_venise_rome,
            titre_lien_venise_rome = titre_lien_venise_rome,
            description_lien_venise_rome = description_lien_venise_rome,
            interpretation_lien_venise_rome = interpretation_lien_venise_rome
    )

                        
@app.route('/focus/')
def graphf():
    
    #connection a la base de donnees
    #recuperations des donnees utiles a l'affichage des graphiques d ela page
    try:
        conn = psycopg2.connect(
              user = "m101",
              password = "1999",
              host = "db-etu.univ-lyon2.fr",
              port = "5432",
              database = "m101"
        )
        
        cur6 = conn.cursor()
        sql6 = "select * from avantVSpendant"
        cur7 = conn.cursor()
        sql7 = "select * from evolutionmoisromecume"
        cur8 = conn.cursor()
        sql8 = "select * from evolutionmoisvenisecume"

        cur6.execute(sql6)
        cur7.execute(sql7)
        cur8.execute(sql8)
        
        res6 = cur6.fetchall()
        res7 = cur7.fetchall() 
        res8 = cur8.fetchall()
        
        cur6.close()
        cur7.close()
        cur8.close()
        conn.close()
    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la connexion à PostgreSQL", error)


    
    
    #graphique comparaisons
    valeurs = []
    monuments = []
    for i in range(0,6):
        valeurs.append(res6[i][1])
        valeurs.append(res6[i][2])
        monuments.append(res6[i][0])
        monuments.append(res6[i][0])
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_comparaison = pd.DataFrame({
            "Monuments": monuments,
            "Nombre de visites": valeurs,
            "Periode": ["Avant", "Pendant", "Avant", "Pendant", "Avant", "Pendant",
                     "Avant", "Pendant", "Avant", "Pendant", "Avant", "Pendant"]
    })
    
    #construction de la figure
    fig_comparaison = px.bar(data_comparaison, 
            x=["Colisée","Colisée", "Palais des Doges",  "Palais des Doges", "Fontaine de Trévi", "Fontaine de Trévi", "Panthéon", "Panthéon", "Place Saint-Marc", "Place Saint-Marc", "Pont du Rialto" ,"Pont du Rialto" ],
            y="Nombre de visites", 
            text="Nombre de visites", 
            color="Periode", 
            barmode="group",
            color_discrete_map=colors_avant_pendant
    )
    
    #modification de l'affichage de la figure
    fig_comparaison.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_comparaison.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_comparaison.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_comparaison = json.dumps(fig_comparaison, cls=plotly.utils.PlotlyJSONEncoder)
    titre_comparaison = "Comparaison des flux touristiques par monuments avant et pendant la période covid"
    description_comparaison = "Ce graphique présente le nombre de touristes ayant visité avant le covid et pendant le covid les monuments de Rome ou Venise."
    interpretation_comparaison = "On constate tout d’abord qu'avant le covid le nombre de  touristes est plus élevé que pendant le covid au niveau de tous les monuments.\
        Ensuite, les chiffres nous montrent que pendant le covid, le Colisée et la fontaine de Trevi enregistrent le plus grand nombre de visites soient respectivement 2942 et 2749.\
        Le graphique nous montre donc que le covid a un impact sur le tourisme à Rome et Venise."
    
    
    #graphe comparaison annee rome
    valeurs = []
    id_mois = []
    annee = []
    for i in range(0, len(res7)):
        valeurs.append(res7[i][2])
        annee.append(res7[i][3])
        id_mois.append(res7[i][5])
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_rome = pd.DataFrame({
            "id_month": id_mois,
            "cumul_count": valeurs,
            "year": annee,
            "text" : ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O']
    })
    
    #construction de la figure
    fig_comparaison_annee_rome = px.line(data_rome, 
            x = "id_month", 
            y = "cumul_count", 
            color = "year",
            text = "text"
    )
    
    #modification de l'affichage de la figure
    fig_comparaison_annee_rome.update_traces(textposition="top left")
    fig_comparaison_annee_rome.update_layout(xaxis_title = 'Mois', yaxis_title = 'Nombre de visites cumulées')
    fig_comparaison_annee_rome.update_layout(height=500, margin={'l': 50, 'b': 50, 't': 20, 'r': 0}, hovermode='closest')
    fig_comparaison_annee_rome.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_comparaison_annee_rome = json.dumps(fig_comparaison_annee_rome, cls=plotly.utils.PlotlyJSONEncoder)
    titre_comparaison_annee_rome = "Comparaison des évolutions annuelles des flux touristiques pour le site de Rome"
    description_comparaison_annee_rome = "Ce graphique présente le nombre de touristes ayant visité le site de Rome de 2017 à 2021 (avant le covid et pendant le covid)."

    #graphique comparaison annee venise
    valeurs_v = []
    id_mois_v = []
    annee_v = []
    for i in range(0, len(res8)):
        valeurs_v.append(res8[i][2])
        annee_v.append(res8[i][3])
        id_mois_v.append(res8[i][5])
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_venise = pd.DataFrame({
            "id_month": id_mois_v,
            "cumul_count": valeurs_v,
            "year": annee_v,
            "text" : ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
                      'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O']
    })
    
    #construction de la figure
    fig_comparaison_annee_venise = px.line(data_venise, 
            x = "id_month", 
            y = "cumul_count", 
            color = "year",
            text = "text"
    )
    
    #modification de l'affichage de la figure
    fig_comparaison_annee_venise.update_traces(textposition="top left")
    fig_comparaison_annee_venise.update_layout(xaxis_title = 'Mois', yaxis_title = 'Nombre de visites cumulées')
    fig_comparaison_annee_venise.update_layout(height=500, margin={'l': 50, 'b': 50, 't': 20, 'r': 0}, hovermode='closest')
    fig_comparaison_annee_venise.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_comparaison_annee_venise = json.dumps(fig_comparaison_annee_venise, cls=plotly.utils.PlotlyJSONEncoder)
    titre_comparaison_annee_venise = "Comparaison des évolutions annuelles des flux touristiques pour le site de Venise"
    description_comparaison_annee_venise = "Ce graphique présente le nombre de touristes ayant visité le site de Venise de 2017 à 2021 (avant le covid et pendant le covid)."
    interpretation_comparaison_annee_rome_venise = "On remarque sur ce graphique que  le nombre de touristes diminue au fur et à mesure des années. Les années 2017 et 2018  sont celles  où Rome enregistre le plus grand nombre de touristes.\
        Le nombre de touristes décroît faiblement jusqu’au 4ème trimestre de l’année 2019 avant de décroître fortement jusqu’à la fin de l’année. Pendant l’année 2020, très peu de touristes visitent Rome et en  2021, le nombre de touristes est très faible.\
        L'année 2017 est  celle où Venise enregistre le plus grand nombre de touristes. Le nombre de touristes diminue progressivement en 2018.En 2019, on observe une forte diminution du nombre de touristes. Pendant l’année 2020, le nombre de touristes est très faible.\
        Cependant, en  2021, on observe une légère augmentation du nombre de touristes.\
        On peut donc conclure au vu de ces analyses que le covid a eu un impact sur le tourisme à Rome et à Venise."
  
    
  
    #graphiques des evolutions mensuels 
    (fs1,fmr1,fmv1)=testC(2017)
    (fs2,fmr2,fmv2)=testC(2018)
    (fs3,fmr3,fmv3)=testC(2019)
    (fs4,fmr4,fmv4)=testC(2020)
    (fs5,fmr5,fmv5)=testC(2021)
    
    titre_evol_mens = " Evolution mensuelle du nombre de visites par monument et par site touristique"
    description_evol_mens = "Le graphique représente l’évolution du nombre de visites  par mois pour chaque année des monuments des deux sites."
    interpretation_evol_mens = "On constate tout d’abord que le nombre de visites à Rome  est plus élevé que celui à Venise sur tous les mois pour toutes les années.\
        Ensuite, ces graphiques nous montrent que ce nombre de visites varie d’un mois à un autre et d’une année à une autre.\
        En 2017, on observe  que le nombre de touristes augmente au fil des mois. Au niveau des 3 monuments de Rome, les touristes visitent en majorité la fontaine de Trevi que les autres sur tous les mois. Au niveau des 3 monuments de Venise, le palais des Doges semble être le plus visité mais  on observe à partir du 3éme mois que la place Saint-Marc a le plus grand nombre de touristes.\
        Le flux touristique en 2018 évolue comme celui de 2017, en effet , la fontaine de Trevi reste le monument  le plus visité au niveau des monuments de Rome et la place Saint-Marc au niveau de ceux de  Venise.\
        En ce qui concerne l’année 2019,sur les 2 premiers mois, Colisée est le monument le plus visité mais à partir du 3éme mois la fontaine de Trevi prend le dessus et reste le monument le plus visité. La place Saint-Marc reste le monument le plus visité au niveau des 3 monuments de Venise tout au long de l’année.\
        Sur toute l’année 2020, le Colisée et la fontaine de Trevi sont les monuments les plus visités. Au niveau des 3 monuments de Venise, la place Saint-Marc est le monument le plus visité au cours des 7 premiers mois. A partir du 8ème mois, le palais des Doges  devient le monuments le plus visité.\
        En 2021, la Fontaine de Trevi demeure le monument le plus visité mais à partir du 7éme mois, le Colisée enregistre le plus grand nombre de touristes. La place Saint-Marc demeure le monument le plus visité au niveau des monuments de Venise."
    
  
    description = "Ces  graphiques nous permettent de voir l’effet du covid sur le tourisme à Rome et Venise. De plus, sur cette page, le graphique “Evolution mensuelle du nombre de visites par monument et par site” nous permet d’appréhender l’évolution mensuelle du nombre de touristes  de 2017 à 2021 des monuments des sites de Rome et Venise."  
  
    

    #retour de la fonction
    return render_template('graphef.html',
            description_page_focus = description,
                           
            
            graph_comparaison = graphJSON_comparaison,
            titre_comparaison = titre_comparaison,
            description_comparaison = description_comparaison,
            interpretation_comparaison = interpretation_comparaison,
            
            graph_comparaison_annee_rome = graphJSON_comparaison_annee_rome,
            titre_comparaison_annee_rome = titre_comparaison_annee_rome,
            description_comparaison_annee_rome = description_comparaison_annee_rome,
            graph_comparaison_annee_venise = graphJSON_comparaison_annee_venise,
            titre_comparaison_annee_venise = titre_comparaison_annee_venise,
            description_comparaison_annee_venise = description_comparaison_annee_venise,
            
            interpretation_comparaison_annee_rome_venise = interpretation_comparaison_annee_rome_venise,
            
            fgs2017=fs1,fgmr2017=fmr1,fgmv2017=fmv1,
            fgs2018=fs2,fgmr2018=fmr2,fgmv2018=fmv2,
            fgs2019=fs3,fgmr2019=fmr3,fgmv2019=fmv3,
            fgs2020=fs4,fgmr2020=fmr4,fgmv2020=fmv4,
            fgs2021=fs5,fgmr2021=fmr5,fgmv2021=fmv5,
            
            interpretation_evol_mens = interpretation_evol_mens,
            titre_evol_mens = titre_evol_mens,
            description_evol_mens = description_evol_mens
            
            
                       
    )



@app.route('/prev/')
def graphp():
    
    #connection a la base de donnees
    #recuperations des donnees utiles a l'affichage des graphiques d ela page
    try:
        conn = psycopg2.connect(
              user = "m101",
              password = "1999",
              host = "db-etu.univ-lyon2.fr",
              port = "5432",
              database = "m101"
        )
        
        cur9 = conn.cursor()
        sql9 = "select * from AnalysePred_Rome_cum"
        cur10 = conn.cursor()
        sql10 = "select * from AnalysePred_Venise_cum"
        cur14 = conn.cursor()
        sql14 = "select * from PredictionRome_2017_2026"
        cur15 = conn.cursor()
        sql15 = "select * from PredictionVenise_2017_2026"
        cur16 = conn.cursor()
        sql16 = "select * from DonneesFinales"

        cur9.execute(sql9)
        cur10.execute(sql10)
        cur14.execute(sql14)
        cur15.execute(sql15)
        cur16.execute(sql16)
        
        res9 = cur9.fetchall() 
        res10 = cur10.fetchall()
        res14 = cur14.fetchall() 
        res15 = cur15.fetchall()
        res16 = cur16.fetchall()
        
        cur9.close()
        cur10.close()
        cur14.close()
        cur15.close()
        cur16.close()
        conn.close()
    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la connexion à PostgreSQL", error)


   
    #graphique prediction_venise
    valeurs_v = []
    trim_v = []
    id_trim_v = []
    annee_v = []
    for i in range(0, len(res9)):
        valeurs_v.append(res9[i][1])
        annee_v.append(res9[i][2])
        trim_v.append(res9[i][3])
        id_trim_v.append(res9[i][4])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_prev_venise = pd.DataFrame({
            "id_trim": id_trim_v,
            "cumul_count": valeurs_v,
            "year": annee_v,
            "trim" : trim_v
    })
    
    #construction de la figure
    fig_prediction_venise = px.line(data_prev_venise, 
        x = "id_trim", 
        y = "cumul_count", 
        text = "trim",
        range_x = [1,4.5],
        range_y = [-10000,55000],
        animation_frame = "year",
        color_discrete_map=colors_monuments
        )

    #modification de l'affichage de la figure
    fig_prediction_venise.update_traces(textposition="bottom right")
    fig_prediction_venise.update_layout(xaxis_title = 'Trimestre', yaxis_title = 'Nombre de visites cumulées')
    fig_prediction_venise.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_prediction_venise = json.dumps(fig_prediction_venise, cls=plotly.utils.PlotlyJSONEncoder)
    titre_prediction_venise = "Prévision du nombre de visites à Venise de 2021 à 2023."
    description_prediction_venise = "Ce graphique présente le nombre de touristes pour les années à venir dans le site touristique de Venise."
    interpretation_prediction_venise = "On observe sur le graphique de la prévision qu’au troisième trimestre de l’année 2021, le nombre de touristes aura augmenté d’une quinzaine. En 2022, le nombre de touristes diminuera par rapport à l’année précédente, cependant on observe une augmentation une légère augmentation du 1er au 4éme trimestre. En 2023, le nombre de touristes est faible."
    
    #graphique prediction_rome 
    valeurs_r = []
    trim_r = []
    id_trim_r = []
    annee_r = []
    for i in range(0, len(res10)):
        valeurs_r.append(res10[i][1])
        annee_r.append(res10[i][2])
        trim_r.append(res10[i][3])
        id_trim_r.append(res10[i][4])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_prev_rome = pd.DataFrame({
            "id_trim": id_trim_r,
            "cumul_count": valeurs_r,
            "year": annee_r,
            "trim" : trim_r
    })
        
    #construction de la figure
    fig_prediction_rome = px.line(data_prev_rome, 
            x = "id_trim", 
            y = "cumul_count", 
            text = "trim",
            range_x = [1,4.5],
            range_y = [-10000,55000],
            animation_frame = "year"
    )

    #modification de l'affichage de la figure
    fig_prediction_rome.update_traces(textposition="bottom right")
    fig_prediction_rome.update_layout(xaxis_title = 'Trimestre', yaxis_title = 'Nombre de visites cumulées')
    fig_prediction_rome.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_prediction_rome = json.dumps(fig_prediction_rome, cls=plotly.utils.PlotlyJSONEncoder)
    titre_prediction_rome = "Prévision du nombre de visite à Rome de 2021 à 2023"
    description_prediction_rome = "Ce graphique présente le nombre de visite à partir du quatrième trimestre de l'année 2021 jusqu'en 2023 pour le site de Venise"
    interpretation_prediction_rome = "On prévoit qu’au quatrième trimestre de l’année 2021, le nombre de touristes a légèrement augmenté. En 2022, on prévoit que le nombre de touristes connaîtra une diminution par rapport à l’année 2021 mais nous aurons une augmentation au fur et à mesure des trimestres. En 2023, on prévoit que le nombre de touristes sera encore beaucoup plus amoindrir que l’année précédente."
  
    
    conclusion_preduction_rome_venise = "Suite aux données de la prédiction, on remarque bien que  le nombre de personnes visitant  les sites de Rome et Venise décroît pendant l’année 2022 et 2023. \
                                        On peut dire que le tourisme n’a pas complètement repris. Cette situation est dû \
                                        au covid. On peut donc dire que le covid continuera jusqu’à en 2023."
    
    
    
    #graphique prediction Rome 2026
    valeurs_r_26 = []
    trim_r_26 = []
    id_trim_r_26 = []
    annee_r_26 = []
    for i in range(0, len(res14)):
        valeurs_r_26.append(res14[i][4])
        annee_r_26.append(res14[i][1])
        trim_r_26.append(res14[i][2])
        id_trim_r_26.append(res14[i][3])
    
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_r_26 = pd.DataFrame({
            "id_trim": id_trim_r_26,
            "cumul_count": valeurs_r_26,
            "year": annee_r_26,
            "trim" : trim_r_26
    })
    
    #construction de la figure
    fig_prediction_r_26 = px.line(data_r_26.loc[data_r_26['year']>2023],
        x = "id_trim",
        y = "cumul_count",
        text = "trim",
        range_x = [1,4.5],
        range_y = [0,50000],
        animation_frame = "year")

    #modification de l'affichage 
    fig_prediction_r_26.update_traces(textposition="bottom right")
    fig_prediction_r_26.update_layout(xaxis_title = 'Trimestre', yaxis_title = 'Nombre de visites cumulées')
    fig_prediction_r_26.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_prediction_rome_2026 = json.dumps(fig_prediction_r_26, cls=plotly.utils.PlotlyJSONEncoder)
    titre_prediction_rome_26 = "Simulation du nombre de visites à Rome de 2024 à 2026"
    description_prediction_rome_26 = "Ce graphique présente le nombre de visite à partir du premier trimestre de l'année 2024 jusqu'en 2026 pour le site de Rome"
    
    
    #graphique prediction venise 2026
    valeurs_v_26 = []
    trim_v_26 = []
    id_trim_v_26 = []
    annee_v_26 = []
    for i in range(0, len(res15)):
        valeurs_v_26.append(res15[i][4])
        annee_v_26.append(res15[i][1])
        trim_v_26.append(res15[i][2])
        id_trim_v_26.append(res15[i][3])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_v_26 = pd.DataFrame({
            "id_trim": id_trim_v_26,
            "cumul_count": valeurs_v_26,
            "year": annee_v_26,
            "trim" : trim_v_26
    })
    
    #construction de la figure
    fig_prediction_v_26 = px.line(data_v_26.loc[data_v_26['year']>2023],
        x = "id_trim",
        y = "cumul_count",
        text = "trim",
        range_x = [1,4.5],
        range_y = [0,20000],
        animation_frame = "year")

    #modification de l'affichage 
    fig_prediction_v_26.update_traces(textposition="bottom right")
    fig_prediction_v_26.update_layout(xaxis_title = 'Trimestre', yaxis_title = 'Nombre de visites cumulées')
    fig_prediction_v_26.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    
    #definition des variables de retour de la fonction
    graphJSON_prediction_venise_2026 = json.dumps(fig_prediction_v_26, cls=plotly.utils.PlotlyJSONEncoder)
    titre_prediction_venise_26 = "Simulation du nombre de visites à Venise de 2024 à 2026"
    description_prediction_venise_26 = "Ce graphique présente le nombre de visite à partir du premier trimestre de l'année 2024 jusqu'en 2026 pour le site de Venise."

    interpretation_prediction_venise_rome_26 = "Le graphique de la simulation nous montre tout d’abord que le nombre de touristes à Rome et Venise augmentera de façon progressive de 2024 à 2026. Ensuite, on remarque que le nombre de visites à Rome  sera toujours plus élevé que celui à Venise sur tous les trimestres pour toutes les années.De plus,on constate que le nombre de touristes augmente progressivement d’un trimestre à un autre pour chaque année."
    conclusion_prediction_venise_rome_26="Suite aux données de la simulation, on remarque bien que  le nombre de personnes visitant  les sites de Rome et Venise croît de l’année 2024 à  2026. On peut dire que les activités ont repris, les gens peuvent voyager  et donc le  tourisme a repris. Cette reprise des activités est dûe au fait que la pandémie du covid à pris fin."
    
    
    #graphique prediction venise 2026
    valeurs_totale = []
    annee_totale = []
    label_total = []
    for i in range(0, len(res16)):
        valeurs_totale.append(res16[i][0])
        annee_totale.append(res16[i][1])
        label_total.append(res16[i][2])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_totale = pd.DataFrame({
            "year": annee_totale,
            "count": valeurs_totale,
            "label": label_total
    })
    
    #construction de la figure
    fig_evol_totale = px.line(data_totale,
        x = "year",
        y = "count",
        text = "year",
        color = "label",
        color_discrete_map=colors_site
        )
         
    #modification de l'affichage
    fig_evol_totale.update_traces(textposition="top right")
    fig_evol_totale.update_layout(xaxis_title = 'Année', yaxis_title = 'Nombre de visites')
    fig_evol_totale.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    
    #definition des variables de retour de la fonction
    graphJSON_evol_totale = json.dumps(fig_evol_totale, cls=plotly.utils.PlotlyJSONEncoder)
    titre_evol_totale = "Evolution des flux touristiques de 2017 à 2026"
    description_evol_totale = "Ce graphique présente les variations des flux touristiques des 2 sites de Rome et Venise tout au long de nos années d’étude c’est-à-dire de 2017 à 2021 et présente les flux sur les années allant jusqu’en 2026."    
    interpretation_evol_totale = "Le graphique permet de regrouper les résultats de notre analyse et de voir encore une fois que la période Covid, de 2019 à 2023 a réellement été source de baisse des flux touristiques tant pour Rome que pour Venise. A partir de 2024, année supposée de retour à la normale, on remarque une nette hausse qui s’expliquerait par la réouverture totale des frontières et par l’envie que les gens auront de voyager à nouveau librement. Les années qui suivent le nombre de visites semble toujours augmenter. On pourrait expliquer cela par le fait qu’au fil du temps les quelques personnes qui étaient encore quelque peu réticentes au fait de voyager immédiatement retrouvent peu à peu assurance ou encore que les personnes qui au sortir de la crise ne pouvaient pas en 2024 se payer ce voyage, ont pu ensuite regrouper assez d’argent."
    

    
    description = "Cette page nous présente une prévision de 2021 à 2026 de l’évolution trimestrielle du nombre de touristes par site touristique et par monument."
    
    #retour de la fonction
    return render_template('graphep.html',
            description_page_prevision = description,
                           
            graph_prediction_venise= graphJSON_prediction_venise,
            titre_prediction_venise = titre_prediction_venise,
            description_prediction_venise = description_prediction_venise,
            interpretation_prediction_venise = interpretation_prediction_venise,
            
            graph_prediction_rome= graphJSON_prediction_rome,
            titre_prediction_rome = titre_prediction_rome,
            description_prediction_rome = description_prediction_rome,
            interpretation_prediction_rome = interpretation_prediction_rome,
                        
            conclusion_preduction_rome_venise = conclusion_preduction_rome_venise,
            
            
            graph_prediction_rome_2026 = graphJSON_prediction_rome_2026,
            titre_prediction_rome_26 = titre_prediction_rome_26,
            description_prediction_rome_26 = description_prediction_rome_26,
            
            graph_prediction_venise_2026 = graphJSON_prediction_venise_2026,
            titre_prediction_venise_26 = titre_prediction_venise_26,
            description_prediction_venise_26 = description_prediction_venise_26,
            
            interpretation_prediction_venise_rome_26 = interpretation_prediction_venise_rome_26,
            conclusion_prediction_venise_rome_26 = conclusion_prediction_venise_rome_26,
            
            graphe_evol_totale = graphJSON_evol_totale,
            titre_evol_totale = titre_evol_totale,
            description_evol_totale = description_evol_totale,
            interpretation_evol_totale = interpretation_evol_totale            
    )




def testC(year_slctd):
    
    #connection a la base de donnees
    #recuperations des donnees utiles a l'affichage des graphiques de la page
    try:
        conn = psycopg2.connect(
              user = "m101",
              password = "1999",
              host = "db-etu.univ-lyon2.fr",
              port = "5432",
              database = "m101"
        )
        
        cur11 = conn.cursor()
        sql11 = "select * from EvolutionMois_label__rome_cum"
        cur12 = conn.cursor()
        sql12 = "select * from EvolutionMois_label__venise_cum"
        cur13 = conn.cursor()
        sql13 = "select * from EvolutionMois_label__cum"

        cur11.execute(sql11)
        cur12.execute(sql12)
        cur13.execute(sql13)
        
        res11 = cur11.fetchall() 
        res12 = cur12.fetchall()
        res13 = cur13.fetchall()
        
        cur11.close()
        cur12.close()
        cur13.close()
        conn.close()
    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la connexion à PostgreSQL", error)
        
    
    
    #recuperer les donnees de EvolutionMois_label__rome_cum
    site_r_cum = []
    count_r_cum = []
    valeurs_r_cum = []
    annee_r_cum = []
    month_r_cum = []
    id_month_r_cum = []
    for i in range(0, len(res11)):
        site_r_cum.append(res11[i][0])
        count_r_cum.append(res11[i][1])
        valeurs_r_cum.append(res11[i][2])
        annee_r_cum.append(res11[i][3])
        month_r_cum.append(res11[i][4])
        id_month_r_cum.append(res11[i][5])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_r_cum = pd.DataFrame({
        "site" :  site_r_cum,  
        "count" : count_r_cum,
        "cumul_count": valeurs_r_cum,
        "year": annee_r_cum,
        "month" : month_r_cum,
        "id_month": id_month_r_cum
    })
    
    #recuperer les donnees de EvolutionMois_label__venise_cum
    site_v_cum = []
    count_v_cum = []
    valeurs_v_cum = []
    annee_v_cum = []
    month_v_cum = []
    id_month_v_cum = []
    for i in range(0, len(res12)):
        site_v_cum.append(res12[i][0])
        count_v_cum.append(res12[i][1])
        valeurs_v_cum.append(res12[i][2])
        annee_v_cum.append(res12[i][3])
        month_v_cum.append(res12[i][4])
        id_month_v_cum.append(res12[i][5])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_v_cum = pd.DataFrame({
        "site" :  site_v_cum,  
        "count" : count_v_cum,
        "cumul_count": valeurs_v_cum,
        "year": annee_v_cum,
        "month" : month_v_cum,
        "id_month": id_month_v_cum
    })
    
    
    data_cum_site = pd.concat([data_v_cum,data_r_cum])
    data_cum_site = data_cum_site[['site','count','cumul_count','year','month','id_month']]
    data_cum_site = data_cum_site.sort_values(['year','id_month','cumul_count'], ascending=True)

    
    #recuperer les donnees de EvolutionMois_label__cum    
    monument_cum = []
    count_cum = []
    valeurs_cum = []
    annee_cum = []
    month_cum = []
    id_month_cum = []
    for i in range(0, len(res13)):
        monument_cum.append(res13[i][0])
        count_cum.append(res13[i][1])
        valeurs_cum.append(res13[i][2])
        annee_cum.append(res13[i][3])
        month_cum.append(res13[i][4])
        id_month_cum.append(res13[i][5])
        
    #regrouper les donnees dans un dataframe pour la construction de la figure 
    data_cum = pd.DataFrame({
        "monument" :  monument_cum,  
        "count" : count_cum,
        "cumul_count": valeurs_cum,
        "year": annee_cum,
        "month" : month_cum,
        "id_month": id_month_cum
    })
    

    data_cum = data_cum[['monument','count','cumul_count','year','month','id_month']]
    data_cum = data_cum.sort_values(['year','id_month','cumul_count'], ascending=True)
    
    
    #Séparation Rome ~ Venise
    data_cum_monument_r = data_cum.loc[(data_cum.monument == "colisee") | (data_cum.monument == "pantheon") | (data_cum.monument == "fontaine_de_trevi"), data_cum.columns]
    
    data_cum_monument_v = data_cum.loc[(data_cum.monument == "doges") | (data_cum.monument == "pont_du_raltio") | (data_cum.monument == "piazza_san_marco"), data_cum.columns]

    #Rename value monuments
    data_cum_monument_r.loc[data_cum_monument_r.monument == "colisee",'monument']='Colisée'
    data_cum_monument_r.loc[data_cum_monument_r.monument == "fontaine_de_trevi",'monument']='Fontaine de Trevi'
    data_cum_monument_r.loc[data_cum_monument_r.monument == "pantheon",'monument']='Panthéon'

    data_cum_monument_v.loc[data_cum_monument_v.monument == "pont_du_raltio",'monument']='Pont du Rialto'
    data_cum_monument_v.loc[data_cum_monument_v.monument == "doges",'monument']='Palais des Doges'
    data_cum_monument_v.loc[data_cum_monument_v.monument == "piazza_san_marco",'monument']='Place Saint-Marc'

    dff1 = data_cum_site[data_cum_site["year"] == year_slctd]
    dff2 = data_cum_monument_r[data_cum_monument_r["year"] == year_slctd]
    dff3 = data_cum_monument_v[data_cum_monument_v["year"] == year_slctd]
    
    #construction de la figure
    fig_monument_r = px.line(dff2,
        x = "id_month",
        y = "cumul_count",
        color = "monument",
        text = dff2["month"].astype(str).str[0],
        title = "Rome",
        range_x = [0,14],
        range_y = [0,30000],
        color_discrete_map=colors_monuments_rome
        )
    
    #construction de la figure
    fig_monument_v = px.line(dff3,
        x = "id_month",
        y = "cumul_count",
        color = "monument",
        text = dff3["month"].astype(str).str[0],
        title = "Venise",
        range_x = [0,14],
        range_y = [0,6000],
        
        color_discrete_map=colors_monuments_venise
        )
    
    #construction de la figure
    fig_site = px.line(dff1,
            x = "id_month",
            y = "cumul_count",
            color = "site",
            text = dff1["month"].astype(str).str[0],
            #title = "Rome et Venise",
            range_x = [0,14],
            range_y = [0,45000],
            color_discrete_map=colors_site
            )  
    
    fig_site.update_traces(textposition="top left")
    fig_monument_r.update_traces(textposition="top left")
    fig_monument_v.update_traces(textposition="top left")
    
    fig_site.update_layout(height=600,width=400, margin={'l': 50, 'b': 50, 't': 30, 'r': 0}, hovermode='closest')
    fig_site.update_layout(xaxis_title = 'Mois', yaxis_title = 'Nombre de visites cumulées')
    
    fig_monument_r.update_layout(height=300,width=400, margin={'l': 50, 'b': 50, 't': 30, 'r': 0}, hovermode='closest')
    fig_monument_r.update_layout(xaxis_title = 'Mois', yaxis_title = 'Nombre de visites cumulées')

    fig_monument_v.update_layout(height=300,width=400, margin={'l': 50, 'b': 50, 't': 30, 'r': 0}, hovermode='closest')
    fig_monument_v.update_layout(xaxis_title = 'Mois', yaxis_title = 'Nombre de visites cumulées')

    fs = json.dumps(fig_site, cls=plotly.utils.PlotlyJSONEncoder)
    fmr = json.dumps(fig_monument_r, cls=plotly.utils.PlotlyJSONEncoder)
    fmv = json.dumps(fig_monument_v, cls=plotly.utils.PlotlyJSONEncoder)
    
    return (fs,fmr,fmv)

@app.route('/graph/')
def graph():

    df =pd.read_csv("Nb_visites_tot-monuments.csv", sep=";")
    df = np.array(df)
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
    fig = px.bar(data, x="Sites", y="Nombre de visites", color="Monuments", barmode="group", color_discrete_map=colors_monuments) #typage du graphe
    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    ## story graph 2
    valeurs = []
    for i in range(0,6,3):
        valeurs.append(df[i][1]+df[i+1][1]+df[i+2][1])
        #print(df[i][1],df[i+1][1],df[i+2][1])
    
    data2 = pd.DataFrame({
        "Nombre de visites": valeurs,
        "Sites": ["Rome", "Venise"]
    })
    
    fig2 = px.bar(data2, x="Sites", y="Nombre de visites", color="Sites",color_discrete_map=colors_site) #typage du graphe

    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graphe.html',
                       a = graphJSON2,b = "dash_app2.layout",graphJSON =graphJSON)

#lancement de l'instance Flask
if __name__ == "__main__":
    app.run(debug=True)
