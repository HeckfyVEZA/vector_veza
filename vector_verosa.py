from docx2txt import process
from re import findall as f_all
import pandas as pd

def many_bl(blank,vals,name_file,BZ,key_cost,cvector_list,vector_podbor,rezerve_list): # Кусок кода, работающий с ВЕРОСАми  ЗДЕСЬ ОТСЛЕЖИВАЕМ НАЛИЧИЕ_ГЛИКОЛЯ
    #blanks = primary_ui("ВЕРОСА")["FolMon"].split(";") Скорее всего здесь передаём наши бланки
    all_infos = []
    i = 0

    info_blank = file_read(blank)
    for mini_info_blank in info_blank:
        mini_info_blank.append(round(mini_info_blank[3]/search_glic_ro(mini_info_blank[4], mini_info_blank[5]), 3))
        all_infos.append(mini_info_blank)
    i += 1

    for i in range(len(all_infos)):
            all_infos[i].append(f"ВЕКТОР-{vals[f'scheme{i}']}-{vals[f'valve{i}']}-{scheme_recognition(vals[f'valve{i}'], float(all_infos[i][7]))}-{vals[f'side{i}']}-С+")
            all_infos[i].append(int(vals[f'rez{i}']) if not (str(vals[f'scheme{i}']) in ['1', '3', '6', '6М'] or vals[f'valve{i}'] == "Ш") else 0)

    names_of, blocks, TOs, GnGs, Ts, Gs, GGs, Vs, short_blank, BZs, rezervs = [], [], [], [], [], [], [], [], [], [], []
    Glycol_found = []
    for item in all_infos:
        if len(item)>8:

            names_of.append(item[0])
            blocks.append(item[1])
            TOs.append(item[2])
            GnGs.append(item[3])
            Ts.append(item[4])
            Gs.append(item[5])
            Glycol_found.append(item[5])
            GGs.append(item[7])
            Vs.append(item[8])
            #BZs.append(item[6].split("/")[-1].split(" ")[0])
            BZs.append(BZ)
            short_blank.append(name_file)
            rezervs.append(0)

    if vector_podbor:
        Vs = cvector_list
        rezervs = rezerve_list

        
    allsis = {"Бланк": short_blank,
              "Блок": blocks,
             "Теплообменник": TOs,
            "Расход жидкости": GnGs,
                "Температура на входе": Ts,
                "Доля гликоля": Gs,
                 "Расход поправочный": GGs,
                    "Вектор": Vs,
                    "Номер БЗ": BZs,
                    "Резерв": rezervs}


    way = names_of[0].replace(names_of[0].split("/")[-1], "")
    df = pd.DataFrame(allsis)  

    #df.to_excel(f"C:\\Users\\kushhov\\Desktop\\vector-main\\ВЕКТОР ВЕРОСА.xlsx", index=False)
  
    df_cost = table_costs(BZs, key_cost, rezervs,Glycol_found) # Для формирования Таблиц-цен нужно: Номер БЗ, Вектор,Резерв,Путь,
    return df, df_cost

def scheme_recognition(valve, G): # Функция, выбирающая то, какую функцию мы будем использовать для определения полного названия ВЕКТОРа
    return TIH(G) if valve.lower() in ["ш", "шаровой"] else TIS(G)

def TIS(G:float): # Определяем типоразмер для схемы с седельным клапаном
    match G:
        case G if G < 500:
            return "1"
        case G if 500 <= G < 800:
            return "2"
        case G if 800 <= G < 1000:
            return "3"
        case G if 1000 <= G < 2000:
            return "4"
        case G if 2000 <= G < 3500:
            return "5"
        case G if 3500 <= G < 6000:
            return "6"
        case G if 6000 <= G < 10000:
            return "7"
        case G if 10000 <= G < 14000:
            return "8"
        case G if 14000 <= G < 22000:
            return "9"
        case G if 22000 <= G < 40000:
            return "10"
        case G if 40000 <= G < 60000:
            return "11"

def TIH(G:float): # Определяем типоразмер для схемы с шаровым клапаном
    match G:
        case G if G < 200:
            return "1А"
        case G if 200 <= G < 300:
            return "1Б"
        case G if 300 <= G < 500:
            return "1"
        case G if 500 <= G < 800:
            return "2"
        case G if 800 <= G < 1000:
            return "3"
        case G if 1000 <= G < 2000:
            return "4"
        case G if 2000 <= G < 3500:
            return "5"
        case G if 3500 <= G < 6000:
            return "6"
        case G if 6000 <= G < 10000:
            return "7"
        case G if 10000 <= G < 14000:
            return "8"

