from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader
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

def wip_userlist(request):
    template = loader.get_template('espace_perso/wip_userlist.html')
    context = {
        'userlist': my_custom_sql(),
    }




    """
    texte = "hello"
    texte += "<ul>"
    for i in my_custom_sql():
        texte+= "<li>"
        for fld in i._fields:
            texte+= " - "+str(fld)+": "+str(getattr(i, fld))
        texte += "</li>\n"
    texte += "</ul>"
    """
    return HttpResponse(template.render(context,request))