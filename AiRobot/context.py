import json
from munch import DefaultMunch

from utils.actions import Actions
import numpy as np


class Context:

    # root_path = r"C:\Users\Milo\AppData\Roaming\Axolot Games\Scrap " \
    #             r"Mechanic\User\User_76561198130980987\Mods\Robot_Brain"
    # path = r"C:\Users\Milo\AppData\Roaming\Axolot Games\Scrap " \
    #        r"Mechanic\User\User_76561198130980987\Mods\Robot_Brain\Scripts\JSON"
    root_path = "."
    path = root_path + r"\Scripts\JSON"
    input_file = path + r"\interface_out.json"
    output_file = path + r"\interface_in.json"

    def __init__(self, read_only=False):
        self.read_only = read_only
        self.output = {}
        self.acceleration = None
        self.old_dict = None
        self.data_dict = None
        self.refresh()

    def update_differential_data(self):
        if self.old_dict is None: 
            self.old_dict = self.data_dict
        old_data = DefaultMunch.fromDict(self.old_dict)
        self.acceleration = self.data.vel - old_data.vel
        self.old_dict = self.data_dict

    def callback(self):
        if self.read_only: return
        open(self.output_file, 'w').write(json.dumps(self.output))

    def refresh(self):
        with open(self.input_file, 'r') as f:
            try:
                str_data = f.read()
                str_data = str_data[1:-2].replace('\\"', '"').replace("\\n", '')
                self.data_dict = json.loads(str_data)
                self.data = DefaultMunch.fromDict(self.data_dict)
                # self.update_differential_data()
            except Exception as e:
                print(e)

    def registerAction(self, action, param):
        self.output.pop(Actions.Disarm, None)
        self.output.setdefault(action, [])
        result = [i for i, item in enumerate(self.output[action]) if item['index'] == param['index']]
        if len(result) == 0:
            self.output[action].append(param)
        else:
            self.output[action][result[0]] = param

        self.callback()

    def clearAction(self):
        self.output.setdefault(Actions.Disarm, True)
        self.callback()