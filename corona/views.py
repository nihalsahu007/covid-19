from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
import numpy as np
from random import randint
from datetime import date,timedelta
from diagnosis.models import data_base as data
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
# Create your views here.

def scrapeSite():
    
    session = requests.Session()
    url = 'https://www.mohfw.gov.in/'
    session.headers = {'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    content = session.get(url, verify=False).content
    soup=BeautifulSoup(content,"html.parser")
    l=[]
    for span in soup.find_all('span',{'class':"icount"}):
        l.append(span.text)
    #l[0]=''.join(l[0].split(',')[:])
    india={
        'screened':l[0],
        'active':l[1],
        'cured':l[2],
        'death':l[3],
    }
    return india,l[:4]
    


def home(request):
    if request.method=="POST":
        try:
            name=request.POST.get("name")
            number=request.POST.get("number")
            email=request.POST.get("email")
            age=request.POST.get("age")
            street=request.POST.get("street")
            city=request.POST.get("city")
            state =request.POST.get("state")
            profile=request.POST.get("profile")
            organisation=request.POST.get("organisation")
            travel=request.POST.get("travel")
            fever=request.POST.get("fever")
            bodypain=request.POST.get("bodypain")
            runnynose=request.POST.get("runnynose")
            diffbreath=request.POST.get("diffbreath")
            sorethroat=request.POST.get("sorethroat")
            #print(name,email,state,bodypain,runnynose,diffbreath,sorethroat)

            entry=data()
            entry.name,entry.phone,entry.email,entry.age=name,number,email,age
            entry.street,entry.city,entry.state=street,city,state
            entry.profile,entry.organisation,entry.travelHistory=profile,organisation,travel
            entry.fever=fever
            if (bodypain):entry.bodyPain=bodypain
            if (runnynose):entry.runningNose=runnynose
            if (diffbreath):entry.diffBreath=diffbreath
            if (sorethroat):entry.soreThroat=sorethroat
            if entry.profile=="Retired":
                entry.infectionProb=32+(int(entry.travelHistory)*8)+(int(entry.fever)*4)+(int(entry.bodyPain)*3)+(int(entry.runningNose)*4)+(int(entry.diffBreath)*6)+(int(entry.soreThroat)*3)+9
            else:entry.infectionProb=33+(int(entry.travelHistory)*8)+(int(entry.fever)*4)+(int(entry.bodyPain)*3)+(int(entry.runningNose)*4)+(int(entry.diffBreath)*6)+(int(entry.soreThroat)*3)    
            print(entry.infectionProb)
            try:
                entry.save()
                print('saved')
                p_id=entry.infectionProb
                p_id=p_id+(p_id*(randint(5,6))/100)
                request.session['p_id']=p_id
                request.session['name']=entry.name
                return redirect(f'/reports/#view')
            except:
                messages.success(request,f'Please enter vaild and unique Mobile number')
                return redirect('/#msg')
                print('not saved')    
            
            
            

        except:
            pass    



    return render(request,'diagnosis/home.html')

def reports(request):
    labels=[]
    critical_data=[]
    total_data=[]
    india,india_data=scrapeSite()
    india_labels=["Screened", "Active", "Cured", "Deaths"]
    print(india_data)
    try:
        g=requests.get("https://corona.lmao.ninja/all")
        globe=g.json()

    except:
        globe={'cases':337591,'deaths':16313,'recovered':101373}
    try:        
        p_id=request.session.get('p_id')
        if p_id:
            pass
        else:return redirect('/')
        name=request.session.get('name')
        name=name.split()[0]
        print(name)
        zone=''
        color=''
        if p_id:
            if p_id<50:
                messages.success(request,f'Very low {p_id}%')
                zone="SAFE ZONE"
                color="Congrats!"
            elif 70>p_id>50:
                messages.info(request,f'High {p_id}%')
                zone="VULNERABLE ZONE"
                color="Opps!"
            else:
                messages.error(request,f'Very high {p_id}%')
                zone="CRITICAL ZONE"
                color="Caution!"
                
        
        tests_all=data.objects.all().count()
        detected=data.objects.filter(infectionProb__gt = 55).count()
        print(" count =",detected)
        
        for i in range(6,-1,-1):
            d=date.today()-timedelta(i)
            labels.append(f'{d.day} {d.strftime("%b")}')
            total_data.append(data.objects.filter(date__date = date.today()-timedelta(i)).count())
            critical_data.append(data.objects.filter(date__date = date.today()-timedelta(i),infectionProb__gt = 55).count())
        

        context={
            'name':name,
            'zone':zone,
            'prob':p_id,
            'color':color,
            'tests_all':tests_all,
            'detected':detected,
            'labels':labels,
            'total_data':total_data,
            'critical_data':critical_data,
            'globe':globe,
            'india':india,
            'india_data':india_data[1:],
            'india_labels':india_labels[1:],
        }

        return render(request,'diagnosis/report.html',context)
    except:        
        for i in range(6,-1,-1):
            d=date.today()-timedelta(i)
            labels.append(f'{d.day} {d.strftime("%b")}')
            total_data.append(data.objects.filter(date__date = date.today()-timedelta(i)).count())
            critical_data.append(data.objects.filter(date__date = date.today()-timedelta(i),infectionProb__gt = 55).count())
        
        context={
            'labels':labels,
            'total_data':total_data,
            'critical_data':critical_data,
            'globe':globe,
            'india':india,
            'india_data':india_data[1:],
            'india_labels':india_labels[1:],
        }

        return render(request,'diagnosis/report.html',context)

    