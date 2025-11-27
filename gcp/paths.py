import pandas as pd


BUCKET_NAME        = 'sagulpa-datalake'
PATH_DATALAKE_DOCS = 'moxsi/documents'

current_month   = pd.Timestamp.now()
crrnt_full_date = current_month.strftime("%Y%m%d")
crrnt_year      = current_month.year
prev_month      = pd.Timestamp.now() - pd.DateOffset(months=1)
prev_year       = prev_month.year
prev_date       = prev_month.strftime("%Y%m")

path_recaudacion              = f'{PATH_DATALAKE_DOCS}/{prev_month}/financiero.recaudacion'                       + f'/{date}.csv'
path_estaciones               = f'{PATH_DATALAKE_DOCS}/{crrnt_year}/moxsi.estaciones'                             + f'/{crrnt_full_date}.csv'
path_incidencias              = f'{PATH_DATALAKE_DOCS}/{prev_month}/moxsi.incidencias'                            + f'/{date}.xlsx'  
path_inventario               = f'{PATH_DATALAKE_DOCS}/{prev_month}/moxsi.inventario'                             + f'/{date}.csv'
path_repuestos                = f'{PATH_DATALAKE_DOCS}/{prev_month}/moxsi.repuestos'                              + f'/{date}.xlsx'
path_revisiones               = f'{PATH_DATALAKE_DOCS}/{prev_month}/moxsi.revisiones'                             + f'/{date}.xlsx'
path_abonos                   = f'{PATH_DATALAKE_DOCS}/{prev_month}/nextbike.abonos'                              + f'/{date}.csv'
path_vehiculos_anclados       = f'{PATH_DATALAKE_DOCS}/{crrnt_year}/nextbike.vehiculos-anclados'                  + f'/{crrnt_full_date}.csv'
path_vehiculos_coords         = f'{PATH_DATALAKE_DOCS}/{crrnt_year}/nextbike.vehiculos-coords'                    + f'/{crrnt_full_date}.csv'
path_clientes_registrados     = f'{PATH_DATALAKE_DOCS}/{crrnt_year}/nextbike.clientes-registrados'                + f'/{crrnt_full_date}.csv'
path_clientes_ultimo_alquiler = f'{PATH_DATALAKE_DOCS}/{crrnt_year}/nextbike.clientes-ult-alquiler-suscripciones' + f'/{crrnt_full_date}.csv'
path_clientes_detalles        = f'{PATH_DATALAKE_DOCS}/{prev_month}/nextbike.clientes-detalles'                   + f'/{date}.csv'
path_alquileres               = f'{PATH_DATALAKE_DOCS}/{prev_month}/nextbike.alquileres'                          + f'/{date}.csv'
path_alquileres_con_abono     = f'{PATH_DATALAKE_DOCS}/{prev_month}/nextbike.alquileres-con-abono'                + f'/{date}.csv'
path_alquileres_sin_abono     = f'{PATH_DATALAKE_DOCS}/{prev_month}/nextbike.alquileres-sin-abono'                + f'/{date}.csv'
