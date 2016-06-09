import csv
import json
from sympy import simplify

from .models import *
from sw_parser.com2us_mapping import *

# This routine expects two CSV files in the root of the project.
# One is the monster definition table and the other is the skill definition table in localvalue.dat


def assign_skill_ids():
    with open('monsters.csv', 'rb') as csvfile:
        monster_data = csv.DictReader(csvfile)

        for row in monster_data:
            monster_family = int(row['unit master id'][:3])
            awakened = row['unit master id'][3] == '1'
            element = element_map.get(int(row['unit master id'][-1:]))

            try:
                monster = Monster.objects.get(com2us_id=monster_family, is_awakened=awakened, element=element)
            except Monster.DoesNotExist:
                print 'Unable to find monster ' + str(row['unit master id'])
            else:
                skills = monster.skills.all().order_by('slot')
                skill_ids = json.loads(row['base skill'])

                if len(skills) != len(skill_ids):
                    print 'Error! ' + str(monster) + ' skill count in bestiary does not match CSV skill count'
                else:
                    for x, skill_id in enumerate(skill_ids):
                        if skills[x].com2us_id is None:
                            skills[x].com2us_id = skill_id
                            skills[x].save()
                            # print 'Updated ID of ' + str(skills[x])
                        elif skills[x].com2us_id != skill_id:
                            print 'Error! Skill ' + str(skills[x]) + ' already has an ID assigned. Tried to assign ' + str(skill_id)


def parse_skill_data():
    with open('skills.csv', 'rb') as csvfile:
        skill_data = csv.DictReader(csvfile)

        for csv_skill in skill_data:
            # Get matching skill in DB
            try:
                skill = Skill.objects.get(com2us_id=csv_skill['master id'])
            except Skill.DoesNotExist:
                print 'Unable to find skill ' + str(csv_skill['master id'])
            else:
                updated = False

                # Icon
                icon_nums = json.loads(csv_skill['thumbnail'])
                icon_filename = 'skill_icon_{0:04d}_{1}_{2}.png'.format(*icon_nums)
                if skill.icon_filename != icon_filename:
                    skill.icon_filename = icon_filename
                    updated = True

                # Cooltime
                cooltime = int(csv_skill['cool time']) if int(csv_skill['cool time']) > 0 else None

                if skill.cooltime != cooltime:
                    skill.cooltime = cooltime
                    updated = True

                # Max Level
                max_lv = int(csv_skill['max level'])
                if skill.max_level != max_lv:
                    skill.max_level = max_lv
                    updated = True

                # Level up progress
                level_up_desc = {
                    'DR': 'Effect Rate +{0}%',
                    'AT': 'Damage +{0}%',
                    'HE': 'Recovery +{0}%',
                    'TN': 'Cooltime Turn -{0}',
                    'SD': 'Shield +{0}%',
                }

                level_up_text = ''

                for level in json.loads(csv_skill['level']):
                    level_up_text += level_up_desc[level[0]].format(level[1]) + '\n'

                if skill.level_progress_description != level_up_text:
                    skill.level_progress_description = level_up_text
                    updated = True

                # Buffs
                # maybe this later. Data seems incomplete sometimes.

                # Scaling formula
                formula = ''
                formula_array = [''.join(map(str, scale)) for scale in json.loads(csv_skill['fun data'])]
                plain_operators = '+-*/'

                for operation in formula_array:
                    if operation not in plain_operators:
                        formula += '({0})'.format(operation)
                    else:
                        formula += '{0}'.format(operation)

                formula = simplify(formula)
                if skill.multiplier_formula != str(formula):
                    skill.multiplier_formula = str(formula)
                    updated = True

                # Finally save it if required
                if updated:
                    skill.save()
                    print 'Updated skill ' + str(skill)