import json


class Data:
    def __init__(self):
        self.data = []
        self.load()

    def save(self):
        try:
            with open('../data/json/data.json', 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            print(f"Error while saving data: {e}")

    def load(self):
        try:
            with open('../data/json/data.json', 'r') as file:
                self.data = json.load(file)
        except Exception as e:
            print(f"Error while loading data: {e}")


# data = Data()
# data.load()
# for item in data.data:
#     if item['Type'] == 'Goal':
#         print(item['Data'][2]['Keyword'])
