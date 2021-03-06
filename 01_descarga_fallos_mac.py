"""
Software para descargar estados diarios de la corte suprema

    TODO:
        Encontrar id de documento a descargar                       -> listo
        Elegir fecha                                                -> listo
        Elegir pagina                                               -> listo
        Revisar si tiene mas de 1 documento y descargarlos todos    ->
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import wget
from datetime import datetime, timedelta
import time
import os
import utils

url_web = "http://www.pjud.cl/estado-diario"
url_descarga_1 = "http://www.pjud.cl/estado-diario?p_p_id=estadodiario_WAR_estadodiarioportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-3&p_p_col_pos=1&p_p_col_count=2&_estadodiario_WAR_estadodiarioportlet_campoTribunal=6050000&_estadodiario_WAR_estadodiarioportlet_paginando=S&_estadodiario_WAR_estadodiarioportlet_cur=3&crr_documento="
url_descarga_2 = "&tipoModulo=CORTE&fuenteDocumento=SUPREMA"
SUBSTRACT_DAYS_FROM_TODAY = 1
downloadFolder = "downloads"
fileFolder = "files"

if not os.path.exists(downloadFolder):
    os.mkdir(downloadFolder)
    print("Directory " + downloadFolder + " Created ")
else:
    print("Directory " + downloadFolder + " already exists")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

driver = webdriver.Chrome(executable_path=DRIVER_BIN)
#driver = webdriver.Chrome("chromedriver")
driver.get(url_web)
print(driver.title)

wait = WebDriverWait(driver, 10)

if driver.title != "404 Not Found":
    select = Select(driver.find_element_by_name(
        "_estadodiario_WAR_estadodiarioportlet_campoCorteApelaciones"))
    select.select_by_value("0")

    select = Select(driver.find_element_by_name(
        "_estadodiario_WAR_estadodiarioportlet_campoTribunal"))
    select.select_by_value("6050000")

    currentDT = datetime.now()
    # date2check = currentDT
    date2check = currentDT - timedelta(days=SUBSTRACT_DAYS_FROM_TODAY)
    date_name = date2check.strftime("%Y_%m_%d")

    input_text = "Date to check: " + date_name + "\n"
    input_text += "(1) OK\n"
    input_text += "(2) Enter other Date\n"
    input_index = input(input_text)

    isInputOk = True
    if input_index == "1":
        pass
    elif input_index == "2":
        input_text = "type date in format: %Y_%m_%d -> ex: 2019_05_19\n"
        input_date = input(input_text)
        date2check = datetime.strptime(input_date, "%Y_%m_%d")
        date_name = input_date
    else:
        print("input " + input_index + " was not an option")
        print("Closing the program")
        isInputOk = False
    if isInputOk:
        print("Date to check: " + date_name)

        select = Select(driver.find_element_by_name(
            "_estadodiario_WAR_estadodiarioportlet_pest_fecha_year_d"))
        select.select_by_value(str(date2check.year))

        select = Select(driver.find_element_by_name(
            "_estadodiario_WAR_estadodiarioportlet_pest_fecha_month_d"))
        select.select_by_value(str(date2check.month - 1))

        select = Select(driver.find_element_by_name(
            "_estadodiario_WAR_estadodiarioportlet_pest_fecha_day_d"))
        select.select_by_value(str(date2check.day))

        input_elems = driver.find_elements_by_tag_name("input")

        for input_elem in input_elems:
            if input_elem.get_attribute("value") == "Filtrar fecha":
                submit_button = input_elem
                break

        time.sleep(2)
        submit_button.click()

        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        #     (By.ID, '_estadodiario_WAR_estadodiarioportlet_ocerSearchContainerPageIteratorBottom_itemsPerPage')))

        wait.until(EC.element_to_be_clickable(
            (By.ID, '_estadodiario_WAR_estadodiarioportlet_ocerSearchContainerPageIteratorBottom_itemsPerPage')))
        select = Select(driver.find_element_by_id(
            "_estadodiario_WAR_estadodiarioportlet_ocerSearchContainerPageIteratorBottom_itemsPerPage"))
        select.select_by_value("75")

        doc_id_list = []
        number_list = []
        entry_number_list = []
        hasMorePages = True

        while hasMorePages:
            next_button = None

            time.sleep(2)
            # with utils.wait_for_page_load(driver):

            print(driver.title)

            NUMBER_KEY = "_estadodiario_WAR_estadodiarioportlet_ocerSearchContainer_col-n°_row-"
            ENTRY_NUMBER_KEY = "_estadodiario_WAR_estadodiarioportlet_ocerSearchContainer_col-n°-de-ingreso_row-"
            NUMBER_OF_DOCUMENTS_KEY = "_estadodiario_WAR_estadodiarioportlet_ocerSearchContainer_col-providencias_row-"

            for j in range(1, 76):
                try:
                    number_element = driver.find_element_by_id(
                        NUMBER_KEY + str(j))
                    entry_number_element = driver.find_element_by_id(
                        ENTRY_NUMBER_KEY + str(j))
                    number_of_documents_element = driver.find_element_by_id(
                        NUMBER_OF_DOCUMENTS_KEY + str(j))
                    number_of_docs = int(number_of_documents_element.text)

                    for k in range(0, number_of_docs):
                        number_list.append(number_element.text)
                        entry_number_list.append(
                            entry_number_element.text + "&" + str(k + 1))

                except exceptions.NoSuchElementException:
                    print("Element number " + str(j) + " wasn´t found")
                    break

            a_elements = driver.find_elements_by_xpath("//a")
            for a_elem in a_elements:
                onclick_atr = a_elem.get_attribute("onclick")
                if onclick_atr:
                    doc_id = onclick_atr[10:-1]
                    doc_id_list.append(doc_id)

            for a_elem in a_elements:
                if a_elem.text == "Siguiente":
                    next_button = a_elem
                    break

            time.sleep(2)
            if next_button:
                next_button.click()
            else:
                print("No more pages")
                hasMorePages = False

        driver.close()

        print("Lista de numeros de ingreso de los fallo: " +
              str(len(entry_number_list)))
        # print(entry_number_list)

        print("Init to Download")
        print("Downloading " + str(len(doc_id_list)) + " files")
        # print(doc_id_list)

        folderName = os.path.join(downloadFolder, date_name)
        fileFolderName = os.path.join(folderName, fileFolder)

        if not os.path.exists(folderName):
            os.mkdir(folderName)
            print("Directory " + folderName + " Created ")
        else:
            print("Directory " + folderName + " already exists")

        if not os.path.exists(fileFolderName):
            os.mkdir(fileFolderName)
            print("Directory " + fileFolderName + " Created ")
        else:
            print("Directory " + fileFolderName + " already exists")

        i = 0
        for doc_id in doc_id_list:
            url_final = url_descarga_1 + doc_id + url_descarga_2
            file_path = os.path.join(
                fileFolderName, date_name + "&" + number_list[i] + "&" + entry_number_list[i])
            print("\n" + file_path)

            file_extension = utils.get_extension(url_final)
            file_complete_path = file_path + "." + file_extension

            if os.path.exists(file_complete_path):
                os.remove(file_complete_path)

            file_name = wget.download(url_final, file_complete_path)
            if (file_extension != "pdf"):
                utils.convert_to_pdf(file_name)
            i = i + 1

input("\nPress any key to close")



