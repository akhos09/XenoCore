import jinja2 as ji

class VgFileGenerator:
    def __init__(self):
        self.env = ji.Environment(
                    loader=ji.FileSystemLoader("./core/templates"),
                    trim_blocks=True,
                    lstrip_blocks=True
                    )
        
        self.template = self.env.get_template('test.j2')
        
        self.params = {
            "multi_machine": True,
            "machines": [
                {
                    "name": "web",
                    "box": "ubuntu/bionic64",
                    "synced_folder": {
                        "host": "./web_data",
                        "guest": "/vagrant_web"
                    },
                    "memory": 1024
                },
                {
                    "name": "db",
                    "box": "ubuntu/bionic64",
                    "memory": 2048
                }
            ]
        }
        self.output = self.template.render(**self.params)
    
    def render_template(self):
        with open('Vagrantfile', 'w') as f:
            f.write(self.output)

test = VgFileGenerator()
test.render_template()