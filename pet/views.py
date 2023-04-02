from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import locale
locale.setlocale(locale.LC_TIME,'')
import datetime
from pet.models import Pet, PetNeeds, PetFeeds

def get_last_needs():
    data = {}
    lastneeds = PetNeeds.objects.filter(done=True).order_by('-date_out').first()
    if lastneeds:
        data = {
            "poop": lastneeds.poop,
            "pee": lastneeds.pee,
            "walk": lastneeds.walk,
            "time": lastneeds.delta
        }
    return data

def get_current_needs(data=None):
    current_petneeds =  PetNeeds.objects.filter(state='start').first()
    if current_petneeds and data:
        # we need to render minute, hour, 
        timer = datetime.datetime.now() - current_petneeds.date_in.replace(tzinfo=None) 
        
        data['in_needs_hour'] = '{:02d}'.format(int(timer.seconds / 60 / 24))
        data['in_needs_minute'] = '{:02d}'.format(int((timer.seconds / 60) % 60 ))
        # we need also enable button stop and disabled button start
        data['in_needs'] = True
        # idem form poop and pee and walk icon
        data['in_needs_pee'] = current_petneeds.pee
        data['in_needs_poop'] = current_petneeds.poop
        data['in_needs_walk'] = current_petneeds.walk
    return data

def get_last_feed(data=None):
    last_feed = None
    if not data:
        data = {}
    last_feed = PetFeeds.objects.all().last()
    if last_feed:
        data['last_feed_date'] = last_feed.date.strftime('%A %d/%m/%Y %H:%M:%S')
        data['quantity_eated'] = last_feed.eated
    return data

def pet(request, pet_name=None):
    if request.user.is_authenticated:
        pet = Pet.objects.get(name=pet_name)
        response = get_last_needs()
        response = get_current_needs(response)
        response = get_last_feed(response)
        return render(request, 'dashboard.html', response)
    else:
        return redirect('index')

@csrf_exempt
def needs(request):
    response = {}
    data = json.loads(request.body)
    if data['action'] == 'start':
        PetNeeds.objects.create(
            date_in=datetime.datetime.today(),
            who=request.user,
            state='start'
        )
    elif data['action'] == 'stop':
        petneeds = PetNeeds.objects.filter(state='start')[0]
        if petneeds:
            petneeds.date_out = datetime.datetime.today()
            petneeds.state='stop'
            petneeds.done=True
            petneeds.poop = data['poop']
            petneeds.pee = data['pee']
            petneeds.walk = data['walk']
            petneeds.save()
    
        response = get_last_needs()
    return JsonResponse(response)

@csrf_exempt
def food(request):
    data = json.loads(request.body)
    PetFeeds.objects.create(
        quantity_given = data['foodGiven'],
        quantity_left = data['foodLeft'],
        who = request.user
    )
    response = get_last_feed()
    return JsonResponse(response)