def table_costs(BZs, Vectors, Rezervs,Glycol_found): #здесь формируются цены
    #costs = [vector_cost(Vectors[i]) if  Rezervs[i] else 0 for i in range(len(Vectors))] #Для резерва цену пока не знаем, поэтому ноль
    costs = [vector_cost(Vectors[i]) for i in range(len(Vectors))]
    costs = [costs[i]*1.8 if Glycol_found[i] != 0 else costs[i] for i in range(len(costs))] #Для глюколя повышаем цену на 80%
    costs = [costs[i]*1.3 if Rezervs[i] else costs[i] for i in range(len(costs))] #Для резерва повышаем цену на 30%
    df = {"Бланк-Заказ":BZs,"Вектор": Vectors, "Стоимость в рублях с НДС": costs}
    df = pd.DataFrame(df)
    #pd.DataFrame(df).to_excel(f"C:\\Users\\kushhov\\Desktop\\vector-main\\ВЕКТОР цены.xlsx", index=False)    
    return df

def file_read(file): # Поиск информации в бланке ВЕРОСА
    all_info = [i for i in process(file).split("\n") if i] 
    all_vecs = []
    i = 0
    for item in all_info:
        if " ВНВ" in item or " ВОВ" in item:
            G, TO = float(f_all(r"[GV]ж=([0-9.,]+)", item.replace(",","."))[0]), f_all(r"(В[НО]В[0-9.\-]+)",item)[0]
            block_num = all_info[all_info.index(item)-1]
            g_s = f_all(r"ленгл: (\d+?)%", item)
            glycol = int(g_s[0]) / 100 if len(g_s) != 0 else 0
            tzhn = float(f_all(r"tжн\*?=(-?\d+[\.,]?\d*?)°C", item)[0].replace(",", "."))
            all_vecs.append(['z', block_num, TO, G, tzhn, glycol, 'z'])
        i += 1
    return all_vecs

