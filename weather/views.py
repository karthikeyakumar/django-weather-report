from django.shortcuts import redirect, render
import requests as d
from .models import City
from .forms import Cityform
def index(request):
    url="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7779141bb1573e4ed78ef87a76a71f76"
    err_msg=''
    message=''
    message_class=''
    if request.method=='POST':
        form=Cityform(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            exist_c_count=City.objects.filter(name=new_city).count()
            if exist_c_count==0:
                r=d.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg="City doesn't exists in world" 
            else:
                err_msg='City already exists in Database !'
    if err_msg:
        message=err_msg
        message_class='is-danger'
    else:
        message='city added sucesfully'
        message_class='is-success'
    
    cities=City.objects.all()
    ct=[]
    form=Cityform()
    for city in cities:
        r=d.get(url.format(city)).json()
        print(r)
        cityweather={
            'city':city.name,
            'temperature':r['main']['temp'],
            'humidity':r['main']['humidity'],
            'icon':r['weather'][0]['icon'],
            'description':r['weather'][0]['description']}
        ct.append(cityweather)
        

    context={
    'weatherdata':ct,
    'form': form,
    'message':message,
    'message_class' : message_class
    }

    return render(request, 'weather.html',context)
def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')