import streamlit as st
from info_search_vector import info #Вытаскиваем информацию по вектору
from info_search_vector import search_glic_ro
from vector_selection import selection #Формируем полное наименование Вектора
from auto_valve_scheme import valve, scheme  # для формирования имени
from blank import blank_auto #Формируем Вектор, который выводится на странице
from order_form import fulfil_temp # По факту, самое главное - формирует сам бланк
import io
from zipfile import ZipFile 
from vector_verosa import many_bl, table_costs
import pandas as pd


st.set_page_config(layout="wide") 
st.session_state['developer'] = st.text_input('Введите имя разработчика') #Вводим имя инженера
main_tab = st.tabs(['Автоматический режим', 'Полуавтоматический режим', 'Ручной режим']) #Возможность выбрать режим
st.session_state['blank_name'] = []


def automate_foo(ind,vector_podbor = bool):
    """ Общая основная функция для автоматического и полуавтоматического режима\n
    Единственные два отличия: вектор и резерв подбираются самостоятельно"""
    i = 0 #Счётчик для кнопок (и для номера файла)
    j = 0
    f = st.file_uploader("Перетяните бланки сюда", accept_multiple_files=True,key=ind) #Виджет ввода бланков
    #file_zip = zipfile.ZipFile ('C:\\Users\\kushhov\\Desktop\\vector-main\\Archive.zip','w')
    Archive = io.BytesIO()
    name_archive = ''
    name_file = ''
    vals = {} #Создаём словарь для передачи в many_bl
    all_df_cost = {}
    all_df_cost = pd.DataFrame(all_df_cost)
    all_df_verosa = {}
    all_df_verosa = pd.DataFrame(all_df_verosa)
    for file in f: #Проходимся по каждому файлу
        #st.session_state['blank_name'].append(file.name) Попытка вывести все наименования загружаемых бланков
        #st.session_state['blank_name']
        j +=1
        #st.write(info(file).all_data) #Выводит один большой вложенный список
        name_file = file.name
        current_info = info(file).all_data #Создаём экземпляр класса (all_data - список)
        name_archive = ''
        BZ = current_info[0][7][1]
        key_cost = []
        cvector_list = []
        rezerve_list = []
        for cinfo in current_info: #Пробегаем по полученному списку (список набор кортежей - пар) Здесь мы работаем только с одним файлом
            ind +=1 
            cvector,vector_scheme, vector_valve, type_size = selection(scheme(cinfo[0][1]), valve(cinfo[0][1], cinfo[2][1]), cinfo[2][1], cinfo[9][1])
            cblank = (blank_auto(selection(scheme(cinfo[0][1]), valve(cinfo[0][1], cinfo[2][1]), cinfo[2][1], cinfo[9][1]), cinfo, st.session_state['developer']))
            cvector,vector_scheme, vector_valve, type_size = selection(scheme(cinfo[0][1], cblank["intermediate coolant"]), valve(cinfo[0][1], cinfo[2][1], cblank["intermediate coolant"]), cinfo[2][1], cinfo[9][1])
            cblank = (blank_auto(cvector, cinfo, st.session_state['developer'])) #Формируем тот самый Вектор, который выводится

            if vector_podbor:
                col = st.columns(2) # Делим на два столбца
                vector_scheme, vector_valve, vector_side,rezerve = vector_form_foo(ind,col,vector_scheme)
                cvector,vector_scheme, vector_valve, type_size = selection(vector_scheme, vector_valve, cblank["consumption"], vector_side)
                type_scheme =[vector_scheme,vector_valve,type_size]
                cblank["vector"] = cvector
            else:
                #type_scheme = scheme(cinfo[0][1], cblank["intermediate coolant"]) + '-' + valve(cinfo[0][1], cinfo[2][1], cblank["intermediate coolant"])
                type_scheme =[vector_scheme,vector_valve,type_size]


            st.write(cblank) # В конечном итоге выводим бланк в виде вектора


            # Блок формирования бланков и добавления в архив


            bio = io.BytesIO()
            document = fulfil_temp(cblank,type_scheme)
            key_cost.append(f'{type_scheme[0]}-{type_scheme[1].upper()}-{type_scheme[2]}')
            document.save(bio)
            cvector_list.append(cvector)
            if vector_podbor:
                rezerve_list.append(rezerve)
            name = f"{cblank['order form']}-{cblank['system']}-{cvector}.docx"
            with ZipFile(Archive, mode='a') as archive:
                archive.writestr(name, bio.getvalue())

            name_archive = cblank['orderer']+'.zip'
            # он полностью относится к cinfo

            vals[f'scheme{i}'] = scheme(cinfo[0][1], cblank["intermediate coolant"])
            vals[f'valve{i}'] = valve(cinfo[0][1], cinfo[2][1], cblank["intermediate coolant"])
            vals[f'side{i}'] = cinfo[9][1]
            vals[f'rez{i}'] = False
            i+=1



        df_verosa, df_cost = many_bl(file,vals,name_file,BZ,key_cost,cvector_list,vector_podbor,rezerve_list) 
        all_df_cost = pd.concat([all_df_cost,df_cost])
        all_df_verosa = pd.concat([all_df_verosa,df_verosa])

        if j == len(f):
            #БЛОК ЗАПОЛНЕНИЯ ТАБЛИЦ (внешний цикл)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            all_df_verosa.to_excel(output, index=False)
            name = 'ВЕКТОР ВЕРОСА.xlsx'
            with ZipFile(Archive, mode='a') as archive:
                archive.writestr(name,output.getvalue())

            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            all_df_cost.to_excel(output, index=False)
            name = 'ВЕКТОР ЦЕНЫ.xlsx' 
            with ZipFile(Archive, mode='a') as archive:
                archive.writestr(name,output.getvalue())

            st.download_button('💾Загрузить Архив: ', data=Archive.getvalue(), file_name=name_archive,key=ind+6) # Для каждого файла свой архив (относится к внешнему циклу)

