import os
from items_data import items_tables

if __name__ == '__main__':
    # output_directory = 'D:\MirServer\Mir200\Envir\MonItems'
    output_directory = 'MonItems'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open('drops_data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(';'):
                continue

            monster_name, values = line.split(':')
            groups = values.split('|')
            output_lines = []
            print(monster_name)
            output_lines.append(f";{monster_name}")

            for group in groups:
                infos = group.split(",")
                if infos[0] == "G":
                    output_lines.append(f"1/{infos[1]} 金币 {infos[2]}")
                    output_lines.append("")
                elif infos[0] == "E":
                    output_lines.append(f"1/{infos[1]} {infos[2]}")
                    output_lines.append("")
                else:
                    items = items_tables.get(infos[0], [])
                    for item in items:
                        output_lines.append(f"1/{infos[1]} {item}")
                    output_lines.append("")

            if output_lines:
                print("\n".join(output_lines))

                output_file_path = os.path.join(output_directory, f"{monster_name}.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write("\n".join(output_lines))