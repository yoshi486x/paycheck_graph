import pprint as pp

from pymongo import MongoClient

CLIENT_HOST = 'mongodb://localhost:27017/'
CLIENT_NAME = 'test_database'

class MongoModel(object):
    def __init__(self, db):
        self.db = db

    def get_mongo_profile(self):
        """Define DB"""
        client = MongoClient(CLIENT_HOST)
        self.db = client[CLIENT_NAME]


class RecordingModel(MongoModel):
    """Definition of class that generates ranking model to write to MongoDB"""
    def __init__(self):
        super().__init__(self)
        if True:
            self.get_mongo_profile()

    def injest_data_to_mongo(self, stack):
        """Insert data to DB"""
        db_stacks = self.db.stacks
        stack_id = db_stacks.insert_one(stack).inserted_id

        """Print to see the inserted data"""
        # print(stack_id, type(stack_id))
        # print("###############")
        pp.pprint(db_stacks.find_one({'_id': stack_id}))



def main(data):
    recording = RecordingModel()
    recording.injest_data_to_mongo(data)
    


if __name__ == "__main__":
    main()