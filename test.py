import xlsxwriter
import pandas as pd
import openpyxl

while True:
    try:
        job_option = int(input("Please select an option:\n1. Software Engineer\n2. Cyber Security Specialist\n3. Data Analyst\n"))
        if job_option in range(1, 4):
            break
    except:
        pass

if job_option == 1:
    xl_name = "SoftwareEngineer"
elif job_option == 2:
    xl_name = "CyberSecuritySpecialist"
elif job_option == 3:
    xl_name = "DataAnalyst"


# def excel_print():
#     workbook = openpyxl.load_workbook(f"{xl_name}.xlsx")
#     worksheet = workbook.active
#     print(worksheet.cell(row=1, column=1).value)

def excel_print():
    try:
        pd.set_option('display.max_colwidth', 200)
        pd.set_option("display.expand_frame_repr", False)
        pd.set_option("display.max_rows", None)
        df = pd.read_excel(f"{xl_name}.xlsx")
        print(df)
    except:
        print("No such file.")
excel_print()