from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=True)
    transactions = db.relationship("Transaction", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")
        self.balance = kwargs.get("balance", 0.0)


    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "balance": self.balance,
            "transactions": [transaction.serialize() for transaction in self.transactions]
        }
    
class Transaction(db.Model):
    """
    Transaction Model
    """
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, **kwargs):
        """
        Initialize a Transaction object
        """


    def serialize(self):
        """
        Serialize a Transaction object
        """

        return {
            "id": self.id,
        }