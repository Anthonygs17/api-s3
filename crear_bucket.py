import boto3
import json

def lambda_handler(event, context):
    # Entrada: se espera que el nombre del bucket venga en el evento
    # Ejemplo: {"bucket_name": "mi-nuevo-bucket-prueba"}
    bucket_name = event.get("bucket_name")
    region = event.get("region", "us-east-1")  # región por defecto

    if not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe especificar el nombre del bucket.'})
        }

    # Proceso
    s3 = boto3.client('s3', region_name=region)
    try:
        if region == 'us-east-1':
            # En us-east-1 no se debe pasar CreateBucketConfiguration
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        # Salida
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Bucket "{bucket_name}" creado exitosamente en la región {region}.'
            })
        }

    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 409,
            'body': json.dumps({'error': 'El bucket ya existe a nivel global.'})
        }
    except s3.exceptions.BucketAlreadyOwnedByYou:
        return {
            'statusCode': 409,
            'body': json.dumps({'error': 'Ya posees un bucket con ese nombre.'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
