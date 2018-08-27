from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

from snap.models import UserData
from django.db.models import Count, Sum, Avg

labels = ['Wellbeing','Company Confidence','Company Connections','People Interactions','Growth','Overall','Critical Thinking']
colors = ['rgb(31, 119, 180)','rgb(255, 127, 14)','rgb(44, 160, 44)','rgb(214, 39, 40)','rgb(148, 103, 189)','rgb(140,86,75)','rgb(227,119,194)']


@login_required
def index(request):
    uname_i = request.user.username
    lastobj = []
    for i in range(len(labels)):
        try:
            lastUserData = UserData.objects.filter(uname=uname_i,label=labels[i]).latest('insertime')
            lastobj.append(lastUserData.ratings)
        except UserData.DoesNotExist:
            lastobj.append(0)

    return render_to_response('snap_survey.html',{'lastobj':lastobj})

@login_required
def addratings(request):
    
    if request.user.is_authenticated:
        
        uname_i = request.user.username
        
        if 'r0' in request.GET and request.GET['r0']:
            r0_i = request.GET['r0']
        if 'r1' in request.GET and request.GET['r1']:
            r1_i = request.GET['r1']
        if 'r2' in request.GET and request.GET['r2']:
            r2_i = request.GET['r2']
        if 'r3' in request.GET and request.GET['r3']:
            r3_i = request.GET['r3']
        if 'r4' in request.GET and request.GET['r4']:
            r4_i = request.GET['r4']
        if 'r5' in request.GET and request.GET['r5']:
            r5_i = request.GET['r5']
        if 'r6' in request.GET and request.GET['r6']:
            r6_i = request.GET['r6']
            
        newranking = UserData(uname=uname_i,label=labels[0],ratings=r0_i)
        newranking.save()
        newranking = UserData(uname=uname_i,label=labels[1],ratings=r1_i)
        newranking.save()    
        newranking = UserData(uname=uname_i,label=labels[2],ratings=r2_i)
        newranking.save()
        newranking = UserData(uname=uname_i,label=labels[3],ratings=r3_i)
        newranking.save()
        newranking = UserData(uname=uname_i,label=labels[4],ratings=r4_i)
        newranking.save()
        newranking = UserData(uname=uname_i,label=labels[5],ratings=r5_i)
        newranking.save()        
        newranking = UserData(uname=uname_i,label=labels[6],ratings=r6_i)
        newranking.save()
        
        return HttpResponse("Inserted")
    
    return HttpResponse("Not authenticated")



@login_required
def alltrend(request):
    
    
    data = []
    for i in range(len(labels)):
        q = UserData.objects.filter(label=labels[i]).extra(select={'day':'date(insertime)'}).values('day').annotate(rating=Avg('ratings'))   
        # y axis
        trend = [d['rating'] for d in q]
        # x axis
        day = [d['day'] for d in q]
    
        # Create a trace
        data.append(go.Scatter(
            x = day,
            y = trend,
            name = labels[i],
            line = dict(
            color = (colors[i]),
            width = 4)
        ))

    for i in range(len(labels)):
        q = UserData.objects.filter(label=labels[i],uname=request.user.username).extra(select={'day':'date(insertime)'}).values('day').annotate(rating=Avg('ratings'))   
        # y axis
        trend = [d['rating'] for d in q]
        # x axis
        day = [d['day'] for d in q]
    
        # Create a trace
        data.append(go.Scatter(
            x = day,
            y = trend,
            name = "Me - " + labels[i],
            line = dict(
            color = (colors[i]),
            width = 4,
            dash='dash'
            )
        ))
        
    layout = go.Layout(
        title='Overall Trend by Day',
        autosize=True
    )
    fig = go.Figure(data=data,layout=layout)
    div = plot(fig,auto_open=False,include_plotlyjs=False,output_type='div')
    return render_to_response('plot.html',{'plot_div':div})





@login_required
def trend(request):
    
    data = []
    for i in range(len(labels)):
        q = UserData.objects.filter(label=labels[i],uname=request.user.username).extra(select={'day':'date(insertime)'}).values('day').annotate(rating=Avg('ratings'))   
        # y axis
        trend = [d['rating'] for d in q]
        # x axis
        day = [d['day'] for d in q]
    
        # Create a trace
        data.append(go.Scatter(
            x = day,
            y = trend,
            name = labels[i]
        ))

    layout = go.Layout(
        title='Overall Trend by Day for ' + request.user.username,
        autosize=True
    )
    fig = go.Figure(data=data,layout=layout)
    div = plot(fig,auto_open=False,include_plotlyjs=False,output_type='div')
    return render_to_response('plot.html',{'plot_div':div})