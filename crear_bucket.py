import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    region = event['body'].get('region', 'us-east-1')

    # Proceso
    s3 = boto3.client('s3', region_name=region)
    
    try:
        # En us-east-1 no se pasa CreateBucketConfiguration
        if region == 'us-east-1':
            s3.create_bucket(Bucket=nombre_bucket)
        else:
            s3.create_bucket(
                Bucket=nombre_bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        # Salida
        return {
            'statusCode': 200,
            'bucket': nombre_bucket,
            'mensaje': f'Bucket "{nombre_bucket}" creado exitosamente en la región {region}.'
        }

    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 409,
            'bucket': nombre_bucket,
            'mensaje': 'El bucket ya existe a nivel global.'
        }

    except s3.exceptions.BucketAlreadyOwnedByYou:
        return {
            'statusCode': 409,
            'bucket': nombre_bucket,
            'mensaje': 'Ya posees un bucket con ese nombre.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'bucket': nombre_bucket,
            'mensaje': f'Error al crear el bucket: {str(e)}'
        }
