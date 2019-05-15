#! /usr/bin/env python3
import logging
from json import loads
from biowardrobe_migration.utils.files import norm_path, get_broken_outputs
from biowardrobe_migration.templates.outputs import OUTPUT_TEMPLATES
from biowardrobe_migration.utils.templates import fill_template


logger = logging.getLogger(__name__)


def get_broken_experiments(connection):
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

    broken_experiments = {}
    for experiment in connection.fetchall(sql_query):
        try:
            logger.debug(f"Processing {experiment['uid']}")
            experiment.update(settings)
            experiment.update({
                "peak_type": "broad" if int(experiment['peak_type']) == 2 else "narrow",
                "outputs": loads(experiment['outputs']) if experiment['outputs'] and experiment['outputs'] != "null" else {}
            })
            experiment["outputs"]["promoter"] = experiment["outputs"]["promoter"] if "promoter" in experiment["outputs"] else 1000

            for template in OUTPUT_TEMPLATES[experiment['exp_id']][experiment['peak_type']]:
                experiment["outputs"].update(fill_template(template, experiment))

            broken_outputs,_ = get_broken_outputs(experiment["outputs"])
            if broken_outputs:
                broken_experiments.update({experiment['uid']: {"exp_type": experiment["exp_type"],
                                                               "exp_id": experiment["exp_id"],
                                                               "peak_type": experiment["peak_type"],
                                                               "broken_outputs": broken_outputs}})
        except Exception:
            logger.debug(f"Failed to process {experiment['uid']}")
    return broken_experiments


def get_statistics(broken_experiments, key="broken_outputs"):
    statistics = {}
    for e in broken_experiments.values():
        for k in e[key].keys():
            if k in statistics:
                statistics[k] += 1
            else:
                statistics[k] = 1
    return statistics