#! /usr/bin/env python3
import logging
from json import loads
from biowardrobe_migration.utils.files import norm_path, get_broken_outputs
from biowardrobe_migration.templates.outputs import OUTPUT_TEMPLATES
from biowardrobe_migration.utils.templates import fill_template


logger = logging.getLogger(__name__)


def scan_outputs(connection):
    settings = connection.get_settings_data()
    sql_query = """SELECT
                         l.uid                    as uid,
                         l.params                 as outputs,
                         e.etype                  as exp_type,
                         e.id                     as exp_id,
                         COALESCE(a.properties,0) as peak_type
                   FROM  labdata l
                   INNER JOIN (experimenttype e) ON (e.id=l.experimenttype_id)
                   LEFT JOIN (antibody a) ON (l.antibody_id=a.id)
                   WHERE (l.deleted=0)                 AND
                         (l.libstatus=12)              AND
                         COALESCE(l.egroup_id,'')<>''  AND
                         COALESCE(l.name4browser,'')<>''"""

    collected_broken_outputs = {}
    for experiment in connection.fetchall(sql_query):
        try:
            
            experiment.update(settings)
            experiment.update({
                "peak_type": "broad" if int(experiment['peak_type']) == 2 else "narrow",
                "outputs": loads(experiment['outputs']) if experiment['outputs'] and experiment['outputs'] != "null" else {}
            })
            experiment["outputs"]["promoter"] = experiment["outputs"]["promoter"] if "promoter" in experiment["outputs"] else 1000

            for template in OUTPUT_TEMPLATES[experiment['exp_id']][experiment['peak_type']]:
                experiment["outputs"].update(fill_template(template, experiment))

            broken,_ = get_broken_outputs(experiment["outputs"])
            if broken:
                collected_broken_outputs.update({experiment['exp_id']: {"data": experiment, "broken": broken} })

        except Exception:
            logger.debug(f"Failed to updated params for {kwargs['uid']}")
    return collected_broken_outputs