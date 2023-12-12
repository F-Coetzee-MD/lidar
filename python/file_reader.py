import json

class FileReader:
    def load_json(self, json_file_path):
        with open(json_file_path, "r") as file:
            data = json.load(file)
            return data