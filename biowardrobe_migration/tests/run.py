
#! /usr/bin/env python3
from json import loads
from biowardrobe_migration.tests.outputs import chipseq_se
from biowardrobe_migration.utils.files import norm_path, get_broken_locations


correct, broken = get_broken_locations(loads(chipseq_se))
print("CORERCT:", correct)
print("BROKEN:", broken)
