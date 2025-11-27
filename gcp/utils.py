from gcp.paths    import BUCKET_NAME
from google.cloud import storage
import pandas as pd  
import mimetypes
import io


BUCKET = storage.Client().bucket(BUCKET_NAME)

def upload_to_gcp(files_dict):
    
    for gcs_path, obj in files_dict.items():

        # Caso 1: DataFrame -> CSV en memoria
        if isinstance(obj, pd.DataFrame):
            csv_buffer = io.StringIO()
            obj.to_csv(csv_buffer, index=False)
            data = csv_buffer.getvalue().encode("utf-8")
            content_type = "text/csv"

        # Caso 2: ruta local a archivo
        elif isinstance(obj, str):
            with open(obj, "rb") as f: data = f.read()
            # intenta deducir content-type por extensión
            content_type = mimetypes.guess_type(obj)[0] or "application/octet-stream"

        # Caso 3: bytes ya preparados
        elif isinstance(obj, (bytes, bytearray)):
            data = obj
            content_type = mimetypes.guess_type(gcs_path)[0] or "application/octet-stream"

        else: raise TypeError(f"Tipo no soportado para el valor asociado a '{gcs_path}': {type(obj)}")

        # Subida al bucket (se asume que 'bucket' ya está creado)
        blob = BUCKET.blob(gcs_path)
        blob.upload_from_string(data, content_type=content_type)
