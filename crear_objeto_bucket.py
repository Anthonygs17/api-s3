import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']

    # Proceso
    s3 = boto3.client('s3')

    try:
        # S3 no tiene carpetas reales, creamos un objeto vacío con nombre terminado en '/'
        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'

        s3.put_object(Bucket=nombre_bucket, Key=nombre_directorio)

        # Salida
        return {
            'statusCode': 200,
            'bucket': nombre_bucket,
            'directorio': nombre_directorio,
            'mensaje': f'Directorio "{nombre_directorio}" creado exitosamente en el bucket "{nombre_bucket}".'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'bucket': nombre_bucket,
            'directorio': nombre_directorio,
            'mensaje': f'Error al crear el directorio: {str(e)}'
        }
