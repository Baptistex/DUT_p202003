from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
# Create your views here.



def my_custom_sql():
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM bcv._personne")
        table = namedtuplefetchall(cursor)
        #table = cursor.fetchall()
    return table

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request):
    texte = "hello"
    texte += "<ul>"
    for i in my_custom_sql():
        texte+= "<li>"
        for j in i:
            texte+= " - "+str(j)
        texte += "</li>\n"
    texte += "</ul>"
    return HttpResponse(texte)