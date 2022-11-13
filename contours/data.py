import numpy as np
import os, json


class Data:
    def __init__(self, name, folder, config=None):
        self.name, self.folder = name, folder
        self.config = {} if config is None else config
    def save_json(self, config=None):
        config = {**self.config, **({} if config is None else config)}
        config = {k : v.tolist() if isinstance(v, np.ndarray) else v for k,v in config.items()}
        json_file = os.path.join(self.folder, f'{self.name}.json')
        print(f'saving {json_file}')
        with open(json_file, 'w') as f:
            json.dump(config, f, indent=2)
    def save_data(self, data):
        file_name = os.path.join(self.folder, f'{self.name}.csv')
        print(f'saving {file_name}')
        np.savetxt(file_name, data)
    def save(self, data, config=None):
        self.save_json(config)
        self.save_data(data)

class DataFile(Data):
    def __init__(self, file_name, json_file=None):
        self.path, self.file = file_name, os.path.basename(file_name)
        self.json_file = f'{os.path.join(folder, name)}.json' if json_file is None else json_file
        folder, name = (os.path.dirname(file_name), os.path.splitext(self.file)[0])
        Data.__init__(self, name, folder, self.load_json())
    def load_data(self):
        print(f'loading {self.path}')
        return np.loadtxt(self.path)
    def load_json(self):
        print(f'loading {self.json_file}')
        with open(self.json_file, 'r') as f:
            config = json.load(f)
        return config
