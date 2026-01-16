# djangoapp/views.py

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """
    Handle user login.
    Expects JSON body: { "userName": "...", "password": "..." }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
    except Exception:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"error": "Invalid credentials", "userName": username})


def logout_user(request):
    """
    Handle user logout.
    """
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def register(request):
    """
    Handle user registration.
    Expects JSON body:
    {
      "userName": "...",
      "password": "...",
      "firstName": "...",
      "lastName": "...",
      "email": "..."
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")
    except Exception:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return JsonResponse({"userName": username, "status": "Registered"})


def get_cars(request):
    """
    Initialize cars if needed and return all car models with their makes.
    """
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append(
            {
                "CarModel": car_model.name,
                "CarMake": car_model.car_make.name,
            }
        )
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """
    Return list of dealerships.
    If state == "All" → /fetchDealers
    Else → /fetchDealers/<state>
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    """
    Return details for a single dealer by ID.
    """
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def get_dealer_reviews(request, dealer_id):
    """
    Return reviews for a dealer, with sentiment added.
    """
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    if not reviews:
        logger.warning(f"No reviews returned for dealer {dealer_id}")
        return JsonResponse({"status": 200, "reviews": []})

    for review_detail in reviews:
        review_text = review_detail.get("review", "")
        response = analyze_review_sentiments(review_text)

        if response and "sentiment" in response:
            review_detail["sentiment"] = response["sentiment"]
        else:
            review_detail["sentiment"] = "neutral"

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})


    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})