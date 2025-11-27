import pandas as pd


BUCKET_NAME        = "sagulpa-datalake"
PATH_DATALAKE_DOCS = "moxsi/documents"

# Fechas base
now = pd.Timestamp.now()

crrnt_full_date = now.strftime("%Y%m%d")  # p.ej. 20251127
crrnt_year      = now.year

prev_month_ts   = now - pd.DateOffset(months=1)
prev_year       = prev_month_ts.year
prev_month_str  = prev_month_ts.strftime("%Y%m")  # p.ej. 202510

# Helpers para construir rutas
def monthly_path(dataset: str, ext: str = "csv"):
    """
    Documentos mensuales: carpeta = mes anterior (YYYYMM),
    fichero = mes anterior (YYYYMM.ext).
    """
    return f"{PATH_DATALAKE_DOCS}/{prev_month_str}/{dataset}/{prev_month_str}.{ext}"

def daily_path_year(dataset: str, ext: str = "csv"):
    """
    Documentos diarios: carpeta = año actual,
    fichero = fecha completa actual (YYYYMMDD.ext).
    """
    return f"{PATH_DATALAKE_DOCS}/{crrnt_year}/{dataset}/{crrnt_full_date}.{ext}"


# Rutas
path_recaudacion              = monthly_path("financiero.recaudacion", ext="csv")
path_incidencias              = monthly_path("moxsi.incidencias", ext="xlsx")
path_inventario               = monthly_path("moxsi.inventario", ext="csv")
path_repuestos                = monthly_path("moxsi.repuestos", ext="xlsx")
path_revisiones               = monthly_path("moxsi.revisiones", ext="xlsx")
path_abonos                   = monthly_path("nextbike.abonos", ext="csv")
path_clientes_detalles        = monthly_path("nextbike.clientes-detalles", ext="csv")
path_alquileres               = monthly_path("nextbike.alquileres", ext="csv")
path_alquileres_con_abono     = monthly_path("nextbike.alquileres-con-abono", ext="csv")
path_alquileres_sin_abono     = monthly_path("nextbike.alquileres-sin-abono", ext="csv")

path_estaciones               = daily_path_year("moxsi.estaciones", ext="csv")
path_vehiculos_anclados       = daily_path_year("nextbike.vehiculos-anclados", ext="csv")
path_vehiculos_coords         = daily_path_year("nextbike.vehiculos-coords", ext="csv")
path_clientes_registrados     = daily_path_year("nextbike.clientes-registrados", ext="csv")
path_clientes_ultimo_alquiler = daily_path_year("nextbike.clientes-ult-alquiler-suscripciones", ext="csv")
