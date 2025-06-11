import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

############# API CONNECTION TO GOOGLE SHEETS ############# 

def load_data(sheet_name: str, worksheet_name: str) -> pd.DataFrame:
    # 1. Define el scope y crea las credenciales (usando secrets si estás en Streamlit Cloud)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]

    # Arreglar clave privada si viene como string con saltos reales
    key_info = dict(st.secrets["gcp_service_account"])
    key_info["private_key"] = key_info["private_key"].replace("\\n", "\n") if "\\n" in key_info["private_key"] else key_info["private_key"]

    # Desde secrets (recomendado para Streamlit Cloud)
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)

    # 2. Autenticación y conexión al Google Sheet
    client = gspread.authorize(creds)

    # 3. Abre el Google Sheet por su nombre (también puedes usar su URL o ID)
    spreadsheet = client.open(sheet_name)

    # 4. Selecciona la hoja "Transferencias"
    worksheet = spreadsheet.worksheet(worksheet_name)

    # 5. Convierte el contenido en DataFrame
    data = worksheet.get_all_records()  # devuelve una lista de diccionarios
    data_vsp = pd.DataFrame(data)


    ############# DATA CLEANING ############# 

    data_vsp.drop(['Transferencia','Fecha Valor','Semana C/P', 
        'Mes C/P', 'Año C/P', 'Mes I/G', 'Año I/G', 'Fecha evento', 'Cliente',
        'Tipo Actividad', 'comprobar duplicados','Fecha Grafico'], axis=1, inplace=True)
    data_vsp.columns = data_vsp.columns.str.lower()
    data_vsp = data_vsp[data_vsp["año"] != 1899]
    data_vsp = data_vsp.rename(columns={
        'valor ( + ) / ( - )': 'cantidad',
        'f. operativa': 'fecha',
        'grupo_1_fdc': 'tipo_transferencia',
        'grupo_2_fdc': 'grupo_principal_transferencia',
        'grupo_3_fdc': 'específico_transferencia',
        'grupos_flujo_de_caja': 'fijo_variable'
    })
    meses_map = {
        'ene': 'Enero',
        'feb': 'Febrero',
        'mar': 'Marzo',
        'abr': 'Abril',
        'may': 'Mayo',
        'jun': 'Junio',
        'jul': 'Julio',
        'ago': 'Agosto',
        'sept': 'Septiembre',
        'oct': 'Octubre',
        'nov': 'Noviembre',
        'dic': 'Diciembre'
    }

    data_vsp['mes'] = data_vsp['mes'].str.lower().map(meses_map)
    data_vsp['cantidad'] = data_vsp['cantidad'].str.replace('€', '', regex=False).str.replace('.', '', regex=False)
    data_vsp['cantidad'] = data_vsp['cantidad'].str.replace(',', '.', regex=False)
    data_vsp['fecha'] = pd.to_datetime(data_vsp['fecha'], format='%d/%m/%Y')
    data_vsp['cantidad'] = data_vsp['cantidad'].astype(float)

    return data_vsp