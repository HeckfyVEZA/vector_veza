from vector_verosa import search_glic_ro,TIH,TIS
from docx import Document
import pandas as pd
from re import findall as f_all
import streamlit as st
import io


def many_bl_kanal(blanks,ind):# Кусок кода, работающий с каналкой   ЗДЕСЬ ОТСЛЕЖИВАЕМ НАЛИЧИЕ_ГЛИКОЛЯ
    #blanks = primary_ui("Канальное оборудование")["FolMon"].split(";")
    all_infos = []
    # Данные их all_infos
    #[['C:/Users/Test/Desktop/vector_veza-master/VECTOR_origin/canal/1-П1.docx', '-', 'Канал-КВН-80-50-3', 2607.9, 90.0, 0, 'C:/Users/Test/Desktop/vector_veza-master/VECTOR_origin/canal/1-П1.docx', 2701.535]]
    
    
    #Пустая таблица-словарь для будущего общего фрейма
    Data_table = {'Название бланка':[],'Блок':[],'Схема':[],'Клапан':[],'Сторона':[],'Теплообменник':[],'Расход жидкости':[],'Доля гликоля':[],'Включён':[],'Резерв':[],} #Пустные столбцы

    list_name = []
    nn = 0
    for blank in blanks:
        info_blank = file_read_kanal(blank)
        blank_name = blank.name
        for mini_info_blank in info_blank:
            mini_info_blank.append(round(mini_info_blank[3]/search_glic_ro(mini_info_blank[4], mini_info_blank[5]), 3))
            nn +=1
            list_name.append(blank_name)
            #Заполняем таблицу
            Data_table['Название бланка'].append(blank_name)
            Data_table['Блок'].append(mini_info_blank[1])
            Data_table['Схема'].append('')
            Data_table['Клапан'].append('')
            Data_table['Сторона'].append('') 
            Data_table['Теплообменник'].append(mini_info_blank[2])
            Data_table['Расход жидкости'].append(mini_info_blank[3])
            Data_table['Доля гликоля'].append(mini_info_blank[5])
            Data_table['Включён'].append(1) #По умолчанию для всех 1
            Data_table['Резерв'].append(0) #По умолчанию для всех  0
            all_infos.append(mini_info_blank)

    if nn:
        #Осуществялем меню-выбор
        Data_frame = pd.DataFrame(Data_table)
        #Множественный выбор
        col = st.columns(5) # Делим на два столбца
        col[0].write('Множественный выбор')
        all_col_vector_scheme = col[1].selectbox( 'Схема', ('Без выбора','1', '2', '3','4','4М','5','5М','6','6М'),key=ind+777)
        all_col_vector_valve = col[2].selectbox( 'Клапан', ('Без выбора','С', 'Ш'),key=ind+767)
        all_col_vector_side = col[3].selectbox( 'Сторона', ('Без выбора','П', 'Л'),key=ind+768)
        all_col_rezerve = col[4].selectbox( 'Резерв', ('Без выбора','0', '1'),key=ind+789)
        if all_col_vector_scheme != 'Без выбора':
            Data_frame['Схема'] = all_col_vector_scheme
        if all_col_vector_valve != 'Без выбора':    
            Data_frame['Клапан'] = all_col_vector_valve
        if all_col_vector_side != 'Без выбора':    
            Data_frame['Сторона'] = all_col_vector_side      
        if all_col_rezerve != 'Без выбора':    
            Data_frame['Резерв'] =  all_col_rezerve

        edit_frame = st.data_editor(Data_frame, use_container_width=True, hide_index=True, 
            column_config={
            "Резерв": st.column_config.SelectboxColumn(
                width="small",
                options=['0', '1'],
                required=True,
                    ),
            "Схема": st.column_config.SelectboxColumn(
                width="small",
                options=['1', '2', '3','4','4М','5','5М','6','6М'],
                required=True,
                    ),
            "Клапан": st.column_config.SelectboxColumn(
                width="small",
                options=['С', 'Ш'],
                required=True,
                    ),
            "Сторона": st.column_config.SelectboxColumn(
                width="small",
                options=['П', 'Л'],
                required=True,
                    ),
                },
                disabled=["Название бланка","Теплообменник","Расход жидкости","Доля гликоля"],
                )

        if st.button("Сформировать", type="primary",key=ind+999):
            vals = {} #Словарь
            for i in range(nn):
                vals[f'scheme{i}'] = edit_frame['Схема'].values[i]
                vals[f'cb{i}'] = edit_frame['Включён'].values[i]
                vals[f'rez{i}'] = edit_frame['Резерв'].values[i]
                vals[f'side{i}'] = edit_frame['Сторона'].values[i]
                vals[f'valve{i}'] = edit_frame['Клапан'].values[i]

                
            for i in range(len(all_infos)):
                if vals[f'cb{i}']:
                    all_infos[i].append(f"ВЕКТОР-{vals[f'scheme{i}']}-{vals[f'valve{i}']}-{scheme_recognition(vals[f'valve{i}'], float(all_infos[i][7]))}-{vals[f'side{i}']}-С+")
                    all_infos[i].append(int(vals[f'rez{i}']) if not (str(vals[f'scheme{i}']) in ['1', '3', '6', '6М'] or vals[f'valve{i}'] == "Ш") else 0)
            names_of, blocks, TOs, GnGs, Ts, Gs, GGs, Vs, short_blank, BZs, rezervs = [], [], [], [], [], [], [], [], [], [], []
            Glycol_found = []
            for item in all_infos:
                if len(item)>7:
                    names_of.append(item[0])
                    blocks.append(item[1])
                    TOs.append(item[2])
                    GnGs.append(item[3])
                    Ts.append(item[4])
                    Gs.append(item[5])
                    Glycol_found.append(item[5])
                    GGs.append(item[7])
                    Vs.append(item[-2])
                    #short_blank.append(item[0].split("/")[-1].split(".doc")[0])
                    #BZs.append(item[0].split("/")[-1].split(".doc")[0])
                    rezervs.append(item[-1])
            allsis = {"Бланк": list_name,
                    "Блок": blocks,
                    "Теплообменник": TOs, 
                    "Расход жидкости": GnGs, 
                    "Температура на входе": Ts, 
                    "Доля гликоля": Gs, 
                    "Расход поправочный": GGs, 
                    "Вектор": Vs, 
                    "Номер БЗ": '-', 
                    "Резерв": rezervs}

            df = pd.DataFrame(allsis)
            output = io.BytesIO()
            
            #df.to_excel(f"ВЕКТОР канал.xlsx", index=False)
            df.to_excel(output, index=False)
            name = 'ВЕКТОР канал.xlsx'
            st.download_button('💾Скачать таблицу: ', data=output.getvalue(), file_name=name,key=ind+98765)




