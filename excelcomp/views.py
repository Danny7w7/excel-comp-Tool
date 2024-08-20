from django.shortcuts import render, HttpResponse

from io import BytesIO

import pandas as pd
import openpyxl
import os

# Create your views here.


def index(request):
    if request.method == 'POST':
        dfs = []
        if request.POST['report'] == 'client_report':
            files = [request.FILES['file1'], request.FILES['file2']]
        elif request.POST['report'] == 'broker_report':
            files = [request.FILES['file1']]

        for file in files:
            extension = get_extension(file)
            if extension == '.xlsx':
                dfs.append(pd.read_excel(file))
            else:
                dfs.append(pd.read_csv(file, delimiter=','))
        return generate_excel(dfs, request, get_last_8_letters(request.FILES['file1'].name))
    return render(request, 'index.html')

def report_client_report(df):
    df.columns = df.columns.str.strip()
    filtered_df = df[df['Status'] != 'Active']
    remaining_df = df[df['Status'] == 'Active']
    return remaining_df, filtered_df

def report_broker_report(df):
    date_columns = ['Received Date', 'Issue Date', 'Effective Date', 'Paid to Date', 'Subscriber DOB']

    # Estandarizar las fechas en las columnas especificadas al formato MM/DD/YYYY
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%m/%d/%Y')


    df.columns = df.columns.str.strip()
    active = df[df['Status'] == 'Active']
    active_grace_period = df[df['Status'] == 'Active (Grace Period) (Payment Error)']
    void_return = df[df['Status'] == 'Void-Return-Existing Insurance']
    active_but_date = df[(df['Status'] == 'Active (Payment Error)') & (df['Paid to Date'].notna()) & (df['Paid to Date'] != '')]
    active_but_no_date = df[(df['Status'] == 'Active (Payment Error)') & (df['Paid to Date'].isna() | (df['Paid to Date'] == ''))]
    automatic_termination = df[df['Status'] == 'Automatic Termination (Payment Error)']
    other_case = df[(df['Status'].notna()) &
                    (df['Status'] != '') &
                    (df['Status'] != 'Active') & 
                    (df['Status'] != 'Active (Payment Error)') & 
                    (df['Status'] != 'Active (Grace Period) (Payment Error)') & 
                    (df['Status'] != 'Void-Return-Existing Insurance') &
                    (df['Status'] != 'Automatic Termination (Payment Error)')]


    return active, active_grace_period, void_return, active_but_date, active_but_no_date, automatic_termination, other_case

def generate_excel(dfs, request, nameUwU):
    remaining_dfs = []
    filtered_dfs = []
    actives = []
    actives_grace_period = []
    voids_return = []
    actives_but_date = []
    actives_but_no_date = []
    automatic_terminations = []
    others_case = []

    if request.POST['report'] == 'client_report':
        for df in dfs:
            remaining_df, filtered_df = report_client_report(df)
            remaining_dfs.append(remaining_df)
            filtered_dfs.append(filtered_df)
    elif request.POST['report'] == 'broker_report':
        for df in dfs:
            active, active_grace_period, void_return, active_but_date, active_but_no_date, automatic_termination, other_case = report_broker_report(df)
            actives.append(active)
            actives_grace_period.append(active_grace_period)
            voids_return.append(void_return)
            actives_but_date.append(active_but_date)
            actives_but_no_date.append(active_but_no_date)
            automatic_terminations.append(automatic_termination)
            others_case.append(other_case)

    # Crear un nuevo archivo Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Escribir los DataFrames originales y filtrados en nuevas hojas
        
        if request.POST['report'] == 'client_report':
            sheet_names = {
                0: ("ACTIVE LAP & TRU", "CANCELADOS LAP & TRU"),
                1: ("ACTIVE SECURE", "CANCELADOS SECURE")
            }
            for i, (remaining_df, filtered_df) in enumerate(zip(remaining_dfs, filtered_dfs)):
                if not remaining_df.empty:
                    remaining_df.to_excel(writer, sheet_name=sheet_names[i][0], index=False)
                if not filtered_df.empty:
                    filtered_df.to_excel(writer, sheet_name=sheet_names[i][1], index=False)
                    
        elif request.POST['report'] == 'broker_report':
            sheet_names = {
                0: "Active Clients",
                1: "Actives Clients with payment",
                2: "Actives Clients Without payment",
                3: "Actives Clients in grace period",
                4: "Automatic Termination",
                5: "Void return",
                6: "Other cases",
            }
            for i, (active_client, active_grace_period, void_return, active_but_date, active_but_no_date, automatic_termination, other_case) in enumerate(zip(actives, actives_grace_period, voids_return, actives_but_date, actives_but_no_date, automatic_terminations, others_case)):
                print(actives_but_date)
                if not active_client.empty:
                    active_client.to_excel(writer, sheet_name=sheet_names[0], index=False)
                if not active_grace_period.empty:
                    active_grace_period.to_excel(writer, sheet_name=sheet_names[3], index=False)
                if not void_return.empty:
                    void_return.to_excel(writer, sheet_name=sheet_names[5], index=False)
                if not active_but_date.empty:
                    active_but_date.to_excel(writer, sheet_name=sheet_names[1], index=False)
                if not active_but_no_date.empty:
                    active_but_no_date.to_excel(writer, sheet_name=sheet_names[2], index=False)
                if not automatic_termination.empty:
                    automatic_termination.to_excel(writer, sheet_name=sheet_names[4], index=False)
                if not other_case.empty:
                    other_case.to_excel(writer, sheet_name=sheet_names[6], index=False)
        
        
        # Verificar si hay hojas en el archivo
        if len(writer.sheets) == 0:
            raise ValueError("No se pudo crear el archivo Excel, ya que no hay hojas visibles.")

    output.seek(0)

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Insxcloud - Client Report {nameUwU}.xlsx"'

    return response


def get_extension(file):
    file_name, extension = os.path.splitext(file.name)
    return extension

def get_last_8_letters(text):
  inicio = len(text) - 12
  final = len(text) -4
  last_8_letters = text[inicio:final]
  return last_8_letters