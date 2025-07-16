def interpret(code):
    locals_dict = {}
    locals_dict["сан"] = range  # "сан(3)" → range(3)
    functions = {}
    lines = code.strip().splitlines()
    i = 0
    skip_else = False  # Егер шарт орындалса — кейінгі 'әйтпесе' бөлімін өткізіп жіберу үшін

    while i < len(lines):
        line = lines[i].strip()

        # Бос жолдарды өткізіп жіберу
        if line == "":
            i += 1
            continue

        # Функция анықтау: анықтау қосу(a, b):
        if line.startswith("анықтау ") and line.endswith(":"):
            header = line[8:-1].strip()
            func_name = header.split("(")[0].strip()
            arg_list = header.split("(")[1].split(")")[0].strip().split(",")
            arg_list = [a.strip() for a in arg_list if a.strip()]

            # Келесі жол 'қайтару ...' болуы тиіс
            i += 1
            if i < len(lines) and lines[i].strip().startswith("қайтару "):
                return_expr = lines[i].strip()[8:]
                functions[func_name] = (arg_list, return_expr)
            else:
                print(f" Қате: {func_name} функциясында 'қайтару' табылмады.")
            i += 1
            continue

        # Айнымалыны меншіктеу: x = 5
        elif "=" in line and not line.startswith(("егер", "үшін")):
            left, right = line.split("=", 1)
            locals_dict[left.strip()] = eval_custom(right.strip(), locals_dict, functions)
            i += 1

        # Басып шығару: басып_шығар(...)
        elif line.startswith("басып_шығар(") and line.endswith(")"):
            content = line[len("басып_шығар("):-1]
            print(eval_custom(content, locals_dict, functions))
            i += 1

        # Шарт: егер ...:
        elif line.startswith("егер ") and line.endswith(":"):
            condition = line[5:-1]
            result = eval_custom(condition, locals_dict, functions)
            i += 1

            if i < len(lines):
                next_line = lines[i].strip()
                if result:
                    if next_line.startswith("басып_шығар("):
                        content = next_line[len("басып_шығар("):-1]
                        print(eval_custom(content, locals_dict, functions))
                    skip_else = True  # Шарт орындалды — 'әйтпесе' бөлімін өткіземіз
                    i += 1
                else:
                    skip_else = False  # Шарт орындалмады — 'әйтпесе' бөлімін орындауға болады

        # Әйтпесе: егер шарт орындалмаса орындалады
        elif line == "әйтпесе:":
            if skip_else:
                skip_else = False
                i += 2  # Әйтпесе және оның ішіндегі жолды өткізіп жіберу
            else:
                i += 1
                if i < len(lines):
                    else_line = lines[i].strip()
                    if else_line.startswith("басып_шығар("):
                        content = else_line[len("басып_шығар("):-1]
                        print(eval_custom(content, locals_dict, functions))
                    i += 1

        # Цикл: үшін i ішінде сан(3):
        elif line.startswith("үшін ") and " ішінде " in line and line.endswith(":"):
            loop_part = line[5:-1]
            var_name, loop_list = loop_part.split(" ішінде ")
            var_name = var_name.strip()
            iterable = eval_custom(loop_list.strip(), locals_dict, functions)

            i += 1
            if i < len(lines):
                inner_line = lines[i].strip()
                if inner_line.startswith("басып_шығар("):
                    for value in iterable:
                        locals_dict[var_name] = value
                        content = inner_line[len("басып_шығар("):-1]
                        print(eval_custom(content, locals_dict, functions))
                i += 1

        # Белгісіз немесе қате команда
        else:
            print("Қате анықталды!")
            print(f"Жол {i + 1}: {line}")
            print("Бұл жол түсініксіз. Мүмкін, синтаксис дұрыс емес немесе команда қолдау таппайды.")
            print("Кеңес: тексеріңіз — 'басып_шығар', 'егер', 'үшін', 'x = ...' немесе 'анықтау'\n")
            i += 1


# Мәнді есептейтін көмекші функция (функция шақыруды да өңдейді)
def eval_custom(expr, locals_dict, functions):
    expr = expr.strip()

    # Егер қолданушы функциясы болса (мысалы: қосу(2, 3))
    if "(" in expr and ")" in expr:
        name = expr.split("(", 1)[0].strip()
        if name in functions:
            args_str = expr.split("(", 1)[1].rsplit(")", 1)[0]
            args = [eval_custom(a.strip(), locals_dict, functions) for a in args_str.split(",") if a.strip()]
            arg_names, return_expr = functions[name]

            if len(args) != len(arg_names):
                raise ValueError(f"{name} функциясы {len(arg_names)} аргумент қабылдайды, бірақ {len(args)} берілді.")

            local_scope = dict(zip(arg_names, args))
            return eval(return_expr, {}, {**locals_dict, **local_scope})

    # Қарапайым Python өрнегін есептеу
    return eval(expr, {}, locals_dict)






