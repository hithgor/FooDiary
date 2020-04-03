from django.shortcuts import render, redirect
import json, requests
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import MealCard, Ingredient
import uuid


def index(request):
    return render(request, 'ct/caloriestracker.html')

def uuidGenerator(request):
    """Endpoint generating uuid on demand for mealCards"""
    context = {
        "generatedId": uuid.uuid4()
    }
    return JsonResponse(context, safe=False)


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

                    for j in mcNamesCalories:
                        ingName = j['name']
                        ingEnergy = j['energy']
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

#------- HELPER FUNCTIONS -------#
def searchForValueInJson(jsonData, searchedValue):
    amount = 0
    for i in jsonData['foodNutrients']:
        if i['nutrient']['name'].lower() == searchedValue.lower():
            amount = i['amount']
    return amount

def listFoodPortionsInJson(jsonData):
    #----- Returns a list of food sizes to populate frontend dropdown -----#
    foodPortions = []
    for i in jsonData['foodPortions']:
        try:
            description = i['portionDescription']
        except KeyError: 
            description = "default packaging"
        weight = i['gramWeight']
        foodPortions.append({description: weight})

    return foodPortions

def calculateCaloriesFromNutrients(proteinValue=0, fatValue=0, carbohydratesValue=0):
    caloriesValue = proteinValue*4+fatValue*9+carbohydratesValue*4
    return caloriesValue



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
                carbohydratesValue = searchForValueInJson(data, "Carbohydrate, by difference")
                caloriesValue = calculateCaloriesFromNutrients(proteinValue, fatValue, carbohydratesValue)
                foodPortions = listFoodPortionsInJson(data)
                if foodPortions == []:
                    defaultPortion = {'Default Portion': 100}
                    foodPortions.append(defaultPortion)

                response = {
                    'protein': proteinValue,
                    'fat': fatValue,
                    'carbohydrates': carbohydratesValue,
                    'calories': caloriesValue,
                    'foodPortions': foodPortions,
                }
                

                return JsonResponse(response, safe=False)




        else:
            return HttpResponse('Unauthorized', status=401)





class UserStatistics(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    #Creation of user-data based plots and statistics
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def fullStatsToContext(username):
        # returns full list of objects to populate plotly graph in form: 
        #[{'date': datetime.date(2020, 3, 3), 'arrayOfMealValues': [{0: 55}, {1: 55}, {2: 55}, {3: 55}], 'energyCounted': 220}, {'date': datetime.date(2020, 3, 4), 'arrayOfMealValues': [{0: 55}, {1: 55}, {2: 55}], 'energyCounted': 165}]

        
        context = []
        userMealCards = MealCard.objects.order_by('number').filter(user=username)

        for i in userMealCards:
            dateOfMC = i.dateCreated
            caloriesSumByDay = []
            energyCounted = 0
            mealCardsByDay = MealCard.objects.filter(dateCreated = i.dateCreated)
            for j in mealCardsByDay:
                numberOfMealCard= j.number
                energySumForMealCard=0
                IngredientList = Ingredient.objects.filter(mealcard = j.id)
                for k in IngredientList:
                    energySumForMealCard = energySumForMealCard + k.energy
                caloriesSumByDay.append({numberOfMealCard: energySumForMealCard})
                energyCounted = energyCounted + energySumForMealCard
            dictToCreate = {"date": dateOfMC, "arrayOfMealValues": caloriesSumByDay, "energyCounted": energyCounted}
            if dictToCreate not in context:
                context.append(dictToCreate)


        newContext = sorted(context, key= lambda k: k['date'])
        return newContext



    def getStats(request):
        #Get request with user data and return monthly stats
        if request.user.is_authenticated:
            if request.method == 'POST':
                mcUser = request.user
                context = UserStatistics.fullStatsToContext(mcUser)
                

                return JsonResponse(context, safe=False)
        else:
            return HttpResponse('Unauthorized', status=401)

    def getPredictions(request):
        #Get request with user data and return monthly predictions
        return

