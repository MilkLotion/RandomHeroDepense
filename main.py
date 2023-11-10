import json
from collections import defaultdict

file_path = "./units.json"

with open(file_path, 'r') as file:
    units = json.load(file)

def find_units_by_grade(grade_to_find):
    found_units = [unit['units'] for unit in units if unit['grade'] == grade_to_find][0]
    return found_units

def find_units_by_name(name_to_find):
    for unit_dict in units:
        for unit in unit_dict['units']:
            if 'name' in unit and unit['name'] == name_to_find:
                return unit
    return None

def find_grade_by_name(name_to_find):
    for unit_dict in units:
        for unit in unit_dict['units']:
            if 'name' in unit and unit['name'] == name_to_find:
                return unit_dict['grade']
    return None

def get_grade_unit_combines(target, cnt, targetGrade) :
    target_dict = find_units_by_name(target)

    if target_dict is None:
        print('해당 유닛은 존재하지 않습니다.')
        return None

    if target_dict.get('combines') is None :
        return None

    target_lower_units = target_dict['combines'].split('+')

    res = []

    for target_lower_unit in target_lower_units :
        if '*' in target_lower_unit :
            tlu_name, tlu_cnt = target_lower_unit.split('*')
        else:
            tlu_name = target_lower_unit
            tlu_cnt = 1

        tlu_grade = find_grade_by_name(tlu_name)

        if targetGrade == tlu_grade :
            res.append(
                {
                    'grade' : tlu_grade,
                    'name' : tlu_name,
                    'cnt' : int(tlu_cnt) * int(cnt)
                }
            )
        else :
            lowers = get_grade_unit_combines(tlu_name, int(tlu_cnt) * int(cnt), targetGrade)
            if lowers is not None :
                for lower in get_grade_unit_combines(tlu_name, int(tlu_cnt) * int(cnt), targetGrade):
                    res.append(lower)

    return res

def print_grade_unit(target) :
    strFormat = '%-6s | %s'

    units_of_grade = find_units_by_grade(target)

    if len(units_of_grade) > 0 :
        print('----- ' + target + ' 등급의 유닛 -----')
        for unit in units_of_grade :
            print(strFormat %(unit['name'], unit['combines']))

    else :
        print('해당 등급의 유닛은 존재하지 않습니다.')


def print_grade_unit_combines(target, targetGrade=None) :
    target_dict = find_units_by_name(target)

    if target_dict is None:
        print('해당 유닛은 존재하지 않습니다.')
        return


    if targetGrade is not None :
        print('----- ' + target + ' 유닛의 [' + targetGrade + '] 유닛 개수 -----')


    target_lower_units = target_dict['combines'].split('+')

    combineFormat = '[%s] %-6s | %s 개'
    lowers = []

    for target_lower_unit in target_lower_units :
        if '*' in target_lower_unit :
            tlu_name, tlu_cnt = target_lower_unit.split('*')
        else:
            tlu_name = target_lower_unit
            tlu_cnt = 1

        tlu_grade = find_grade_by_name(tlu_name)

        if(targetGrade is not None):
            if tlu_grade != targetGrade :
                # print(get_grade_unit_combines(tlu_name, tlu_cnt, targetGrade))
                res = get_grade_unit_combines(tlu_name, tlu_cnt, targetGrade)

                if res is None :
                    continue

                for _res in res:
                    # print(combineFormat % (_res['grade'], _res['name'], _res['cnt']))
                    lowers.append(
                        {
                            'grade' : _res['grade'],
                            'name' : _res['name'],
                            'cnt' : int(_res['cnt'])
                        }
                    )
            else :
                # print(combineFormat % (tlu_grade, tlu_name, tlu_cnt))
                lowers.append(
                    {
                        'grade' : tlu_grade,
                        'name' : tlu_name,
                        'cnt' : int(tlu_cnt)
                    }
                )
    merged_dict = defaultdict(int)

    for item in lowers:
        merged_dict[(item['grade'], item['name'])] += item['cnt']

    merged_list = [{'grade': key[0], 'name': key[1], 'cnt': value} for key, value in merged_dict.items()]

    # print(merged_list)
    for merged in merged_list :
        print(combineFormat % (merged['grade'], merged['name'], merged['cnt']))
    print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_grade_unit_combines('순양함', '스페셜')
    print_grade_unit_combines('순양함', '에픽')
    print_grade_unit_combines('순양함', '초월')
