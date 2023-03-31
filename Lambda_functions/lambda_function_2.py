import json
import boto3
import base64

runtime = boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2023-03-31-21-21-34-686'

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["image_data"])

    # Instantiate a Predictor
    # For this model the IdentitySerializer needs to be "image/png"
    # Make a prediction:
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,ContentType='image/png',Body=image)
    inferences = response['Body'].read()
    # We return the data back to the Step Function    
    event["inferences"] = json.loads(inferences.decode('utf-8'))
    return {
        'statusCode': 200,
        'body': event
    }