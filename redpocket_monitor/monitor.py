
import configparser
import datetime
import json
import re
import requests

from pprint import pprint

POST_URL = 'https://www.redpocket.com/login'
GET_DETAILS_ID_URL = 'https://www.redpocket.com/account/get-other-lines'
GET_PARAMS_URL = 'https://www.redpocket.com/account/get-details?id=%s&type=api'

def extract_csrf_from_html( html_text ):
    re_tag = r'<input type="hidden" name="csrf" value="([\w|-]+)">'
    match = re.search( re_tag, html_text )
    if match: 
        return match.group( 1 )
    return None

if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read( 'redpocket.ini' )

    client = requests.session()

    r = client.get( url=POST_URL )

    payload = {
      'mdn' : parser[ 'redpocket.com' ][ 'username' ],
      'password' : parser[ 'redpocket.com' ][ 'password' ],
      'csrf' : extract_csrf_from_html( r.text ),
    }

    r = client.post( url=POST_URL, data=payload )

    r = client.get( url=GET_DETAILS_ID_URL )
    params = json.loads( r.text )
    details_id = params[ 'return_data' ][ 'confirmedLines' ][ 0 ][ 'hash' ]

    r = client.get( url=GET_PARAMS_URL % details_id )
    params = json.loads( r.text )
    data = params[ 'return_data' ]
    pprint( data )