def search_glic_ro(T, part): # Определяет плотность теплоносителя, основываясь на температуре и содержании гликоля
    df = {0: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-',
             11: '-', 12: '-', 13: '-', 14: 0.99987, 15: 0.99999, 16: 0.99973, 17: 0.99913, 18: 0.99823, 19: 0.99707, 20: 0.99567, 21: 0.99406, 
             22: 0.99224, 23: 0.99016, 24: 0.98807, 25: 0.98538, 26: 0.98269, 27: 0.98, 28: 0.97781, 29: 0.975, 30: 0.97183, 31: 0.968585, 32: 0.96534, 
             33: 0.96186, 34: 0.95838, 35: 0.96697, 36: 0.94811, 37: 0.942975, 38: 0.93784, 39: 0.93271, 40: 0.92757, 41: 0.922435, 42: 0.9173, 43: '-', 44: '-'}, 
             0.1: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: '-', 13: '-', 14: 1.017, 15: 1.016, 16: 1.015, 
            17: 1.014, 18: 1.013, 19: 1.011, 20: 1.009, 21: 1.008, 22: 1.006, 23: 1.004, 24: 1.001, 25: 0.998, 26: 0.996, 27: 0.993, 28: 0.99, 29: 0.988, 30: 0.985, 31: 0.981, 
            32: 0.978, 33: 0.975, 34: 0.967, 35: 0.965, 36: 0.963, 37: 0.959, 38: 0.955, 39: 0.951, 40: 0.947, 41: 0.939, 42: 0.929, 43: 0.919, 44: 0.909}, 
            0.2: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: '-', 13: 1.033, 14: 1.032, 15: 1.031, 16: 1.029, 
            17: 1.028, 18: 1.026, 19: 1.024, 20: 1.023, 21: 1.021, 22: 1.019, 23: 1.016, 24: 1.014, 25: 1.011, 26: 1.008, 27: 1.005, 28: 1.002, 29: 0.999, 30: 0.996, 
            31: 0.992, 32: 0.989, 33: 0.985, 34: 0.982, 35: 0.978, 36: 0.974, 37: 0.97, 38: 0.966, 39: 0.962, 40: 0.957, 41: 0.949, 42: 0.939, 43: 0.93, 44: 0.92}, 
            0.3: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: 1.05, 13: 1.049, 14: 1.048, 15: 1.046, 16: 1.044, 
            17: 1.043, 18: 1.041, 19: 1.038, 20: 1.04, 21: 1.034, 22: 1.031, 23: 1.028, 24: 1.025, 25: 1.023, 26: 1.02, 27: 1.016, 28: 1.013, 29: 1.01, 30: 1.007, 31: 1.003, 
            32: 0.999, 33: 0.995, 34: 0.992, 35: 0.988, 36: 0.984, 37: 0.98, 38: 0.976, 39: 0.972, 40: 0.967, 41: 0.958, 42: 0.949, 43: 0.94, 44: 0.93}, 
            0.37: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: 1.064, 12: 1.063, 13: 1.062, 14: 1.061, 15: 1.059, 16: 1.056, 
            17: 1.054, 18: 1.052, 19: 1.05, 20: 1.048, 21: 1.045, 22: 1.042, 23: 1.039, 24: 1.036, 25: 1.033, 26: 1.03, 27: 1.027, 28: 1.024, 29: 1.02, 30: 1.017, 31: 1.013, 
            32: 1.009, 33: 1.005, 34: 1.001, 35: 0.997, 36: 0.993, 37: 0.989, 38: 0.985, 39: 0.981, 40: 0.976, 41: 0.967, 42: 0.958, 43: 0.949, 44: 0.939}, 
            0.4: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: 1.072, 11: 1.071, 12: 1.069, 13: 1.067, 14: 1.066, 15: 1.064, 16: 1.061, 
            17: 1.059, 18: 1.056, 19: 1.055, 20: 1.052, 21: 1.05, 22: 1.046, 23: 1.043, 24: 1.04, 25: 1.037, 26: 1.034, 27: 1.031, 28: 1.028, 29: 1.024, 30: 1.021, 31: 1.017, 
            32: 1.013, 33: 1.009, 34: 1.005, 35: 1.001, 36: 0.997, 37: 0.993, 38: 0.989, 39: 0.985, 40: 0.98, 41: 0.971, 42: 0.962, 43: 0.953, 44: 0.943}, 
            0.415: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: 1.077, 10: 1.075, 11: 1.073, 12: 1.071, 13: 1.069, 14: 1.068, 15: 1.066, 16: 1.063, 
            17: 1.061, 18: 1.058, 19: 1.057, 20: 1.054, 21: 1.052, 22: 1.048, 23: 1.045, 24: 1.042, 25: 1.039, 26: 1.036, 27: 1.033, 28: 1.03, 29: 1.026, 30: 1.023, 31: 1.019, 
            32: 1.015, 33: 1.011, 34: 1.007, 35: 1.003, 36: 0.999, 37: 0.995, 38: 0.991, 39: 0.987, 40: 0.982, 41: 0.973, 42: 0.964, 43: 0.955, 44: 0.944}, 
            0.44: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: 1.08, 10: 1.079, 11: 1.078, 12: 1.076, 13: 1.074, 14: 1.072, 15: 1.07, 16: 1.067, 
            17: 1.065, 18: 1.062, 19: 1.06, 20: 1.057, 21: 1.054, 22: 1.051, 23: 1.047, 24: 1.044, 25: 1.041, 26: 1.038, 27: 1.035, 28: 1.033, 29: 1.028, 30: 1.025, 31: 1.021, 
            32: 1.017, 33: 1.013, 34: 1.009, 35: 1.005, 36: 1.001, 37: 0.997, 38: 0.993, 39: 0.989, 40: 0.984, 41: 0.975, 42: 0.966, 43: 0.957, 44: 0.945}, 
            0.465: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: 1.09, 8: 1.088, 9: 1.086, 10: 1.084, 11: 1.082, 12: 1.08, 13: 1.078, 14: 1.076, 15: 1.074, 16: 1.07, 
             17: 1.068, 18: 1.066, 19: 1.063, 20: 1.061, 21: 1.057, 22: 1.054, 23: 1.05, 24: 1.047, 25: 1.044, 26: 1.041, 27: 1.038, 28: 1.038, 29: 1.031, 30: 1.028, 31: 1.024, 
            32: 1.02, 33: 1.016, 34: 1.012, 35: 1.008, 36: 1.004, 37: 1, 38: 0.996, 39: 0.992, 40: 0.987, 41: 0.978, 42: 0.969, 43: 0.96, 44: 0.947}, 
             0.49: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: 1.096, 7: 1.094, 8: 1.092, 9: 1.09, 10: 1.088, 11: 1.086, 12: 1.084, 13: 1.082, 14: 1.08, 15: 1.078, 
            16: 1.075, 17: 1.073, 18: 1.07, 19: 1.067, 20: 1.064, 21: 1.061, 22: 1.057, 23: 1.054, 24: 1.051, 25: 1.048, 26: 1.044, 27: 1.041, 28: 1.037, 29: 1.034, 30: 1.03, 
            31: 1.026, 32: 1.022, 33: 1.018, 34: 1.014, 35: 1.01, 36: 1.006, 37: 1.002, 38: 0.998, 39: 0.992, 40: 0.985, 41: 0.978, 42: 0.971, 43: 0.963, 44: 0.948}, 
            0.5: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: 1.101, 7: 1.098, 8: 1.095, 9: 1.092, 10: 1.09, 11: 1.088, 12: 1.086, 13: 1.084, 14: 1.081, 15: 1.079, 
            16: 1.075, 17: 1.073, 18: 1.071, 19: 1.068, 20: 1.065, 21: 1.061, 22: 1.058, 23: 1.054, 24: 1.051, 25: 1.048, 26: 1.045, 27: 1.042, 28: 1.04, 29: 1.035, 30: 1.031, 
            31: 1.027, 32: 1.023, 33: 1.019, 34: 1.015, 35: 1.011, 36: 1.007, 37: 1.003, 38: 0.999, 39: 0.995, 40: 0.99, 41: 0.981, 42: 0.972, 43: 0.963, 44: 0.949}, 
            0.515: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: 1.105, 6: 1.103, 7: 1.1, 8: 1.097, 9: 1.094, 10: 1.092, 11: 1.09, 12: 1.088, 13: 1.086, 14: 1.083, 15: 1.081, 
            16: 1.077, 17: 1.075, 18: 1.073, 19: 1.07, 20: 1.067, 21: 1.063, 22: 1.06, 23: 1.056, 24: 1.053, 25: 1.05, 26: 1.047, 27: 1.044, 28: 1.042, 29: 1.037, 30: 1.033, 
            31: 1.029, 32: 1.025, 33: 1.021, 34: 1.017, 35: 1.013, 36: 1.009, 37: 1.005, 38: 1.001, 39: 0.997, 40: 0.992, 41: 0.983, 42: 0.974, 43: 0.965, 44: 0.951}, 
            0.54: {0: '-', 1: '-', 2: '-', 3: '-', 4: 1.112, 5: 1.109, 6: 1.107, 7: 1.105, 8: 1.102, 9: 1.099, 10: 1.096, 11: 1.094, 12: 1.092, 13: 1.09, 14: 1.087, 15: 1.085, 
            16: 1.082, 17: 1.079, 18: 1.076, 19: 1.073, 20: 1.07, 21: 1.067, 22: 1.063, 23: 1.06, 24: 1.057, 25: 1.054, 26: 1.05, 27: 1.047, 28: 1.043, 29: 1.04, 30: 1.036, 
            31: 1.032, 32: 1.028, 33: 1.024, 34: 1.02, 35: 1.016, 36: 1.012, 37: 1.008, 38: 1.004, 39: 0.997, 40: 0.99, 41: 0.983, 42: 0.976, 43: 0.967, 44: 0.953}, 
            0.565: {0: '-', 1: '-', 2: '-', 3: 1.118, 4: 1.115, 5: 1.112, 6: 1.11, 7: 1.108, 8: 1.105, 9: 1.103, 10: 1.1, 11: 1.098, 12: 1.095, 13: 1.093, 14: 1.09, 15: 1.088, 
            16: 1.085, 17: 1.083, 18: 1.08, 19: 1.077, 20: 1.074, 21: 1.071, 22: 1.067, 23: 1.064, 24: 1.061, 25: 1.058, 26: 1.054, 27: 1.051, 28: 1.047, 29: 1.043, 
            30: 1.039, 31: 1.035, 32: 1.031, 33: 1.027, 34: 1.023, 35: 1.019, 36: 1.015, 37: 1.011, 38: 1.007, 39: 1.003, 40: 0.998, 41: 0.989, 42: 0.979, 43: 0.97, 44: 0.954}, 
            0.6: {0: '-', 1: '-', 2: '-', 3: 1.121, 4: 1.119, 5: 1.117, 6: 1.115, 7: 1.112, 8: 1.11, 9: 1.108, 10: 1.105, 11: 1.103, 12: 1.101, 13: 1.098, 14: 1.095, 15: 1.092, 
            16: 1.09, 17: 1.087, 18: 1.084, 19: 1.081, 20: 1.078, 21: 1.074, 22: 1.071, 23: 1.067, 24: 1.064, 25: 1.061, 26: 1.058, 27: 1.054, 28: 1.051, 29: 1.047, 30: 1.043, 31: 1.039, 
            32: 1.035, 33: 1.031, 34: 1.027, 35: 1.023, 36: 1.019, 37: 1.015, 38: 1.011, 39: 1.007, 40: 1.002, 41: 0.992, 42: 0.983, 43: 0.974, 44: 0.957}, 
            0.68: {0: '-', 1: 1.138, 2: 1.135, 3: 1.132, 4: 1.129, 5: 1.127, 6: 1.125, 7: 1.122, 8: 1.12, 9: 1.118, 10: 1.115, 11: 1.112, 12: 1.109, 13: 1.107, 14: 1.104, 15: 1.1, 
            16: 1.097, 17: 1.094, 18: 1.091, 19: 1.087, 20: 1.084, 21: 1.08, 22: 1.077, 23: 1.074, 24: 1.07, 25: 1.067, 26: 1.064, 27: 1.06, 28: 1.057, 29: 1.053, 30: 1.049, 31: 1.045, 
            32: 1.041, 33: 1.065, 34: 1.033, 35: 1.029, 36: 1.025, 37: 1.021, 38: 1.017, 39: 1.013, 40: 1.008, 41: 0.999, 42: 0.99, 43: 0.98, 44: 0.97}, 
            0.7: {0: '-', 1: '-', 2: 1.137, 3: 1.135, 4: 1.132, 5: 1.13, 6: 1.127, 7: 1.125, 8: 1.123, 9: 1.12, 10: 1.117, 11: 1.114, 12: 1.112, 13: 1.109, 14: 1.106, 
            15: 1.102, 16: 1.099, 17: 1.096, 18: 1.093, 19: 1.089, 20: 1.086, 21: 1.082, 22: 1.079, 23: 1.076, 24: 1.072, 25: 1.069, 26: 1.065, 27: 1.062, 28: 1.058, 
            29: 1.055, 30: 1.051, 31: 1.047, 32: 1.043, 33: 1.074, 34: 1.035, 35: 1.031, 36: 1.027, 37: 1.023, 38: 1.018, 39: 1.014, 40: 1.01, 41: 1.001, 42: 0.992, 43: 0.982, 
            44: 0.973}, 0.8: {0: '-', 1: 1.151, 2: 1.148, 3: 1.145, 4: 1.143, 5: 1.14, 6: 1.137, 7: 1.134, 8: 1.132, 9: 1.129, 10: 1.126, 11: 1.123, 12: 1.12, 
            13: 1.117, 14: 1.114, 15: 1.111, 16: 1.108, 17: 1.105, 18: 1.101, 19: 1.097, 20: 1.094, 21: 1.09, 22: 1.087, 23: 1.084, 24: 1.08, 25: 1.076, 26: 1.072, 
            27: 1.068, 28: 1.065, 29: 1.061, 30: 1.057, 31: 1.053, 32: 1.049, 33: 1.046, 34: 1.042, 35: 1.038, 36: 1.033, 37: 1.029, 38: 1.025, 39: 1.021, 40: 1.017, 
            41: 1.008, 42: 0.999, 43: 0.99, 44: 0.981}, 0.9: {0: '-', 1: '-', 2: 1.158, 3: 1.156, 4: 1.153, 5: 1.15, 6: 1.147, 7: 1.144, 8: 1.141, 9: 1.138, 10: 1.135, 
            11: 1.132, 12: 1.129, 13: 1.125, 14: 1.122, 15: 1.118, 16: 1.115, 17: 1.112, 18: 1.108, 19: 1.104, 20: 1.101, 21: 1.094, 22: 1.092, 23: 1.091, 24: 1.087, 
            25: 1.084, 26: 1.08, 27: 1.076, 28: 1.072, 29: 1.068, 30: 1.065, 31: 1.061, 32: 1.058, 33: 1.053, 34: 1.049, 35: 1.045, 36: 1.041, 37: 1.037, 38: 1.033, 39: 1.03, 
            40: 1.026, 41: 1.016, 42: 1.007, 43: 0.998, 44: 0.989}, 1: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: 1.143, 11: 1.139, 
            12: 1.136, 13: 1.132, 14: 1.128, 15: 1.125, 16: 1.121, 17: 1.118, 18: 1.114, 19: 1.111, 20: 1.107, 21: 1.104, 22: 1.1, 23: 1.097, 24: 1.094, 25: 1.09, 26: 1.086, 
            27: 1.082, 28: 1.079, 29: 1.075, 30: 1.071, 31: 1.067, 32: 1.064, 33: 1.06, 34: 1.056, 35: 1.052, 36: 1.048, 37: 1.044, 38: 1.04, 39: 1.036, 40: 1.032, 41: 1.023, 
            42: 1.015, 43: 1.006, 44: 0.996}}
    
    root_df = {-70: 0, -65: 1, -60: 2, -55: 3, -50: 4, -45: 5, -40: 6, -35: 7, -30: 8, -25: 9, -20: 10, -15: 11, -10: 12, 
               -5: 13, 0: 14, 5: 15, 10: 16, 15: 17, 20: 18, 25: 19, 30: 20, 35: 21, 40: 22, 45: 23, 50: 24, 55: 25, 60: 26, 65: 27, 70: 28, 75: 29, 80: 30, 85: 31, 
               90: 32, 95: 33, 100: 34, 105: 35, 110: 36, 115: 37, 120: 38, 125: 39, 130: 40, 140: 41, 150: 42, 160: 43, 170: 44}
    try:
        ro = df[part][root_df[T]]
        return ro
    except:
        if T not in root_df.keys():
            notT, Td, Tu = True, T, T
            for item in root_df.keys():
                if T > item:
                    Td = item
                elif T < item:
                    Tu = item
                    temps = [Td, Tu]
                    break
        else:
            notT = False
        if part not in df.keys():
            notpart, partd, partu = True, part, part
            for item in df.keys():
                if part > item:
                    partd = item
                elif part < item:
                    partu = item
                    parts = [partd, partu]
                    break
        else:
            notpart = False
        if all([notT, notpart]):
            rolu = search_glic_ro(temps[0], parts[0])
            roru = search_glic_ro(temps[0], parts[1])
            rold = search_glic_ro(temps[1], parts[0])
            rord = search_glic_ro(temps[1], parts[1])
            rou = roru + ((rolu - roru)*((T-temps[0])/(temps[1] - temps[0])))
            rod = rord + ((rold - rord)*((T-temps[0])/(temps[1] - temps[0])))
            ro = rou + (((rod - rou)*((part-parts[0])/(parts[1] - parts[0]))))
            return ro
        elif notT:
            rou = search_glic_ro(temps[0], part)
            rod = search_glic_ro(temps[1], part)
            ro = rou + ((rod-rou)*((T-temps[0])/(temps[1] - temps[0])))
            return ro
        elif notpart:
            rou = search_glic_ro(T, parts[0])
            rod = search_glic_ro(T, parts[1])
            ro = rou + ((rod-rou)*((part-parts[0])/(parts[1] - parts[0])))
            return ro