def file_read_kanal(way:str): # Поиск информации в бланке каналки
    key_ = False
    all_vecs = []
    doc = Document(way)
    for tab in doc.tables:
        for row in tab.rows:
            for cell in row.cells:
                try:
                    TO = f_all(r"(Канал-КВ[НО][А-Яа-я0-9\-]+)", cell.text)[0]
                    G = float(f_all(r"[GV]ж=([0-9.,]+)", cell.text)[0].replace(",","."))
                    tzhn = float(f_all(r"tжн=([0-9.,]+)", cell.text)[0].replace(",","."))
                    block_num = "-"
                    g_s = f_all(r"ленгликоль [-]*? ?([0-9.,]+)", cell.text)
                    glycol = float((g_s[0])) / 100 if len(g_s) != 0 else 0
                    all_vecs.append([way, block_num, TO, G, tzhn, glycol, way])
                    break
                except:
                    if "Спектральные (дБ) и суммарные (дБА) уровни звуковой мощности" in cell.text:
                        key_ = True
                        break
                    else:
                        pass
            if key_:
                break
        if key_:
            break
    return all_vecs

def scheme_recognition(valve, G): # Функция, выбирающая то, какую функцию мы будем использовать для определения полного названия ВЕКТОРа
        return TIH(G) if valve.lower() in ["ш", "шаровой"] else TIS(G)



