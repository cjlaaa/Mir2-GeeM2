import os
import pprint

from items_data import equipment_data
from items_data import potions_data
from items_data import equipment_group_order

if __name__ == '__main__':
    # output_directory = 'D:\MirServer\Mir200\Envir\MonItems'
    output_directory = 'MonItems'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    drops_data_auto = []

    directory_path = 'D:\MirServer\Mir200\Envir\MonItems'
    # directory_path = 'src'
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)

            # drops: {
            # Gold: [[num, rate], [num, rate]],
            # Potions: [[id, rate], [id, rate]],
            # equipment: {B1: [[name, rate], [name, rate]], B2: [[name, rate], [name, rate]],}
            # Others: [[name, rate], [name, rate]]
            # }
            drops = {}
            with open(file_path, 'r', encoding='gbk') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue

                    line_text = ' '.join(line.split())
                    infos = line_text.split(' ')

                    if len(infos) <= 1:
                        continue

                    # 金币处理
                    if infos[1] == "金币":
                        if "Gold" not in drops:
                            drops["Gold"] = []

                        rate = infos[0].split('/')[1]
                        drops["Gold"].append([infos[2], rate])

                    else:
                        is_other = True

                        # 药水处理
                        group_id = None
                        for key, potions in potions_data.items():
                            if infos[1] in potions:
                                group_id = key
                                break  # 找到后退出循环
                        if group_id:
                            if "Potions" not in drops:
                                drops["Potions"] = []

                            rate = infos[0].split('/')[1]
                            drops["Potions"].append([group_id, rate, infos[1]])
                            is_other = False

                        # 装备处理
                        group_id = None
                        for key, equipment in equipment_data.items():
                            if infos[1] in equipment:
                                group_id = key
                                break  # 找到后退出循环
                        if group_id:
                            if "equipment" not in drops:
                                drops["equipment"] = {}

                            if group_id not in drops["equipment"]:
                                drops["equipment"][group_id] = []

                            rate = infos[0].split('/')[1]
                            drops["equipment"][group_id].append([infos[1], rate])
                            is_other = False

                        # 其他处理
                        if is_other:
                            if "Others" not in drops:
                                drops["Others"] = []

                            rate = infos[0].split('/')[1]
                            drops["Others"].append([infos[1], rate])

                if not drops:
                    continue

                # 整理数据
                drops_data = [] # 爆率一键配置文件
                output_lines = [] # 爆率文件

                # 金币,爆率,数量 G,4,30
                if "Gold" in drops:
                    for gold in drops["Gold"]:
                        drops_data.append(f"G,{gold[1]},{gold[0]}")
                        output_lines.append(f"1/{gold[1]} 金币 {gold[0]}")
                output_lines.append("")

                # 药品,id,数量,爆率 P,R1,4,2
                potions_count = {}
                if "Potions" in drops:
                    for potions in drops["Potions"]:
                        if potions[0] not in potions_count:
                            potions_count[potions[0]] = {}
                        if potions[1] not in potions_count[potions[0]]:
                            potions_count[potions[0]][potions[1]] = 0
                        potions_count[potions[0]][potions[1]] += 1
                        output_lines.append(f"1/{potions[1]} {potions[2]}")
                    for id, values in potions_count.items():
                        for rate, num in values.items():
                            drops_data.append(f"P,{id},{num},{rate}")
                    output_lines.append("")

                # 装备组,爆率 B1,600
                if "equipment" in drops:
                    for group_id in equipment_group_order:
                        if group_id in drops["equipment"]:
                            values = drops["equipment"][group_id]
                            rate_max = 0
                            for name, rate in values:
                                if rate_max < int(rate):
                                    rate_max = int(rate)
                                output_lines.append(f"1/{rate} {name}")
                            output_lines.append("")
                            drops_data.append(f"{group_id},{rate_max}")

                # 其他物品,爆率,物品名 O,100,魔法头盔
                if "Others" in drops:
                    for other in drops["Others"]:
                        drops_data.append(f"O,{other[1]},{other[0]}")
                        output_lines.append(f"1/{other[1]} {other[0]}")

                # print(file_name, "|".join(drops_data))
                drops_data_str = "|".join(drops_data)
                drops_data_auto.append(f"{file_name}: {drops_data_str}")

                # if output_lines:
                #     print("\n".join(output_lines))
                #
                #     output_file_path = os.path.join(output_directory, f"{file_name}")
                #     with open(output_file_path, 'w', encoding='utf-8') as output_file:
                #         output_file.write("\n".join(output_lines))

    # print(drops_data_auto)
    if drops_data_auto:
        print("\n".join(drops_data_auto))

        output_file_path = os.path.join("", f"drops_data_auto.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(drops_data_auto))
