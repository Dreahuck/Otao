#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 22:11:06 2020

@author: Mymac
"""
import calendar

def getDay(i):
    calendrier = ["Lundi", "Mardi", "Mercredi",
                  "Jeudi","Vendredi","Samedi","Dimanche"]
    return calendrier[i];


def getMonth(i):
    listeDesMois = ["Janvier", "Février","Mars","Avril","Mai","Juin",
                    "Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    return listeDesMois[i]

def genererJourHtmlAutreMois(num):
    return '<li class="day other-month"> <div class="date">' + str(num) +'</div></li>'

def genererJourHtmlMoisEnCOurs(num,listTache):
    retour = '<li class="day"> <div class="date">' + str(num) + '</div>'
    if len(listTache) <= 30 and len(listTache) > 0:
        #retour += '<div class="event">'
        for tache in listTache:
            retour += '<div class="event"><a href="detailTache/'+str(tache.id) + '"><div id="' + str(tache.id) + '"class="event-desc">'+ str(tache) +'</div> </a></div>'
        #retour += '</div>'
    if len(listTache) >30: 
        retour += '<div class="event"><div class="event-desc">Beaucoup de tâches ('+str(len(listTache))+ ')</div></div>'
    return retour + '</li>'

def creerAgenda(annee, mois, listeTaches):
    html = ''
    a = calendar.monthcalendar(annee, mois)
    for semaine in a:
        html += '<ul class="days">'
        for jour in semaine:
            listeTacheDuJour = [tache for tache in listeTaches if tache.jalon_date.day == jour]
            if jour > 0:
                if len(listeTacheDuJour) >0: 
                    html += genererJourHtmlMoisEnCOurs(jour,listeTacheDuJour)
                else:
                    html += genererJourHtmlMoisEnCOurs(jour,[])
            else:
                html += genererJourHtmlAutreMois('X')
        html += '</ul>'
    return html

