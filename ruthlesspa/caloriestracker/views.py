from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import MealCard, Ingredient


def index(request):
    return render(request, 'ct/caloriestracker.html')


class BaseMealCardsViewSer(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    """Base viewset for user owned mealcards"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def postSaveMealCards(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
            # Get a JSONified mealCards, make them python and save to db.
                data4 = json.loads(request.body)
                #clear This Day before saving a new
                mcMealCardThisDayThisUser = MealCard.objects.filter(user=request.user, dateCreated=data4[0]['dateCreated'])
                mcMealCardThisDayThisUser.delete()
                #loop through and create mealCards created by user at frontend
                for i in data4:
                    print(i['id'])
                    mcId =              i['id']
                    mcUser =            request.user
                    mcDateCreated =     i['dateCreated']
                    mcNumber =          i['number']
                    mcMealTitle =       i['mealTitle']
                    mcNamesCalories =   i['namesCalories']
                    
                    newMealCard = MealCard.objects.create(id=mcId, user=mcUser,     dateCreated=mcDateCreated,number=mcNumber, mealTitle=mcMealTitle)
                    ingName = mcNamesCalories['name']
                    ingEnergy = mcNamesCalories['energy']
                    newIngredient = Ingredient.objects.create(name=ingName, energy=ingEnergy)

                    newMealCard.namesCalories.add(newIngredient)
                    print(newMealCard)
                    newMealCard.save()

                print(data4)
                print("I am printing wanted number: " + str(data4[0]['number']))
                print("I am printing wanted namesCalories: " + str(data4[0]['namesCalories']))
                return redirect('caloriestracker')


        else:
            return HttpResponse('Unauthorized', status=401)
    
    def getMealCards(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                data4 = json.loads(request.body)
                mcUser =            request.user
                mcDateCreated =     data4['dateCreated']

                targetDayMealCards = MealCard.objects.order_by('number').filter(user=mcUser, dateCreated=mcDateCreated)
                print(list(targetDayMealCards.values()))
                return JsonResponse(list(targetDayMealCards.values()), safe=False)


        else:
            return HttpResponse('Unauthorized', status=401)