from json import loads
from collections import OrderedDict


def fill_template(template, kwargs):
    template_object = loads(
        template
            .replace('\n', ' ')
            .format(**kwargs)
            .replace("'True'", 'true')
            .replace("'False'", 'false')
            .replace('"True"', 'true')
            .replace('"False"', 'false')
    )
    return OrderedDict(sorted(template_object.items()))
