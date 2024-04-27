class InMemoryDB:
    def __init__(self):
        self.db = {}
        self.transaction_data = {}
        self.transaction_active = False

    def get(self, key):
        if key in self.transaction_data:
            return self.transaction_data[key]
        elif key in self.db:
            return self.db[key]
        else:
            return None

    def put(self, key, value):
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.transaction_data[key] = value

    def begin_transaction(self):
        if self.transaction_active:
            raise Exception("A transaction is already in progress")
        self.transaction_active = True
        self.transaction_data = {}

    def commit(self):
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.db.update(self.transaction_data)
        self.transaction_active = False
        self.transaction_data = {}

    def rollback(self):
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.transaction_active = False
        self.transaction_data = {}


# Example usage
inmemoryDB = InMemoryDB()

# should return None, because A doesn't exist in the DB yet
print(inmemoryDB.get("A"))

# should throw an error because a transaction is not in progress
try:
    inmemoryDB.put("A", 5)
except Exception as e:
    print(str(e))

# starts a new transaction
inmemoryDB.begin_transaction()

# set's value of A to 5, but it's not committed yet
inmemoryDB.put("A", 5)

# should return None, because updates to A are not committed yet
print(inmemoryDB.get("A"))

# update A's value to 6 within the transaction
inmemoryDB.put("A", 6)

# commits the open transaction
inmemoryDB.commit()

# should return 6, that was the last value of A to be committed
print(inmemoryDB.get("A"))

# throws an error, because there is no open transaction
try:
    inmemoryDB.commit()
except Exception as e:
    print(str(e))

# throws an error because there is no ongoing transaction
try:
    inmemoryDB.rollback()
except Exception as e:
    print(str(e))

# should return None because B does not exist in the database
print(inmemoryDB.get("B"))

# starts a new transaction
inmemoryDB.begin_transaction()

# Set key B's value to 10 within the transaction
inmemoryDB.put("B", 10)

# Rollback the transaction - revert any changes made to B
inmemoryDB.rollback()

# Should return None because changes to B were rolled back
print(inmemoryDB.get("B"))