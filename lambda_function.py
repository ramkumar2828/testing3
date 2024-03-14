import base64
import urllib.parse
import xml.etree.ElementTree as ET

def lambda_handler(event, context):
    try:
        encoded_saml_response = event['encoded_saml_response']
        decoded_saml_response = decode_saml_response(encoded_saml_response)
        
        root = ET.fromstring(decoded_saml_response)
        namespace = {'saml': 'urn:oasis:names:tc:SAML:2.0:assertion'}
        name_id = root.find('.//saml:NameID', namespace)
        email = name_id.text.strip() if name_id is not None else None
        
        return {
            'statusCode': 200,
            'body': {
                'email': email
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'message': 'Internal Server Error',
                'error': str(e)
            }
        }

def decode_saml_response(encoded_saml_response):
    uri_decoded_saml_response = urllib.parse.unquote(encoded_saml_response)
    decoded_saml_response = base64.b64decode(uri_decoded_saml_response)
    saml_response_xml = decoded_saml_response.decode('utf-8')
    return saml_response_xml