def vector_form_foo(ind,col,vector_scheme):
    col[0].write(f'Узелрегулирующий ВЕКТОР:')
    col[1].write(' ')
    col[1].write(' ')
    col[1].write(' ')
   

    origin = 0
    match vector_scheme:
        case "1":
            origin = 0
        case "2":
            origin = 1
        case "3": 
            origin = 2
        case "4":
            origin = 3
        case "4М":
            origin = 4
        case "5":
            origin = 5
        case "5М":
            origin = 6
        case "6":
            origin = 7
        case "6М":
            origin = 8


    vector_scheme = col[0].selectbox( 'Схема', ('1', '2', '3','4','4М','5','5М','6','6М'),key=ind+111,index=origin)
    if vector_scheme in ('1','3','4М'):
        vector_valve = 'С'
        col[0].write('Клапан: С')
    elif vector_scheme in ('6','6М'):
        vector_valve = 'Ш'
        col[0].write('Клапан: Ш')
    else:
        vector_valve = col[0].selectbox( 'Клапан', ('С', 'Ш'),key=ind+222)

    rezerve = col[1].checkbox(label ='Резерв',key=ind+444)
    if rezerve:
        rezerve = 1
    else:
        rezerve = 0
    vector_side = col[1].selectbox( 'Сторона подключения', ('Л', 'П'),key=ind+333,index=1)
    return vector_scheme, vector_valve, vector_side, rezerve

with main_tab[0]: # Для автоматического режима 
    automate_foo(0,False)

with  main_tab[2]: # Для ручного режима
    col = st.columns(2) # Делим на два столбца

    cblank = {} #Создаём пустой бланк
    Archive = io.BytesIO()
    #Основная юридическая информация
    col[0].write('Основная юридическая информация')
    cblank["orderer"] = col[0].text_input('Заказчик:')
    cblank["object"] = col[0].text_input('Объект:')
    cblank["manager"] = col[0].text_input('Менеджер:')
    cblank["order form"] = col[0].text_input('Номер БЗ:')
    cblank["developer"] = col[0].text_input('Выполнил:')

    #Исходные данные и режимы работы 
    col[1].write('Исходные данные и режимы работы')
    cblank["temperature"] = col[1].number_input('Температура на входе:')
    cblank["consumption"] = col[1].number_input('Расход теплоносителя, т/ч')
    glycol_hidden = False
    cblank["glycol type"] = col[1].radio("Выберите тип теплоносителя",('Этиленгликоль', 'Пропиленгликоль', 'Вода, соответствует требованиям СП 124.13330.2012'))
    if  cblank["glycol type"] == 'Вода, соответствует требованиям СП 124.13330.2012':
        glycol_hidden = True
        cblank["glycol"] = 0
    cblank["glycol"] = col[1].number_input(label ='Cодержание гликоля %',disabled =glycol_hidden)


    #Формирование поправочной цены

    realG = cblank["consumption"] /search_glic_ro(cblank["temperature"], cblank["glycol"]/100)

    #Формирование вектора

    
    vector_scheme, vector_valve, vector_side,rezerve = vector_form_foo(10,col,1)
    cvector,vector_scheme, vector_valve, type_size = selection(vector_scheme, vector_valve, cblank["consumption"], vector_side)
    st.write(f'{cvector}')



    cblank["vector"] = cvector
    if rezerve:
        cblank["reserve"] = 1
    else:
        cblank["reserve"] = 0



    type_scheme =[vector_scheme,vector_valve,type_size]
    document = fulfil_temp(cblank,type_scheme)
    key_cost = [f'{vector_scheme}-{vector_valve}-{type_size}']
    bio = io.BytesIO()
    document.save(bio)
    name = f"{cvector}.docx"
    with ZipFile(Archive, mode='a') as archive:
        archive.writestr(name, bio.getvalue())



    #Формирование таблиц
    allsis={"Бланк": [cblank["orderer"]],
                "Расход жидкости": [cblank["consumption"]],
                "Температура на входе": [cblank["temperature"]],
                "Доля гликоля": [cblank["glycol"]],
                "Расход поправочный": realG,
                "Вектор": [cblank["vector"]],
                "Номер БЗ": [cblank["order form"]],
                "Резерв": [cblank["reserve"]]}
        
    df_verosa = pd.DataFrame(allsis)  
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_verosa.to_excel(output, index=False)
    name = 'ВЕКТОР ВЕРОСА.xlsx'
    with ZipFile(Archive, mode='a') as archive:
        archive.writestr(name,output.getvalue())
    BZ = [cblank["order form"]]
    rezerve = [str(cblank["reserve"])]
    glycol = [cblank["glycol"]]
    blank = [cblank["orderer"]]
    block = ['-']
    df_cost = table_costs(BZ, key_cost, rezerve,glycol,blank,block)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_cost.to_excel(output, index=False)
    name = 'ВЕКТОР ЦЕНЫ.xlsx' 
    with ZipFile(Archive, mode='a') as archive:
        archive.writestr(name,output.getvalue())
    name_archive = cblank['order form']+'.zip'
    st.download_button('💾Загрузить Архив: ', data=Archive.getvalue(), file_name=name_archive) # Для каждого файла свой архив (относится к внешнему циклу)

with  main_tab[1]: #Полуавтоматический режим: ВЕКТОК-схема-клапан-сторона и резерв
    automate_foo(400,True)
