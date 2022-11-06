import re, json
from munch import DefaultMunch

class Context:

    input_file = './../../Scripts/JSON/interface_out.json'
    output_file = './../../Scripts/JSON/interface_in.json'

    def __init__(self):
        self.output = {}
        self.refresh()

    def callback(self):
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
        self.output.setdefault(action, {})
        self.output[action].setdefault(param['index'], param)
        self.callback()