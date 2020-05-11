"""
Buscar fallos que tengan al menos 'N' páginas
"""
import utils
import os
import shutil
import PyPDF2 as pyPdf

MIN_PAGES = -1
folderName = "downloads"
pdfFolderPath = "pdfs"
bigFileFolderPath = "biggerThan"

# Look for folders
dateFolders = utils.get_immediate_subdirectories(folderName)

# get input to check how many pages there is on files
isMinPageOk = False
while not isMinPageOk:
    try:
        MIN_PAGES = int(input("Ingresar la cantidad de páginas mínimas: "))

        if(MIN_PAGES <= 0):
            print("El valor tiene que ser mayor que cero")
        else:
            isMinPageOk = True 
    except ValueError:
        print("Valor ingresado tiene que ser número entero")

# Choose a folder
choose_text = "Choose folder to transform pdf files:\n"

i = 1
for folder in dateFolders:
    choose_text += "(" + str(i) + ") " + dateFolders[i-1] + "\n"
    i += 1

folder_index = int(input(choose_text))
choose_folder = os.path.join(folderName, dateFolders[folder_index-1])

# Extract pdf files name
pdf_path = os.path.join(choose_folder, pdfFolderPath)
pdf_files = utils.get_immediate_files(pdf_path)
print(pdf_files)

# # Create folder to save big files
# big_file_folder = os.path.join(choose_folder, bigFileFolderPath + str(MIN_PAGES))

# if not os.path.exists(big_file_folder):
#     os.mkdir(big_file_folder)
#     print("Directory " + big_file_folder + " Created ")
# else:
#     print("Directory " + big_file_folder + " already exists")

name_list = []

# Find files at less with 'N' pages and get file name
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_path, pdf_file)

    with open(pdf_file_path, "rb") as myFile:
        try:
            reader = pyPdf.PdfFileReader(myFile)
            myFile_page_number = reader.getNumPages()

            if myFile_page_number >= MIN_PAGES:
                print(pdf_file)
                name_list.append(pdf_file)
        except Exception as e:
            print(e)
            print("Error trying to get " + pdf_file + " file")

entry_number_list = []
for name in name_list:
    entry_number = name.split("&")[2]
    entry_number_list.append(entry_number)

date = choose_folder.split("\\")[1]

print()
print("########## RESULTADOS #########\n")
text = "El día " + date + " hubo " + str(len(pdf_files)) + " fallos\n"
print(text)

text = "De todos los fallos " + str(len(name_list)) + " se encontraron que tenga " + str(MIN_PAGES) + " o más páginas\n"
print(text)

text = "El número de ingreso de estos fallos son:\n"
print(text)
print(entry_number_list)
