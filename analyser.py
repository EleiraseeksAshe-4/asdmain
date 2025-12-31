import os

import pandas as pd
import fitz
from tabula import read_pdf
from tabulate import tabulate



def find_text_in_pdf(pdf_path, text_to_find) :
    doc = fitz.open(pdf_path)

    # Specify the text you want to search for
    search_text = text_to_find

    # Iterate through each page in the PDF
    for page in doc:
        page_num = page.number
        # Use the `search_for` method to find instances of the search text on the page
        text_instances = page.search_for(search_text)
        return text_instances[0]

        # # Iterate through each instance and print the bounding box coordinates
        # for text_instance in text_instances:
        #     x0, y0, x1, y1 = text_instance.bbox
        #     print(f"Page {page_num + 1}:")
        #     print(f"Text: {search_text}")
        #     print(f"Bounding Box: ({x0}, {y0}) - ({x1}, {y1})")

def find_textoptions_in_pdf(pdf_path, text_to_find, excludetext) :
    doc = fitz.open(pdf_path)

    # Specify the text you want to search for
    search_text = text_to_find

    # Iterate through each page in the PDF
    for page in doc:
        page_num = page.number
        # Use the `search_for` method to find instances of the search text on the page
        text_instances = page.search_for(search_text)
        text_instance = text_instances[0]
        if len(text_instances) > 1:
            exclude_instances = page.search_for(excludetext)
            if len(exclude_instances) > 0:
                for ti in text_instances:
                    tx0, ty0, tx1, ty1 = ti
                    for ei in exclude_instances:
                        if not (ty0 == ei.y0 and ty1 == ei.y1 and tx0 > ei.x0 and tx1 <= ei.x1):
                            return ti


        return text_instance
        # # Iterate through each instance and print the bounding box coordinates
        # for text_instance in text_instances:
        #     x0, y0, x1, y1 = text_instance.bbox
        #     print(f"Page {page_num + 1}:")
        #     print(f"Text: {search_text}")
        #     print(f"Bounding Box: ({x0}, {y0}) - ({x1}, {y1})")

def list_files_with_extension(directory_path, extension):
    file_names = []
    for item in os.listdir(directory_path):
        if item.endswith(extension) and os.path.isfile(os.path.join(directory_path, item)):
            file_names.append(os.path.splitext(item)[0])
    return file_names


def list_directories(path):
    directories = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            directories.append(item)
    directories.sort()
    return directories


def processInvoices(invoiceNames, path):
    invoiceNames.sort()
    for invoice in invoiceNames:
        try:
            #if invoice == 'lcas202310_rc':
            readInvoice(invoice, path)
        except Exception as e:
            print("Error reading invoice " + invoice, e)

def findTableColumns(pdf_name):
    dateR = find_text_in_pdf(pdf_name, 'Date of meeting')
    sessionR = find_textoptions_in_pdf(pdf_name, 'Session', 'Length of Session')
    principalR = find_text_in_pdf(pdf_name, 'Principal or Associate')
    hoursR = find_text_in_pdf(pdf_name, 'Length of Session')
    travelR = find_text_in_pdf(pdf_name, 'Travel')
    reportR = find_text_in_pdf(pdf_name, 'Report')
    return [dateR.x0, sessionR.x0, principalR.x0, hoursR.x0, travelR.x0, reportR.x0]

def readInvoice(invoiceName, invoicePath):
    print(invoiceName)
    pdf_name = invoicePath + '/' + invoiceName + '.pdf'

    tl = find_text_in_pdf(pdf_name, 'Date of meeting')
    br = find_text_in_pdf(pdf_name, 'Total Treatment (Principal)')
#    table0area = [289, 56, 502, 535]
    table0area = [tl.y0-2, tl.x0 -2, br.y0, 535]
#    table0columns = [56, 138, 298, 379, 451, 500]
    table0columns = findTableColumns(pdf_name)


    #    table1area = [510, 54, 572, 535]
    table1area = [br.y0 - 2, tl.x0 -2, br.y0 + 62, 535]

    # reads table from pdf file
    table0 = read_pdf(pdf_name, pages="all", multiple_tables=False, area=table0area,
                      columns=table0columns)  # address of pdf file
    selected_columns = table0[0].iloc[:, 1:]
    newTable = pd.DataFrame({0: [invoiceName] * len(table0[0])})
    newTableFinal = pd.concat([newTable, selected_columns], axis=1)
    # ewTableFinal.rename(columns = {'InvRef', 'Date', 'Notes', 'Associate', 'ClinicalHours', "TravelHours", 'Report'})
    newTableFinal.rename(columns={newTableFinal.columns[0]: 'InvRef',
                                  newTableFinal.columns[1]: 'Date',
                                  newTableFinal.columns[2]: 'Notes',
                                  newTableFinal.columns[3]: 'Associate',
                                  newTableFinal.columns[4]: 'ClinicalHours',
                                  newTableFinal.columns[5]: "TravelHours"},
                                  inplace=True)

    sumHours = 0
    sumTravel = 0
    try:
        sumHours = newTableFinal['ClinicalHours'].sum()
        sumTravel = newTableFinal['TravelHours'].sum()
    except:
        print("")
#    sumReport = newTableFinal['Report'].sum()


    table1 = read_pdf(pdf_name, pages="all", multiple_tables=False, area=table1area,
                      pandas_options={'header': None})  # address of pdf file

    # print(invoiceName)
    # print(tabulate(newTableFinal))
    # print(tabulate(table1[0]))
    summaryClinical = table1[0].iloc[1, 1]
    summaryTravel = table1[0].iloc[3, 1]
    summaryFuel = table1[0].iloc[4, 1]


    clinicalDiff = summaryClinical - sumHours
    travelDiff = summaryTravel - sumTravel

    if clinicalDiff != 0 or travelDiff != 0:
        print(invoiceName, summaryClinical - sumHours, summaryTravel - sumTravel)
        print(tabulate(newTableFinal))
        print(tabulate(table1[0]))
        print(sumHours, sumTravel)
        print(summaryClinical, summaryTravel)



# Specify the path to the directory you want to enumerate
directory_path = "/Users/johnbridges/Dropbox/NewHope Psychology/Invoicing/dropboxinvoices/Becca/"

# Enumerate directory names
directory_names = list_directories(directory_path)

# Print the directory names
for name in directory_names:
    #for name in ['AS']:
    pathToClient = directory_path + name
    invoices = list_files_with_extension(directory_path + name, '.pdf')
    processInvoices(invoices, pathToClient)
    print(name)

# readInvoice('lccg202312', '/Users/johnbridges/Dropbox/NewHope Psychology/Invoicing/dropboxinvoices/Becca/CG/')
