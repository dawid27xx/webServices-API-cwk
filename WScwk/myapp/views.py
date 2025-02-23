from django.shortcuts import render
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Professor, Module, ModuleInstance, Rating
import json


@csrf_exempt
def registerUser(request):
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already taken"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"message": "User registered successfully", "user_id": user.id}, status=201)


@csrf_exempt
def loginUser(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"}, status=200)
    else:
        return JsonResponse({"error": "Invalid username or password"}, status=401)


@csrf_exempt
def logoutUser(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)



def listInstances(request):
    instances = ModuleInstance.objects.select_related('module').prefetch_related('professors').values(
        'id', 
        'module__module_code', 
        'module__module_name', 
        'year', 
        'semester'
    )

    for instance in instances:
        instance['professors'] = list(Professor.objects.filter(moduleinstance=instance['id']).values('id', 'full_name'))
        
    if not instances:
        return "No Module Instances"

    return JsonResponse(list(instances), safe=False)


def viewProfessors(request):
    professors = Professor.objects.all()

    if not professors.exists(): 
        return JsonResponse({"message": "No Professors found"}, status=404)

    professorRatings = []

    for professor in professors:
        avgRating = Rating.objects.filter(module_instance__professors=professor).aggregate(Avg('score'))['score__avg']
        avgRating = round(avgRating) if avgRating is not None else 0

        starScore = "*" * avgRating 

        professorRatings.append({
            "prof_code": professor.professor_code,
            "full_name": professor.full_name,
            "star_rating": starScore  # Optional star representation
        })

    return JsonResponse(professorRatings, safe=False)



def avgInstance(request, professorId, moduleCode):
    try:
        professor = Professor.objects.get(professor_code=professorId)
        module = Module.objects.get(module_code=moduleCode)

        moduleInstances = module.moduleinstance_set.filter(professors=professor)

        avgRating = Rating.objects.filter(module_instance__in=moduleInstances).aggregate(Avg('score'))['score__avg']
        avgRating = round(avgRating) if avgRating is not None else 0

        starScore = "*" * avgRating

        return JsonResponse({
            "professor": professor.full_name,
            "module": module.module_name,
            "average_rating": starScore
        })

    except Professor.DoesNotExist:
        return JsonResponse({"error": "Professor not found"}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({"error": "Module not found"}, status=404)

@login_required
@csrf_exempt
def rateInstance(request):
    try:
        data = json.loads(request.body)
        professorId = data.get("professor_id")
        moduleCode = data.get("module_code")
        year = data.get("year")
        semester = data.get("semester")
        rating = data.get("rating")

        if not all([professorId, moduleCode, year, semester, rating]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if not (1 <= rating <= 5):
            return JsonResponse({"error": "Rating must be between 1 and 5"}, status=400)

        professor = Professor.objects.get(professor_code=professorId)
        module = Module.objects.get(module_code=moduleCode)

        moduleInstance = ModuleInstance.objects.filter(
            module=module, year=year, semester=semester, professors__id=professor.id
        ).first()

        if not moduleInstance:
            return JsonResponse({"error": "Module instance not found for given professor, module, year, and semester"}, status=404)

        user = request.user

        newRating = Rating.objects.create(
            user=user,
            module_instance=moduleInstance,
            score=rating
        )

        return JsonResponse({"message": "Rating successfully recorded", "rating_id": newRating.id}, status=200)

    except Professor.DoesNotExist:
        return JsonResponse({"error": "Professor not found"}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({"error": "Module not found"}, status=404)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

