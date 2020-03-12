from django.shortcuts import render, redirect
import json, requests
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
                IngredientList = Ingredient.objects.get(mealcard = targetDayMealCards[0].id)
                resp = []

                for i in targetDayMealCards:
                    IngredientList = Ingredient.objects.filter(mealcard = i.id)
                    namesCaloriesToResponse = []
                    for j in IngredientList:
                        ingredientContext = {
                            'name': j.name,
                            'energy': j.energy,
                        }
                        namesCaloriesToResponse.append(ingredientContext)

                    context = {
                        'id': i.id,
                        'number': i.number,
                        'mealTitle': i.mealTitle,
                        'dateCreated': i.dateCreated,
                        'namesCalories': namesCaloriesToResponse
                    }
                    resp.append(context)
                    
        
                return JsonResponse(resp, safe=False)


        else:
            return HttpResponse('Unauthorized', status=401)

#------- HELPER FUNCTIONCS -------#
def searchForValueInJson(jsonData, searchedValue):
    amount = 0
    for i in jsonData['foodNutrients']:
        if i['nutrient']['name'].lower() == searchedValue.lower():
            amount = i['amount']
    return amount



class BaseIngredientsView(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    #Base ingredient-related views for the API

    def getIngredientFromId(request):
        
        if request.user.is_authenticated:
            if request.method == 'POST':
                data = json.loads(request.body)
                IngredientId = data['reqIngredientId']
                URL = f'https://api.nal.usda.gov/fdc/v1/{IngredientId}?api_key=tkjynWdwgrZk4ZSFXGK43b36n34uLXnY5aUQsWWc'
                req = requests.get(url = URL)
                data = req.json()

                proteinValue = searchForValueInJson(data, "protein")
                fatValue = searchForValueInJson(data, "Total lipid (fat)")
                carbohydratesValue = searchForValueInJson(data, "Total lipid (fat)")

                response = {
                    'protein': proteinValue,
                    'fat': fatValue,
                    'carbohydrates': carbohydratesValue,
                }
                

                return JsonResponse(response, safe=False)




        else:
            return HttpResponse('Unauthorized', status=401)

