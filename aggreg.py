#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calendar import c
from unicodedata import category
import feedparser as fp
import time
import yaml

def charge_urls(liste_url):
    """Cette fonction récupère les documents RSS, les range dans une liste"""

    #Initialisation d'une liste vide
    liste_flux = [] 

    #Boucle traitant chaque url présent dans la liste des url 
    for url in liste_url:
        
        #On récupère le flux RSS avec la babliothèque de feedparser
        element = fp.parse(url) 

        # Si notre flux RSS est existant 
        if element['bozo'] == False:
            for flux in element['entries']:
                #Alors on l'ajoute à la liste des flux disponible
                liste_flux.append(flux)
        else: 
            # Sinon, on ajoute un None, pour dire que le flux RSS n'existe pas
            liste_flux.append(None) 
    
    return (liste_flux)


def fusion_flux(liste_url, liste_flux): 
    """Cette fonction permet de produire un 'résumé' de chaque flux RSS"""

    #Initialisation d'une liste vide
    liste_évènement = []
    for chaque_flux in liste_flux:

        if not (chaque_flux == None) :
            #On récupère le titre de l'évènement
            titre = chaque_flux['title'] 
            #On récupère le lien de l'évènement
            lien = chaque_flux['link'] 
            #On récupère la description de l'évènement
            description = chaque_flux['description'] 
            #On récupère la date de publication de l'évènement
            pubDate = chaque_flux["published"] 
            #On récupère le Guid
            guid = chaque_flux["guid"] 
            #On récupère la catégorie de l'évènement
            category = chaque_flux["category"] 
            
            #On récupère le nom du lien en fonction du serveur, puis on lui rajoute "http://", afin de pouvoir le lancer sur internet
            liste_serveur_split = chaque_flux["link"].split(".")
            serveur = liste_serveur_split[0].lstrip('http://')

            #Création et ajout du dictionnaire dans la liste_rep
            liste_évènement.append({'titre':titre, 'lien': lien, 'description': description, 
            'date_publi': pubDate, 'categorie':category, 'serveur':serveur, 'guid': guid})

    return liste_évènement 


def genere_html(liste_evenements, chemin_html):
    """Cette fonction permet de générer des pages html à partir d'une liste d'évènements"""

    #Définition de l'heure
    local_time = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
    with open (chemin_html, 'w', encoding='utf-8') as fichier:
        
        # Génération de la balise "head", suivant presque toujours la même base :
        head = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            '<title>Events log</title>',
            '<style>@import url(style.css);</style>',
            '</head>'         
        ]
        
        # Génération de la balise "body"
        body = [
            '<body>',
            '<header>',
            '<h1>'+'Events_log'+'</h1>',
            '<p class="date">'+local_time+'</p>',
            '</header>',
            '<main>'+'\n'
        ]   

        #Pour chaque élément, présent dans la liste des événements
        article = []
        for i in range (len(liste_evenements)):

            # On va séparer les 3 catégories possible = MAJOR - MINOR - CRITICAL
            category = liste_evenements[i]['categorie']
            
            # Si le nom associé à category est "Minor"
            if category == "MINOR":

                # Génération de l'article
                article.append([
                    '<article class="minor">',
                    '<header>',
                    '<h2>'+liste_evenements[i]['titre']+'</h2>',
                    '</header>',
                    '<p class="serv">'+'from: '+liste_evenements[i]['serveur']+'</p>',
                    '<p class="pub_date">'+liste_evenements[i]['date_publi']+'</p>',
                    '<p class="cate">'+category+'</p>',
                    '<p class="guid">'+liste_evenements[i]['guid']+'</p>',
                    '<p class="link">'+'<a href="'+liste_evenements[i]['lien']+'">'+liste_evenements[i]['lien']+'</a>'+'</p>',
                    '<p class="desc">'+liste_evenements[i]['description']+'</p>',
                    '</article>'+'\n'
                ])
            
            # Si le nom associé à category est "Major"
            elif category == "MAJOR":

                # Génération de l'article
                article.append( [
                    '<article class="major">',
                    '<header>',
                    '<h2>'+liste_evenements[i]['titre']+'</h2>',
                    '</header>',
                    '<p class="serv">'+'from: '+liste_evenements[i]['serveur']+'</p>',
                    '<p class="pub_date">'+liste_evenements[i]['date_publi']+'</p>',
                    '<p class="cate">'+category+'</p>',
                    '<p class="guid">'+liste_evenements[i]['guid']+'</p>',
                    '<p class="link">'+'<a href="'+liste_evenements[i]['lien']+'">'+liste_evenements[i]['lien']+'</a>'+'</p>',
                    '<p class="desc">'+liste_evenements[i]['description']+'</p>',
                    '</article>'+'\n'
                ])

            # Si le nom associé à category est "Critical"
            elif category == "CRITICAL":

                # Génération de la balise "article"
                article.append( [
                    '<article class="critical">',
                    '<header>',
                    '<h2>'+liste_evenements[i]['titre']+'</h2>',
                    '</header>',
                    '<p class="serv">'+'from: '+liste_evenements[i]['serveur']+'</p>',
                    '<p class="pub_date">'+liste_evenements[i]['date_publi']+'</p>',
                    '<p class="cate">'+category+'</p>',
                    '<p class="guid">'+liste_evenements[i]['guid']+'</p>',
                    '<p class="link">'+'<a href="'+liste_evenements[i]['lien']+'">'+liste_evenements[i]['lien']+'</a>'+'</p>',
                    '<p class="desc">'+liste_evenements[i]['description']+'</p>',
                    '</article>'+'\n'
                ])

            # On ajoute toute la balise "article" dans la balise "body"
            for le_texte in article:
                body.append(le_texte)
        
       
        # Écriture de la page
        for le_texte in head :
            fichier.writelines(le_texte)
        fichier.write('\n'*2)
    
        for le_texte in body:
            fichier.writelines(le_texte)
        fichier.write('</main>'+'\n')
        fichier.write('</body>'+'\n')
        fichier.write('</html>'+'\n')

        return None

def main():
	
    with open('conf.yaml', 'r') as config:
        config = yaml.safe_load(config)
        
        destination = config['destination']
        url_liste = config['sources']
        rss_name = config['rss-name']
        
    urls =[]
    for url in url_liste:
   		url = url +  '/' + rss_name
   		urls.append(url)

    liste_flux = charge_urls(urls)
    fusion = fusion_flux(urls, liste_flux)
    genere_html(fusion, destination)
    

if __name__ == '__main__':
    main()