import json
from munch import DefaultMunch

from python.PythonServer.AiRobot.utils.actions import Actions


class Context:

    input_file = '../../../Scripts/JSON/interface_out.json'
    output_file = '../../../Scripts/JSON/interface_in.json'

    def __init__(self, read_only=False):
        self.read_only = read_only
        self.output = {}
        self.refresh()

    def callback(self):
        if self.read_only: return
        open(self.output_file, 'w').write(json.dumps(self.output))

    def refresh(self):
        with open(self.input_file, 'r') as f:
            try:
                str_data = f.read()
                str_data = str_data[1:-2].replace('\\"', '"').replace("\\n", '')
                data_dict = json.loads(str_data)
                self.data = DefaultMunch.fromDict(data_dict)
            except Exception as e:
                print(e)

    def registerAction(self, action, param):
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