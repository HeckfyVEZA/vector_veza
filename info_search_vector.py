from docx2txt import process
from re import findall
import streamlit as st
def search_glic_ro(T, part): # Определяет плотность теплоносителя, основываясь на температуре и содержании гликоля
    df = {0: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: '-', 13: '-', 14: 0.99987, 15: 0.99999, 16: 0.99973, 17: 0.99913, 18: 0.99823, 19: 0.99707, 20: 0.99567, 21: 0.99406, 22: 0.99224, 23: 0.99016, 24: 0.98807, 25: 0.98538, 26: 0.98269, 27: 0.98, 28: 0.97781, 29: 0.975, 30: 0.97183, 31: 0.968585, 32: 0.96534, 33: 0.96186, 34: 0.95838, 35: 0.96697, 36: 0.94811, 37: 0.942975, 38: 0.93784, 39: 0.93271, 40: 0.92757, 41: 0.922435, 42: 0.9173, 43: '-', 44: '-'}, 0.1: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: '-', 13: '-', 14: 1.017, 15: 1.016, 16: 1.015, 17: 1.014, 18: 1.013, 19: 1.011, 20: 1.009, 21: 1.008, 22: 1.006, 23: 1.004, 24: 1.001, 25: 0.998, 26: 0.996, 27: 0.993, 28: 0.99, 29: 0.988, 30: 0.985, 31: 0.981, 32: 0.978, 33: 0.975, 34: 0.967, 35: 0.965, 36: 0.963, 37: 0.959, 38: 0.955, 39: 0.951, 40: 0.947, 41: 0.939, 42: 0.929, 43: 0.919, 44: 0.909}, 0.2: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: '-', 13: 1.033, 14: 1.032, 15: 1.031, 16: 1.029, 17: 1.028, 18: 1.026, 19: 1.024, 20: 1.023, 21: 1.021, 22: 1.019, 23: 1.016, 24: 1.014, 25: 1.011, 26: 1.008, 27: 1.005, 28: 1.002, 29: 0.999, 30: 0.996, 31: 0.992, 32: 0.989, 33: 0.985, 34: 0.982, 35: 0.978, 36: 0.974, 37: 0.97, 38: 0.966, 39: 0.962, 40: 0.957, 41: 0.949, 42: 0.939, 43: 0.93, 44: 0.92}, 0.3: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: '-', 12: 1.05, 13: 1.049, 14: 1.048, 15: 1.046, 16: 1.044, 17: 1.043, 18: 1.041, 19: 1.038, 20: 1.04, 21: 1.034, 22: 1.031, 23: 1.028, 24: 1.025, 25: 1.023, 26: 1.02, 27: 1.016, 28: 1.013, 29: 1.01, 30: 1.007, 31: 1.003, 32: 0.999, 33: 0.995, 34: 0.992, 35: 0.988, 36: 0.984, 37: 0.98, 38: 0.976, 39: 0.972, 40: 0.967, 41: 0.958, 42: 0.949, 43: 0.94, 44: 0.93}, 0.37: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: '-', 11: 1.064, 12: 1.063, 13: 1.062, 14: 1.061, 15: 1.059, 16: 1.056, 17: 1.054, 18: 1.052, 19: 1.05, 20: 1.048, 21: 1.045, 22: 1.042, 23: 1.039, 24: 1.036, 25: 1.033, 26: 1.03, 27: 1.027, 28: 1.024, 29: 1.02, 30: 1.017, 31: 1.013, 32: 1.009, 33: 1.005, 34: 1.001, 35: 0.997, 36: 0.993, 37: 0.989, 38: 0.985, 39: 0.981, 40: 0.976, 41: 0.967, 42: 0.958, 43: 0.949, 44: 0.939}, 0.4: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: 1.072, 11: 1.071, 12: 1.069, 13: 1.067, 14: 1.066, 15: 1.064, 16: 1.061, 17: 1.059, 18: 1.056, 19: 1.055, 20: 1.052, 21: 1.05, 22: 1.046, 23: 1.043, 24: 1.04, 25: 1.037, 26: 1.034, 27: 1.031, 28: 1.028, 29: 1.024, 30: 1.021, 31: 1.017, 32: 1.013, 33: 1.009, 34: 1.005, 35: 1.001, 36: 0.997, 37: 0.993, 38: 0.989, 39: 0.985, 40: 0.98, 41: 0.971, 42: 0.962, 43: 0.953, 44: 0.943}, 0.415: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: 1.077, 10: 1.075, 11: 1.073, 12: 1.071, 13: 1.069, 14: 1.068, 15: 1.066, 16: 1.063, 17: 1.061, 18: 1.058, 19: 1.057, 20: 1.054, 21: 1.052, 22: 1.048, 23: 1.045, 24: 1.042, 25: 1.039, 26: 1.036, 27: 1.033, 28: 1.03, 29: 1.026, 30: 1.023, 31: 1.019, 32: 1.015, 33: 1.011, 34: 1.007, 35: 1.003, 36: 0.999, 37: 0.995, 38: 0.991, 39: 0.987, 40: 0.982, 41: 0.973, 42: 0.964, 43: 0.955, 44: 0.944}, 0.44: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: 1.08, 10: 1.079, 11: 1.078, 12: 1.076, 13: 1.074, 14: 1.072, 15: 1.07, 16: 1.067, 17: 1.065, 18: 1.062, 19: 1.06, 20: 1.057, 21: 1.054, 22: 1.051, 23: 1.047, 24: 1.044, 25: 1.041, 26: 1.038, 27: 1.035, 28: 1.033, 29: 1.028, 30: 1.025, 31: 1.021, 32: 1.017, 33: 1.013, 34: 1.009, 35: 1.005, 36: 1.001, 37: 0.997, 38: 0.993, 39: 0.989, 40: 0.984, 41: 0.975, 42: 0.966, 43: 0.957, 44: 0.945}, 0.465: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: 1.09, 8: 1.088, 9: 1.086, 10: 1.084, 11: 1.082, 12: 1.08, 13: 1.078, 14: 1.076, 15: 1.074, 16: 1.07, 17: 1.068, 18: 1.066, 19: 1.063, 20: 1.061, 21: 1.057, 22: 1.054, 23: 1.05, 24: 1.047, 25: 1.044, 26: 1.041, 27: 1.038, 28: 1.038, 29: 1.031, 30: 1.028, 31: 1.024, 32: 1.02, 33: 1.016, 34: 1.012, 35: 1.008, 36: 1.004, 37: 1, 38: 0.996, 39: 0.992, 40: 0.987, 41: 0.978, 42: 0.969, 43: 0.96, 44: 0.947}, 0.49: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: 1.096, 7: 1.094, 8: 1.092, 9: 1.09, 10: 1.088, 11: 1.086, 12: 1.084, 13: 1.082, 14: 1.08, 15: 1.078, 16: 1.075, 17: 1.073, 18: 1.07, 19: 1.067, 20: 1.064, 21: 1.061, 22: 1.057, 23: 1.054, 24: 1.051, 25: 1.048, 26: 1.044, 27: 1.041, 28: 1.037, 29: 1.034, 30: 1.03, 31: 1.026, 32: 1.022, 33: 1.018, 34: 1.014, 35: 1.01, 36: 1.006, 37: 1.002, 38: 0.998, 39: 0.992, 40: 0.985, 41: 0.978, 42: 0.971, 43: 0.963, 44: 0.948}, 0.5: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: 1.101, 7: 1.098, 8: 1.095, 9: 1.092, 10: 1.09, 11: 1.088, 12: 1.086, 13: 1.084, 14: 1.081, 15: 1.079, 16: 1.075, 17: 1.073, 18: 1.071, 19: 1.068, 20: 1.065, 21: 1.061, 22: 1.058, 23: 1.054, 24: 1.051, 25: 1.048, 26: 1.045, 27: 1.042, 28: 1.04, 29: 1.035, 30: 1.031, 31: 1.027, 32: 1.023, 33: 1.019, 34: 1.015, 35: 1.011, 36: 1.007, 37: 1.003, 38: 0.999, 39: 0.995, 40: 0.99, 41: 0.981, 42: 0.972, 43: 0.963, 44: 0.949}, 0.515: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: 1.105, 6: 1.103, 7: 1.1, 8: 1.097, 9: 1.094, 10: 1.092, 11: 1.09, 12: 1.088, 13: 1.086, 14: 1.083, 15: 1.081, 16: 1.077, 17: 1.075, 18: 1.073, 19: 1.07, 20: 1.067, 21: 1.063, 22: 1.06, 23: 1.056, 24: 1.053, 25: 1.05, 26: 1.047, 27: 1.044, 28: 1.042, 29: 1.037, 30: 1.033, 31: 1.029, 32: 1.025, 33: 1.021, 34: 1.017, 35: 1.013, 36: 1.009, 37: 1.005, 38: 1.001, 39: 0.997, 40: 0.992, 41: 0.983, 42: 0.974, 43: 0.965, 44: 0.951}, 0.54: {0: '-', 1: '-', 2: '-', 3: '-', 4: 1.112, 5: 1.109, 6: 1.107, 7: 1.105, 8: 1.102, 9: 1.099, 10: 1.096, 11: 1.094, 12: 1.092, 13: 1.09, 14: 1.087, 15: 1.085, 16: 1.082, 17: 1.079, 18: 1.076, 19: 1.073, 20: 1.07, 21: 1.067, 22: 1.063, 23: 1.06, 24: 1.057, 25: 1.054, 26: 1.05, 27: 1.047, 28: 1.043, 29: 1.04, 30: 1.036, 31: 1.032, 32: 1.028, 33: 1.024, 34: 1.02, 35: 1.016, 36: 1.012, 37: 1.008, 38: 1.004, 39: 0.997, 40: 0.99, 41: 0.983, 42: 0.976, 43: 0.967, 44: 0.953}, 0.565: {0: '-', 1: '-', 2: '-', 3: 1.118, 4: 1.115, 5: 1.112, 6: 1.11, 7: 1.108, 8: 1.105, 9: 1.103, 10: 1.1, 11: 1.098, 12: 1.095, 13: 1.093, 14: 1.09, 15: 1.088, 16: 1.085, 17: 1.083, 18: 1.08, 19: 1.077, 20: 1.074, 21: 1.071, 22: 1.067, 23: 1.064, 24: 1.061, 25: 1.058, 26: 1.054, 27: 1.051, 28: 1.047, 29: 1.043, 30: 1.039, 31: 1.035, 32: 1.031, 33: 1.027, 34: 1.023, 35: 1.019, 36: 1.015, 37: 1.011, 38: 1.007, 39: 1.003, 40: 0.998, 41: 0.989, 42: 0.979, 43: 0.97, 44: 0.954}, 0.6: {0: '-', 1: '-', 2: '-', 3: 1.121, 4: 1.119, 5: 1.117, 6: 1.115, 7: 1.112, 8: 1.11, 9: 1.108, 10: 1.105, 11: 1.103, 12: 1.101, 13: 1.098, 14: 1.095, 15: 1.092, 16: 1.09, 17: 1.087, 18: 1.084, 19: 1.081, 20: 1.078, 21: 1.074, 22: 1.071, 23: 1.067, 24: 1.064, 25: 1.061, 26: 1.058, 27: 1.054, 28: 1.051, 29: 1.047, 30: 1.043, 31: 1.039, 32: 1.035, 33: 1.031, 34: 1.027, 35: 1.023, 36: 1.019, 37: 1.015, 38: 1.011, 39: 1.007, 40: 1.002, 41: 0.992, 42: 0.983, 43: 0.974, 44: 0.957}, 0.68: {0: '-', 1: 1.138, 2: 1.135, 3: 1.132, 4: 1.129, 5: 1.127, 6: 1.125, 7: 1.122, 8: 1.12, 9: 1.118, 10: 1.115, 11: 1.112, 12: 1.109, 13: 1.107, 14: 1.104, 15: 1.1, 16: 1.097, 17: 1.094, 18: 1.091, 19: 1.087, 20: 1.084, 21: 1.08, 22: 1.077, 23: 1.074, 24: 1.07, 25: 1.067, 26: 1.064, 27: 1.06, 28: 1.057, 29: 1.053, 30: 1.049, 31: 1.045, 32: 1.041, 33: 1.065, 34: 1.033, 35: 1.029, 36: 1.025, 37: 1.021, 38: 1.017, 39: 1.013, 40: 1.008, 41: 0.999, 42: 0.99, 43: 0.98, 44: 0.97}, 0.7: {0: '-', 1: '-', 2: 1.137, 3: 1.135, 4: 1.132, 5: 1.13, 6: 1.127, 7: 1.125, 8: 1.123, 9: 1.12, 10: 1.117, 11: 1.114, 12: 1.112, 13: 1.109, 14: 1.106, 15: 1.102, 16: 1.099, 17: 1.096, 18: 1.093, 19: 1.089, 20: 1.086, 21: 1.082, 22: 1.079, 23: 1.076, 24: 1.072, 25: 1.069, 26: 1.065, 27: 1.062, 28: 1.058, 29: 1.055, 30: 1.051, 31: 1.047, 32: 1.043, 33: 1.074, 34: 1.035, 35: 1.031, 36: 1.027, 37: 1.023, 38: 1.018, 39: 1.014, 40: 1.01, 41: 1.001, 42: 0.992, 43: 0.982, 44: 0.973}, 0.8: {0: '-', 1: 1.151, 2: 1.148, 3: 1.145, 4: 1.143, 5: 1.14, 6: 1.137, 7: 1.134, 8: 1.132, 9: 1.129, 10: 1.126, 11: 1.123, 12: 1.12, 13: 1.117, 14: 1.114, 15: 1.111, 16: 1.108, 17: 1.105, 18: 1.101, 19: 1.097, 20: 1.094, 21: 1.09, 22: 1.087, 23: 1.084, 24: 1.08, 25: 1.076, 26: 1.072, 27: 1.068, 28: 1.065, 29: 1.061, 30: 1.057, 31: 1.053, 32: 1.049, 33: 1.046, 34: 1.042, 35: 1.038, 36: 1.033, 37: 1.029, 38: 1.025, 39: 1.021, 40: 1.017, 41: 1.008, 42: 0.999, 43: 0.99, 44: 0.981}, 0.9: {0: '-', 1: '-', 2: 1.158, 3: 1.156, 4: 1.153, 5: 1.15, 6: 1.147, 7: 1.144, 8: 1.141, 9: 1.138, 10: 1.135, 11: 1.132, 12: 1.129, 13: 1.125, 14: 1.122, 15: 1.118, 16: 1.115, 17: 1.112, 18: 1.108, 19: 1.104, 20: 1.101, 21: 1.094, 22: 1.092, 23: 1.091, 24: 1.087, 25: 1.084, 26: 1.08, 27: 1.076, 28: 1.072, 29: 1.068, 30: 1.065, 31: 1.061, 32: 1.058, 33: 1.053, 34: 1.049, 35: 1.045, 36: 1.041, 37: 1.037, 38: 1.033, 39: 1.03, 40: 1.026, 41: 1.016, 42: 1.007, 43: 0.998, 44: 0.989}, 1: {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-', 9: '-', 10: 1.143, 11: 1.139, 12: 1.136, 13: 1.132, 14: 1.128, 15: 1.125, 16: 1.121, 17: 1.118, 18: 1.114, 19: 1.111, 20: 1.107, 21: 1.104, 22: 1.1, 23: 1.097, 24: 1.094, 25: 1.09, 26: 1.086, 27: 1.082, 28: 1.079, 29: 1.075, 30: 1.071, 31: 1.067, 32: 1.064, 33: 1.06, 34: 1.056, 35: 1.052, 36: 1.048, 37: 1.044, 38: 1.04, 39: 1.036, 40: 1.032, 41: 1.023, 42: 1.015, 43: 1.006, 44: 0.996}}
    root_df = {-70: 0, -65: 1, -60: 2, -55: 3, -50: 4, -45: 5, -40: 6, -35: 7, -30: 8, -25: 9, -20: 10, -15: 11, -10: 12, -5: 13, 0: 14, 5: 15, 10: 16, 15: 17, 20: 18, 25: 19, 30: 20, 35: 21, 40: 22, 45: 23, 50: 24, 55: 25, 60: 26, 65: 27, 70: 28, 75: 29, 80: 30, 85: 31, 90: 32, 95: 33, 100: 34, 105: 35, 110: 36, 115: 37, 120: 38, 125: 39, 130: 40, 140: 41, 150: 42, 160: 43, 170: 44}
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

class info():
    """Можно достать инфу из бланков
    """
    def __init__(self, file):
        """ИНФА

        Args:
            file (_type_): file.docx
        """
        try:
            composed_docx = [x for x in process(file).split("\n") if len(x)]
            decomposed_docx = [[composed_docx[composed_docx.index(item)-1], item] for item in composed_docx if ("ВНВ" in item or "ВОВ" in item or "название:"in item)]
            decomposed_docx = [[item[1], True] if 'Теплоутилизатор'.lower() in item[0].lower() else [item[1], False] for item in decomposed_docx if not 'Теплоутилизатор-охладитель'.lower() in item[0].lower()]
            try:
                orderer, object_, manager = [y for y in composed_docx if "организация: " in y or "менеджер:" in y or "объект: " in y]
                orderer = orderer.replace("организация: ", "")
                object_ = object_.replace("объект: ","")
                manager = manager.replace("менеджер: ", "")
                all_data = []
                var = []
                # st.write(decomposed_docx)
                name = decomposed_docx[0][0][10:]
                system = decomposed_docx[1][0][10:]
                # st.write(decomposed_docx[1])
                for item in decomposed_docx[2:]:
                    try:
                        var.append(item[0])
                        
                        sidee = findall(r"сторона: ([слевапр]*)", item[0])[0][1].upper()
                        heat_exchanger = findall(r"теплообменник; назв: ([ВНО\.\d\-]*)", item[0])[0]
                        temperature = float(findall(r"tжн=([\-\.\d]*)°C;", item[0])[0])
                        G = float(findall(r"[GV]ж=([\d\.]*)кг/ч", item[0])[0])/1000
                        try:
                            glycol = float(findall(r"иленгл: ([\d\.]*)%;", item[0])[0])
                            glykol_type = findall(r"([этпро]*иленгл)", item[0])[0]+'иколь'
                            realG = G/search_glic_ro(temperature, glycol/100)
                        except:
                            glycol = 0
                            glykol_type = ''
                            realG = G/search_glic_ro(temperature, glycol/100)
                        realG = round(realG, 3)
                        hu = item[1]
                        all_data.append([('теплообменник', heat_exchanger), ("температура",temperature), ("расход", realG), ("содержание гликоля", glycol), ("заказчик", orderer), ("объект", object_), ("менеджер", manager), ("название", name), ("система", system), ("сторона обслуживания", sidee),  ("теплоутилизатор", hu), ("тип гликоля", glykol_type)])
                    except:
                        pass
            except:
                try:
                    decomposed_docx = [item for item in process(folder+file2).split("\n") if len(item)]
# print(infos)
                    orderer = decomposed_docx[decomposed_docx.index('Заказчик:')+1]
                    object_ = decomposed_docx[decomposed_docx.index('Объект:')+1]
                    manager = " "
                    all_data = []
                    var = []
                    name = system = decomposed_docx[decomposed_docx.index('Название:')+1]
                    for item in decomposed_docx:
                        if "Индекс: Канал-КВН" in item or "Индекс: Канал-ВКО" in item:
                            var.append('')
                            sidee = "СПРАВА"
                            heat_exchanger = item.split()[1].split(";")[0]
                            temperature = float(findall(r"tжн= {0,1}([\-\.,\d]*) {0,1}°C", item)[0].replace(",", "."))
                            G = float(findall(r"Gж=([\-\.,\d]*) кг/ч", item)[0].replace(",", "."))/1000
                            glycol = 0
                            glykol_type = ''
                            realG = G/search_glic_ro(temperature, glycol/100)
                            hu = ''
                            all_data.append([('теплообменник', heat_exchanger), ("температура",temperature), ("расход", realG), ("содержание гликоля", glycol), ("заказчик", orderer), ("объект", object_), ("менеджер", manager), ("название", name), ("система", system), ("сторона обслуживания", sidee),  ("теплоутилизатор", hu), ("тип гликоля", glykol_type)])
                except:
                    pass
            self.all_data = all_data
            self.var = var
        except:
            pass
