from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.parsers import JSONParser
from demo.models import User, Transaction
from demo.serializers import UserSerializer, TransactionSerializer
from django.db import transaction as db_transaction

# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def user_route(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})
        
    if request.method == 'POST':
        # Form submission handling
        name = request.POST.get('name')
        username = request.POST.get('username')
        balance = request.POST.get('balance')

        if not name or not username or balance is None:
            return render(request, 'users.html', {
                'users': User.objects.all(),
                'error': 'Missing required fields'
            })
        
        try:
            balance = float(balance)
            user = User.objects.create(name=name, username=username, balance=balance)
            return redirect('users')
        except ValueError:
            return render(request, 'users.html', {
                'users': User.objects.all(),
                'error': 'Invalid balance value'
            })
    
@csrf_exempt
def get_user_by_id(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)
        other_users = User.objects.exclude(id=id)
        return render(request, 'user_detail.html', {'user': user, 'users': other_users})

@csrf_exempt
def transaction_route(request):
    # Show all transactions and a form to create a new one
    transactions = Transaction.objects.all().order_by('-date')
    users = User.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions, 'users': users})

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender')
        receiver_id = request.POST.get('receiver')
        amount_str = request.POST.get('amount')
        description = request.POST.get('description')
        
        # Validate input
        if not sender_id or not receiver_id or not amount_str or not description:
            return render(request, 'transactions.html', {
                'transactions': Transaction.objects.all().order_by('-date'),
                'users': User.objects.all(),
                'error': 'Missing required fields for transaction'
            })
            
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            amount = float(amount_str)
            
            # Make sure sender has enough balance
            if sender.balance < amount:
                return render(request, 'transactions.html', {
                    'transactions': Transaction.objects.all().order_by('-date'),
                    'users': User.objects.all(),
                    'error': f'Insufficient balance for {sender.name}. Current balance: ${sender.balance}'
                })
                
            # Make sure sender and receiver are different
            if sender.id == receiver.id:
                return render(request, 'transactions.html', {
                    'transactions': Transaction.objects.all().order_by('-date'),
                    'users': User.objects.all(),
                    'error': 'Sender and receiver cannot be the same user'
                })
                
            # Create transaction and update balances atomically
            with db_transaction.atomic():
                # Create the transaction
                transaction = Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    description=description
                )
                
                # Update balances
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()
            
            # Redirect based on where the form was submitted from
            referer = request.META.get('HTTP_REFERER', '')
            if f'/users/{sender.id}/' in referer:
                return redirect('get_user', id=sender.id)
            else:
                return render(request, 'transactions.html', {
                    'transactions': Transaction.objects.all().order_by('-date'),
                    'users': User.objects.all(),
                    'success': 'Transaction created successfully'
                })
                
        except User.DoesNotExist:
            return render(request, 'transactions.html', {
                'transactions': Transaction.objects.all().order_by('-date'),
                'users': User.objects.all(),
                'error': 'User not found'
            })
        except ValueError:
            return render(request, 'transactions.html', {
                'transactions': Transaction.objects.all().order_by('-date'),
                'users': User.objects.all(),
                'error': 'Invalid amount value'
            })
        except Exception as e:
            return render(request, 'transactions.html', {
                'transactions': Transaction.objects.all().order_by('-date'),
                'users': User.objects.all(),
                'error': f'Error creating transaction: {str(e)}'
            })
            
    # If not POST, redirect to transactions page
    return redirect('transactions')

