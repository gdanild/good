from pathlib import Path
import json, requests,time
class user_work():

    CLIENT_VERSION = '1.6.0'
    AWS_API_KEY = 'yqKeRnxGX77NSeqvX3YyQ5VBio3SJcJ44iOfOnBX'
    AWS_CLIENT_ID = '7g1h82vpnjve0omfq1ssko18gl'
    AWS_API_VERSION = '1.0'
    WHOOSH_API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBfaWQiOiI0YWZkMTU4MzgyYjMwOTA4ZWRhZiJ9.GbmM6dzdATpQzfS9Rqd4QIYJCAgMHFQp1oFj-uw7uT4'

    def __init__(self):
        credentials_file = Path('credentials.json')
        with credentials_file.open('r') as cred_file:
            user_datas = dict(json.load(cred_file))
        self.user_data = user_datas
        if not self.login():
            print("I WONT UPDATE TOKEN")
            self.refrech_token()

    def get_headers(self):
        headers = {
            'User-Agent': 'okhttp/3.12.1',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Id-Token': self.user_data["id_token"],
            'X-Auth-Token': self.user_data["auth_token"],
            'X-Api-Key': self.AWS_API_KEY,
            'X-Client': 'android',
            'X-Client-Version': self.CLIENT_VERSION,
            'X-Api-Version': '1.0',
            'x-client-uuid': self.user_data["device_id"],
        }
        return headers

    def refrech_token(self):
        headers = {
            'User-Agent': 'aws-sdk-android/2.22.5 Linux/4.14.180-perf-g6a605b68c08e Dalvik/2.1.0/0 en_US',
            'Content-Type': 'application/x-amz-json-1.1',
            'aws-sdk-retry': '0/0',
            'accept-language': 'en-US,en;q=0.5',
            'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
        }

        datav = {
            'AuthFlow': 'REFRESH_TOKEN_AUTH',
            'AuthParameters': {'REFRESH_TOKEN': self.user_data["refresh_token"]},
            'ClientId': self.AWS_CLIENT_ID,
            'UserContextData': {}
        }
        data_result = requests.post('https://cognito-idp.us-east-1.amazonaws.com', data=json.dumps(datav),
                                    headers=headers)
        self.user_data["id_token"] = data_result.json()['AuthenticationResult']['IdToken']
        self.user_data["auth_token"] = data_result.json()['AuthenticationResult']['AccessToken']
        with open('credentials.json', 'w') as cred_file:
            cred_file.write(json.dumps(self.user_data))
            print("I AM UPDATE TOKEN BITCH")
        return True

    def login(self):
        result = requests.get(f'https://api.whoosh.bike/v0/users/logged', headers=self.get_headers())
        if result.status_code == 401: return False
        elif result.status_code==200: return True
        else:
            print("WHAT THE FUCK")
            return True

    def regions(self, start_lat, start_lng):
        while True:
            result = requests.get(f'https://api.whoosh.bike/v0/regions/id?lat={start_lat}&lng={start_lng}', headers=self.get_headers())
            if result.status_code==401: self.refrech_token()
            else: break
        if len(result.json().keys()) <= 0:
            print('NOOOO FUCKIN REGIONS',start_lat,"   ",start_lng)
            return False
   #     print(result.json())
        return {"id":result.json()["region"]["id"],
                "name": result.json()["region"]["name"]}


    def get_scooters(self, coord, region_id):
        time.sleep(0.01)
        data = {
            'clientSearchDevicesParams': {
                'regionId': region_id,
                'visibleArea': {
                    'bottomRight': {'lat': coord["bottom"]["lat"], 'lng': coord["bottom"]["lng"]},
                    'upperLeft': {'lat': coord["upper"]["lat"], 'lng': coord["upper"]["lng"]},
                }
            }
        }

        while True:
            result = requests.post(f'https://api.whoosh.bike/v0/client/devices/searches', data=json.dumps(data), headers=self.get_headers())
            if result.status_code == 401: self.refrech_token()
            else: break
        return result.json()

    def get_zones(self, start_lat, start_lng):
        while True:
            result = requests.get(f'https://api.whoosh.bike/v0/regions/location?lat={start_lat}&lng={start_lng}', headers=self.get_headers())
            if result.status_code==401: self.refrech_token()
            else: break
        if list(result.json().keys())[0]=="wishVote": return False
        return result.json()




