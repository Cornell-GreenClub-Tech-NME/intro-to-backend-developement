from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from demo.models import User
from demo.serializers import UserSerializer

# Create your views here.

@csrf_exempt
def user_route(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except Exception as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        name = data.get('name')
        username = data.get('username')
        balance = data.get('balance')

        if not name or not username or balance is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        user = User.objects.create(name=name, username=username, balance=balance)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False, status=201)
    
@csrf_exempt
def get_user_by_id(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User Not Found'}, status=404)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False, status=200)
        


@csrf_exempt
def transaction_route(request):
    # TODO: EXTRA CREDIT: Get all of a user's transactions
    pass