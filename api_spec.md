# API Specification

## Database

A correct implementation of the User model has been provided. Implement the following model with a many-to-one relationship with the User model.

### Transaction Model
Required Fields:
- ID (primary key)
- amount (float)
- sender id (foreign key)
- receiver id (foreign key)
- pending (boolean)

## Routes

The get all users route has been provided as an example. Please complete the following routes.

### Create user
``` POST /users/```
#### Request
```json
{
    "name": "Raahi Menon",
    "username": "raahi014",
    "balance": <USER INPUT (OPTIONAL INTEGER)>
}
```

#### Response
```json
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "name": "Raahi Menon",
    "username": "raahi014",
    "balance": <USER INPUT, OR 0 IF NOT PROVIDED>,
    "transactions": []
}
```

### Get user by ID
``` GET /users/<int:id>/```

#### Response
```json
<HTTP STATUS CODE 200>
{
    "id": <ID>,
    "name": "Raahi Menon",
    "username": "raahi014",
    "balance": <USER INPUT, OR 0 IF NOT PROVIDED>,
    "transactions": []
}
```

### Get all Transactions
``` GET /transactions/```

#### Response
```json
<HTTP STATUS CODE 200>
{
    transactions: [
        {
            "id": <ID>,
            "sender": "Larry Tao",
            "receiver": "Elizabeth Moon",
            "amount": 10.0,
            "date": "3/21/2025",
            "description": "test"
        }
    ]
}
```

### Create Transaction
``` POST /transactions/create/```

#### Response
```json
<HTTP STATUS CODE 201>

{
    "id": <ID>,
    "sender": "Larry Tao",
    "receiver": "Elizabeth Moon",
    "amount": 10.0,
    "date": "3/21/2025",
    "description": "test"
}
```

