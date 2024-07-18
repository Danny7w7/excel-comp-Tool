from django.shortcuts import render, HttpResponse

from io import BytesIO

import pandas as pd
import openpyxl
import os

# Create your views here.


def index(request):
    if request.method == 'POST':
        files = [request.FILES['file1'], request.FILES['file2']]
        dfs = []
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
    filtered_df = df[df['Provider Status'] != 'Active']
    remaining_df = df[df['Provider Status'] == 'Active']
    return remaining_df, filtered_df

def generate_excel(dfs, request, nameUwU):
    remaining_dfs = []
    filtered_dfs = []

    if request.POST['report'] == 'client_report':
        for df in dfs:
            remaining_df, filtered_df = report_client_report(df)
            remaining_dfs.append(remaining_df)
            filtered_dfs.append(filtered_df)

    # Crear un nuevo archivo Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Escribir los DataFrames originales y filtrados en nuevas hojas
        sheet_names = {
            0: ("ACTIVE LAP & TRU", "CANCELADOS LAP & TRU"),
            1: ("ACTIVE SECURE", "CANCELADOS SECURE")
        }
        for i, (remaining_df, filtered_df) in enumerate(zip(remaining_dfs, filtered_dfs)):
            remaining_df.to_excel(writer, sheet_name=sheet_names[i][0], index=False)
            filtered_df.to_excel(writer, sheet_name=sheet_names[i][1], index=False)


    # Configurar el puntero del buffer al inicio
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