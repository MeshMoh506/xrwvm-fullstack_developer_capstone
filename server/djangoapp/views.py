from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get('userName')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )
    else:
        return JsonResponse(
            {"userName": username, "status": "Unauthorized"},
            status=401
        )


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )
    else:
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(
                review_detail.get('review', '')
            )

            if response and 'sentiment' in response:
                review_detail['sentiment'] = response['sentiment']
            else:
                review_detail['sentiment'] = "unknown"

        return JsonResponse(
            {"status": 200, "reviews": reviews}
        )

    return JsonResponse(
        {"status": 400, "message": "Bad Request"}
    )


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse(
            {"status": 200, "dealer": dealership}
        )

    return JsonResponse(
        {"status": 400, "message": "Bad Request"}
    )


def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": 400, "message": "Invalid JSON"}
            )

        try:
            response = post_review(data)
            return JsonResponse(
                {"status": 200, "response": response}
            )
        except Exception as err:
            return JsonResponse(
                {"status": 401, "message": str(err)}
            )

    return JsonResponse(
        {"status": 403, "message": "Unauthorized"}
    )
