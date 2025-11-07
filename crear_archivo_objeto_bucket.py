import boto3
import base64

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']
    nombre_archivo = event['body']['archivo']
    contenido_base64 = event['body']['contenido']  # el archivo viene codificado en base64

    # Asegurar que el directorio termine con "/"
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'

    # Ruta completa del archivo dentro del bucket
    key = f"{nombre_directorio}{nombre_archivo}"

    # Decodificar el contenido base64
    contenido_bytes = base64.b64decode(contenido_base64)

    # Proceso
    s3 = boto3.client('s3')
    
    try:
        # Subir el archivo
        s3.put_object(Bucket=nombre_bucket, Key=key, Body=contenido_bytes)

        # Salida
        return {
            'statusCode': 200,
            'bucket': nombre_bucket,
            'archivo': key,
            'mensaje': f'Archivo "{nombre_archivo}" subido correctamente a "{nombre_directorio}" en el bucket "{nombre_bucket}".'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'bucket': nombre_bucket,
            'archivo': key,
            'mensaje': f'Error al subir el archivo: {str(e)}'
        }