def vector_cost(vector):
    costs = {'1-С-1': [35057.64609745312, 987.349745420188], 
             '1-С-2': [35238.15768959952, 987.349745420188], 
             '1-С-3': [35269.87086325758, 987.349745420188], 
             '1-С-4': [35950.79434747794, 1041.205186079471], 
             '1-С-5': [36969.13478643999, 1045.5435410214689], 
             '1-С-6': [39683.39995457348, 1108.374888457299], 
             '1-С-7': [45676.383454197756, 1268.2956275261142], 
             '1-С-8': [50589.672040737234, 1246.3046559235738], 
             '1-С-9': [63080.31834465491, 1246.3046559235738], 
             '2-С-1': [41891.44335921299, 1117.2011967875703], 
             '2-С-2': [41989.0575391156, 1204.7162878589054], 
             '2-С-3': [41971.1588450607, 1204.7162878589054], 
             '2-С-4': [43198.09548631178, 1145.1761062411424], 
             '2-С-5': [44536.69294114351, 1168.3638654138892], 
             '2-С-6': [51038.188588700206, 1280.8618970132802], 
             '2-С-7': [58098.832982450534, 1424.0276100992075], 
             '2-С-8': [94223.84413269396, 1403.0838276205975], 
             '2-С-9': [116293.61985171704, 1976.7938690882372], 
             '2-С-10': [135729.65972653904, 1923.9856175528848], 
             '2-С-11': [171262.67207833336, 2304.7136633247605], 
             '3-С-1': [40274.14871458903, 1085.0375308382763], 
             '3-С-2': [39875.57622020369, 1109.4220775812296], 
             '3-С-3': [39926.52305949266, 1109.4220775812296], 
             '3-С-4': [40548.3966487217, 1080.9983727888302], 
             '3-С-5': [41261.451988640736, 1091.3206655818594], 
             '3-С-6': [42569.447639298385, 1156.9943834969295], 
             '3-С-7': [48031.82090442671, 1260.366909873498], 
             '3-С-8': [54821.189908055036, 1201.7243189333894], 
             '3-С-9': [67297.78247411526, 1491.9453047084146], 
             '3-С-10': [92698.2940833871, 1505.4091648732353], 
             '3-С-11': [123319.78443011346, 2027.6573408220045], 
             '4-С-1': [46585.31381055441, 1684.3289066190755], 
             '4-С-2': [45982.65944414104, 1707.3670673455465], 
             '4-С-3': [46081.12944414104, 1707.3670673455465], 
             '4-С-4': [46416.12895060667, 1594.1210435147766], 
             '4-С-5': [47992.84520877821, 1511.5427011705424], 
             '4-С-6': [53408.61720933065, 1714.2485958742325], 
             '4-С-7': [60303.43791946911, 1939.8430528581182], 
             '4-С-8': [97662.27864406249, 1963.778804262244], 
             '4-С-9': [120788.40216787187, 2448.0289748569635], 
             '4-С-10': [159912.96993847023, 2448.0289748569635], 
             '4-С-11': [199746.42792935792, 2448.0289748569635], 
             '4М-С-1': [47006.100659724776, 1272.4843840218364],
             '4М-С-2': [46436.07669448882, 1554.477455251693], 
             '4М-С-3': [46436.07669448882, 1554.477455251693], 
             '4М-С-4': [47314.37765563679, 1309.4352002519556], 
             '4М-С-5': [47258.4269988635, 1191.2524276940844], 
             '4М-С-6': [52519.643999126645, 1550.438297202247], 
             '4М-С-7': [59364.65924061838, 1550.438297202247], 
             '4М-С-8': [97797.45214244333, 1963.778804262244], 
             '4М-С-9': [120809.59829656399, 2043.0659807884103], 
             '4М-С-10': [157652.44295619364, 2692.7720329641493], 
             '4М-С-11': [198901.94040655813, 2692.7720329641493], 
             '5-С-1': [42464.304702401285, 1148.6168705054854], 
             '5-С-2': [42005.35472343386, 1145.62490157997], 
             '5-С-3': [41994.854723433855, 1145.62490157997], 
             '5-С-4': [43113.50735085749, 1113.9100309695032], 
             '5-С-5': [43714.70289225225, 1116.3036061099156], 
             '5-С-6': [48262.42071119953, 1290.1370006823793], 
             '5-С-7': [56075.34985206057, 1457.6872605112594], 
             '5-С-8': [91720.03898679322, 1602.648154952496], 
             '5-С-9': [112048.7645272423, 1809.5428061519083],
             '5-С-10': [150939.82299389684, 1809.5428061519083], 
             '5-С-11': [194884.95033826417, 2629.6414886357675], 
             '5М-С-1': [46059.95187244376, 1471.4503175686318], 
             '5М-С-2': [45634.96422434863, 1471.4503175686318], 
             '5М-С-3': [45573.16422434864, 1471.4503175686318], 
             '5М-С-4': [45411.17139427414, 1292.23137893024], 
             '5М-С-5': [46344.84836962588, 1143.5305233321087], 
             '5М-С-6': [51327.857240449506, 1533.6832712193589], 
             '5М-С-7': [58584.85595129775, 1533.6832712193589], 
             '5М-С-8': [96672.58474727465, 1741.9243084352531], 
             '5М-С-9': [117507.86539375971, 2177.2557870977907], 
             '5М-С-10': [155946.184090778, 2176.6573933126874], 
             '5М-С-11': [205067.33685822226, 2629.6414886357675], 
             '2-Ш-1А': [17276.094035585054, 128.90649595970197], 
             '2-Ш-1Б': [17300.574035585054, 128.90649595970197], 
             '2-Ш-1': [14356.206940183652, 137.28093189211882], 
             '2-Ш-2': [14361.454080492185, 137.28093189211882], 
             '2-Ш-3': [14357.20694018365, 137.28093189211882], 
             '2-Ш-4': [17239.52115856228, 133.09371392591038], 
             '2-Ш-5': [17239.52115856228, 133.09371392591038], 
             '2-Ш-6': [18913.780243461013, 133.09371392591038], 
             '2-Ш-7': [25550.571526201078, 509.6442438870816], 
             '2-Ш-8': [59578.41095895477, 509.6442438870816], 
             '4-Ш-1А': [17651.201571056776, 202.7809843635219], 
             '4-Ш-1Б': [17651.201571056776, 202.7809843635219], 
             '4-Ш-1': [14816.559924797984, 202.7809843635219], 
             '4-Ш-2': [14827.434924797984, 202.7809843635219], 
             '4-Ш-3': [14828.434924797986, 202.7809843635219], 
             '4-Ш-4': [18331.57453126246, 202.7809843635219], 
             '4-Ш-5': [18350.848064686747, 202.7809843635219], 
             '4-Ш-6': [18543.110675663764, 202.7809843635219], 
             '4-Ш-7': [24311.74977459125, 595.332668695561], 
             '4-Ш-8': [63619.87150675621, 837.144506244097], 
             '5-Ш-1А': [17878.3786688939, 149.3939552943646], 
             '5-Ш-1Б': [17878.3786688939, 149.3939552943646], 
             '5-Ш-1': [14725.055441314935, 149.3939552943646], 
             '5-Ш-2': [14257.841179587576, 149.3939552943646], 
             '5-Ш-3': [14269.255441314936, 149.3939552943646], 
             '5-Ш-4': [17097.174723506138, 149.54349879315774], 
             '5-Ш-5': [17123.68085532585, 149.54349879315774], 
             '5-Ш-6': [17847.099761821806, 149.54349879315774], 
             '5-Ш-7': [23878.532223167174, 304.02193304648966], 
             '5-Ш-8': [59964.270285272316, 304.02193304648966], 
             '5М-Ш-1А': [19204.166651179556, 144.6], 
             '5М-Ш-1Б': [19204.166651179556, 144.6], 
             '5М-Ш-1': [15921.837205734077, 144.6], 
             '5М-Ш-2': [15921.837205734077, 144.6], 
             '5М-Ш-3': [15922.837205734077, 144.6], 
             '5М-Ш-4': [18722.38843513905, 144.6], 
             '5М-Ш-5': [18722.38843513905, 144.6], 
             '5М-Ш-6': [20620.027743771647, 144.6],
             '5М-Ш-7': [23129.89851454298, 485.84999999999997],
             '5М-Ш-8': [58532.64755618429, 484.95], 
             '6-Ш-4': [9862.903074025606, 175.26498058558087], 
             '6-Ш-5': [9864.00193014902, 175.26498058558087], 
             '6-Ш-6': [11385.502983291006, 218.3335082380103], 
             '6-Ш-7': [12538.162560797564, 218.93168223318293], 
             '6-Ш-8': [18440.34025392801, 263.79473187113024], 
             '6М-Ш-4': [13226.930199586526, 288.91803966838074], 
             '6М-Ш-5': [13228.930199586526, 288.91803966838074], 
             '6М-Ш-6': [14806.806622074719, 292.2079966418302], 
             '6М-Ш-7': [15975.439757247354, 292.2079966418302], 
             '6М-Ш-8': [20346.786966495965, 321.81760940287546]}
    try:
            #key = "-".join(vector.split("-")[1:4])
            cost = costs[vector.upper()]
            FSZN = 0.35 * cost[1]
            BELGOSSTRAH = 0.0047 * cost[1]
            OBSH_RASH = 0.26 * cost[0]
            PROIZV_SELFCOST = cost[0] + cost[1] + FSZN + BELGOSSTRAH + OBSH_RASH
            REALIZE_RASH = 0.02 * cost[0]
            FULL_SELFCOST = PROIZV_SELFCOST + REALIZE_RASH
            OTPUSKN_COST = 1.25 * FULL_SELFCOST
            RENTAB = OTPUSKN_COST - FULL_SELFCOST
            OTPUSKN_COST_35 = OTPUSKN_COST * 100 / 65
            FILIAL_SKIDKA = OTPUSKN_COST_35 - OTPUSKN_COST
            NDS = 0.2 * OTPUSKN_COST_35
            WITH_NDS = NDS + OTPUSKN_COST_35
            return round(WITH_NDS, 2)
    except:
            return 'error'