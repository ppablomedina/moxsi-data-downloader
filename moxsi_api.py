import pandas as pd
import http.client
import json
import os


creds = os.getenv("MOXSI_API_CREDS")
USER = creds.split("\n")[0]
PASS = creds.split("\n")[1]

def download_stations_moxsi():

    # Petición inicial de login
    conn = http.client.HTTPSConnection("sw.moxsi.sagulpa.com")
    payload_login = f"{{\"service\": \"login\", \"user_name\": \"{USER}\", \"login_key\": \"{PASS}\"}}"
    headers = {'Content-Type': 'text/plain'}
    conn.request("POST", "/sw_login/v2/", payload_login, headers)

    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))

    # Extraer el token
    token = response_json.get("token")

    # Ahora usar el token en la siguiente petición
    payload_stations = "{\"service\": \"stations\",\"active\":1,\"service_type\":\"Sityneta\"}"
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f"Bearer {token}" 
    }
    conn.request("POST", "/moxsi_api/v5/", payload_stations, headers)

    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))

    stations_sityneta = response_json.get("stations")

    # Ahora usar el token en la siguiente petición
    payload_stations = "{\"service\": \"stations\",\"active\":1,\"service_type\":\"Sitycleta\"}"
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f"Bearer {token}" 
        }
    conn.request("POST", "/moxsi_api/v5/", payload_stations, headers)

    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))

    stations_sitycleta = response_json.get("stations")

    for station in stations_sityneta:  station['service_type'] = 'Sityneta'
    for station in stations_sitycleta: station['service_type'] = 'Sitycleta'

    # Combinar ambas listas en una sola
    combined_stations = stations_sityneta + stations_sitycleta

    # Convertir a DataFrame
    df_combined = pd.DataFrame(combined_stations)

    df_combined = df_combined.drop(columns=["external_id", "active", "city_id", "city_name"])

    df_combined["latitude"]  =  df_combined["latitude"].astype(float)
    df_combined["longitude"] = df_combined["longitude"].astype(float)

    return df_combined
