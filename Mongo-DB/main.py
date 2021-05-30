from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId  # if we don't use this, we get None returned when querying using ObjectId

cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = MongoClient(cluster)

print(client.list_database_names())  # To get the existing databases
db = client['testDatabase']  # We can either use a dictionary style or client.testDatabase
print(db.list_collection_names())  # To get the collections within the specific database

todo1 = {
    "name": "Mary",
    "text": "My first todo!",
    "status": "Open",
    "tags": ["Python", "Coding"],
    "date": datetime.datetime.utcnow()
}

# Lets put todo1 in todos collection
todos = db.todos  # We first get the collection
results = todos.insert_one(todo1)  # To insert one element we use insert_one

# Multiple elements
todos2 = [{
    "name": "Patrick",
    "text": "My second todo!",
    "status": "Open",
    "tags": ["Python", "Coding"],
    "date": datetime.datetime.utcnow()
},
    {
        "name": "Patrick",
        "text": "My third todo!",
        "status": "Open",
        "tags": ["Machine Learnig", "Coding"],
        "date": datetime.datetime.utcnow()
    }]

result = todos.insert_many(todos2) # This inserts multiple items

# To retrieve an item
result = todos.find_one() # Gets us the first item

# To get the specific ones
specific_result = todos.find_one({"text": "My third todo!"})  # We just need to pass the relevant key and value pairs

# To query through the nested items
result_from_array = todos.find_one({"tags": "Machine Learnig"})  # if we don't have the element it returns None

# To query using the object id, we need bson module (imported above)
result_from_id = todos.find_one({'_id': ObjectId('60b251047a56304de7fecb69')})

# Multiple results
results_from_all = todos.find({'name': "Patrick"})  # Returns an iterable

for result in results_from_all:
    print(result['text'])

# Counting the elements
print(todos.count_documents({}))

# Querying for a range
d = datetime.datetime(2021, 6, 1)  # Date here is June 1st
results = todos.find({"date": {"$lt": d}})  # This is the notation to get everything before the date
# To get after the date use notation "$gt"  (greater than)
for result in results:
    print(result)
    # Returns all the objects which was recorded before June 1st

# To delete a record from the database
deleted_resulted = todos.delete_one({"_id": ObjectId('60b24f8a7dd834d404cbcaf6')})
deleted_all = todos.delete_many({"name": "Patrick"}) # Deletes everything with the name "Patrick"

# We can also use the below code to delete everything from the database
todos.delete_many({})

# To update an item
update_result = todos.update_one({"tags": "Python"}, {"$set": {'status': 'Done'}})
unset_result = todos.update_one({"tags": "Python"}, {"$unset": {'status': None}})

# We can also set a value to a key which currently doesn't exist
set_result = todos.update_one({"tags": "Python"}, {"$set": {'status': "We are back baby!"}})