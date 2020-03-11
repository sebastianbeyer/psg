import jinja2


class ExpWriter:
    """
    Write the experiment to the output file
    """
    def __init__(self, templatePath, templateName):
        self.loader = jinja2.FileSystemLoader(searchpath=templatePath)
        self.env = jinja2.Environment(loader=self.loader,
                                      trim_blocks=True,
                                      undefined=jinja2.StrictUndefined)

        tempate_file = templateName
        self.template = self.env.get_template(tempate_file)

    def write(self, out_file, exp_data):
        self.template.stream(exp_data).dump(out_file)
