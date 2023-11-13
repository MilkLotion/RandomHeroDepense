import json
from collections import defaultdict

class CombineMatrix :
    def __init__(self, file_path) :
        with open(file_path, 'r') as file:
            self.units = json.load(file)

    def find_units_by_grade(self, target):
        found_units = [unit['units'] for unit in self.units if unit['grade'] == target][0]
        return found_units

    def find_units_by_name(self, target):
        for unit_dict in self.units:
            for unit in unit_dict['units']:
                if 'name' in unit and unit['name'] == target:
                    return unit
        return None

    def find_grade_by_name(self, target):
        for unit_dict in self.units:
            for unit in unit_dict['units']:
                if 'name' in unit and unit['name'] == target:
                    return unit_dict['grade']
        return None

    def find_level_by_grade(self, target):
        for unit_dict in self.units:
            if 'grade' in unit_dict and unit_dict['grade'] == target:
                return unit_dict['level']
        return None

    def find_level_by_name(self, target):
        for unit_dict in self.units:
            for unit in unit_dict['units']:
                if 'name' in unit and unit['name'] == target:
                    return unit_dict['level']
        return None

    def get_grade_unit_combines(self, target, cnt, target_level) :
        target_dict = self.find_units_by_name(target)

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

            # tlu_grade = self.find_grade_by_name(tlu_name)
            tlu_level = self.find_level_by_name(tlu_name)

            if target_level < tlu_level :
                lowers = self.get_grade_unit_combines(tlu_name, int(tlu_cnt) * int(cnt), target_level)
                if lowers is not None :
                    for lower in self.get_grade_unit_combines(tlu_name, int(tlu_cnt) * int(cnt), target_level):
                        res.append(lower)
            else :
                res.append(
                    {
                        'grade' : self.find_grade_by_name(tlu_name),
                        'level' : tlu_level,
                        'name' : tlu_name,
                        'cnt' : int(tlu_cnt) * int(cnt)
                    }
                )

        return res

    # def print_grade_unit(target) :
    #     strFormat = '%-6s | %s'
    #
    #     units_of_grade = find_units_by_grade(target)
    #
    #     if len(units_of_grade) > 0 :
    #         print('----- ' + target + ' 등급의 유닛 -----')
    #         for unit in units_of_grade :
    #             print(strFormat %(unit['name'], unit['combines']))
    #
    #     else :
    #         print('해당 등급의 유닛은 존재하지 않습니다.')


    def print_grade_unit_combines(self, target, targetGrade) :
        target_dict = self.find_units_by_name(target)

        if target_dict is None:
            print('해당 유닛은 존재하지 않습니다.')
            return

        targetLevel = self.find_level_by_grade(targetGrade)
        target_lower_units = target_dict['combines'].split('+')
        combineFormat = '[%s] %-6s | %s 개'
        lowers = []

        print('----- ' + target + ' 유닛의 [' + targetGrade + '] 등급 이하의 유닛 개수 -----')

        for target_lower_unit in target_lower_units :
            if '*' in target_lower_unit :
                tlu_name, tlu_cnt = target_lower_unit.split('*')
            else:
                tlu_name = target_lower_unit
                tlu_cnt = 1

            tlu_grade = self.find_grade_by_name(tlu_name)
            tlu_level = self.find_level_by_name(tlu_name)

            if(targetLevel is not None):
                if tlu_level > targetLevel :
                    # print(get_grade_unit_combines(tlu_name, tlu_cnt, targetGrade))
                    res = self.get_grade_unit_combines(tlu_name, tlu_cnt, targetLevel)

                    if res is None :
                        continue

                    for _res in res:
                        # print(combineFormat % (_res['grade'], _res['name'], _res['cnt']))
                        lowers.append(
                            {
                                'grade' : _res['grade'],
                                'level' : _res['level'],
                                'name' : _res['name'],
                                'cnt' : int(_res['cnt'])
                            }
                        )
                else :
                    # print(combineFormat % (tlu_grade, tlu_name, tlu_cnt))
                    lowers.append(
                        {
                            'grade' : tlu_grade,
                            'level' : tlu_level,
                            'name' : tlu_name,
                            'cnt' : int(tlu_cnt)
                        }
                    )
        merged_dict = defaultdict(int)

        for item in lowers:
            merged_dict[(item['grade'], item['level'], item['name'])] += item['cnt']

        merged_list = [{'grade': key[0], 'level' : key[1], 'name': key[2], 'cnt': value} for key, value in merged_dict.items()]

        merged_list.sort(key=lambda dict: dict['level'], reverse=True)

        # print(merged_list)
        for merged in merged_list :
            print(combineFormat % (merged['grade'], merged['name'], merged['cnt']))
        print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    myCM = CombineMatrix('sc_random_hero_defense.json')

    # myCM.print_grade_unit_combines('순양함', '스페셜')
    # myCM.print_grade_unit_combines('순양함', '초월')
    
    myCM.print_grade_unit_combines('순양함', '스페셜')
    myCM.print_grade_unit_combines('군단케리건', '스페셜')
    myCM.print_grade_unit_combines('아몬', '스페셜')
