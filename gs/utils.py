from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
import os
import io


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# El secreto se inyecta en la env var como texto JSON
creds_info = json.loads(os.environ["GS_SERVICE_ACCOUNT_CREDS"])

creds = Credentials.from_service_account_info(
    creds_info,
    scopes=SCOPES,
)

# Autenticarse con gspread
CLIENT = gspread.authorize(creds)


def download_from_gs_excel(sheet_url):
    """(igual que antes) descarga TODAS las hojas a un Excel en memoria."""
    sh = CLIENT.open_by_url(sheet_url)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for ws in sh.worksheets():
            values = ws.get_all_values()
            header = values[0]
            rows = values[1:]
            df = pd.DataFrame(rows, columns=header)

            sheet_name = (ws.title or "Sheet")[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output.getvalue()


def download_from_gs_single_sheet(sheet_url, sheet_name=None):
    """
    Descarga SOLO una hoja de un Google Sheet y la devuelve como DataFrame.
    Luego `upload_to_gcp` la subirá como CSV.
    """
    sh = CLIENT.open_by_url(sheet_url)
    ws = sh.worksheet(sheet_name) if sheet_name else sh.sheet1

    values = ws.get_all_values()
    if not values: return pd.DataFrame()

    header = values[0]
    rows = values[1:]

    return pd.DataFrame(rows, columns=header)
