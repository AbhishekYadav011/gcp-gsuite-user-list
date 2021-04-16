from __future__ import print_function
import re
import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

regex = '^[\w.+\-]+@sap\.com$'


def main():
    """Cloud db login to get I/D/C number of employee using their email id"""
    clouddb_url = 'https://db.multicloud.int.sap/jwt-token/'
    # using clouddb credentials to get token for authentication
    data = {'username': 'i334554', 'password': 'M@nager0'}
    # Email of the Service Account
    SERVICE_ACCOUNT_EMAIL = 'gcp-user-details@sap-mc-gcp-core-prod.iam.gserviceaccount.com'
    SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'C:\\Users\\I334554\\learning\\sap-mc-gcp-core-prod-204f6d1a850c.p12'
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=['https://www.googleapis.com/auth/admin.directory.user'])
    credentials = credentials.create_delegated('abhishek.yadav01@sap.com')
    service = build('admin', 'directory_v1', credentials=credentials)

    # Call the Admin SDK Directory API
    print('Getting the users list in the domain')
    results = service.users().list(customer='my_customer',
                                   orderBy='email').execute()
    print(results.get('nextPageToken'))
    nextPageToken = results.get('nextPageToken')
    users = results.get('users', [])
    userlist = open("userlist.txt", "w+")

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            if not user['suspended']:
                print(u'{0} ({1})'.format(user['primaryEmail'],
                                          user['name']['fullName']))
                if re.search(regex, user['primaryEmail']):
                    clouddb_response = requests.post(clouddb_url, data=data)
                    clouddb_access = clouddb_response.json()
                    bearer = (clouddb_access['access'])
                    headers = {"Authorization": 'Bearer ' + bearer}
                    creator_account_list_url = "https://db.multicloud.int.sap/sapmc/users/{}".format(
                        user['primaryEmail'])
                    creator_account_list_request = requests.get(creator_account_list_url, headers=headers)
                    creator_account_list_response = creator_account_list_request.json()
                    # print(creator_account_list_response['inum'])
                    userlist.write(creator_account_list_response['inum'] + "\n")
    userlist.close()

    while nextPageToken is not None:
        results = service.users().list(customer='my_customer',
                                       orderBy='email', pageToken=nextPageToken).execute()
        users = results.get('users', [])
        userlist_append = open("userlist.txt", "a+")
        if not users:
            print('No users in the domain.')
        else:
            # print('Users:')
            for user in users:
                if not user['suspended']:
                    print(u'{0} ({1})'.format(user['primaryEmail'],
                                              user['name']['fullName']))
                    if re.search(regex, user['primaryEmail']):
                        clouddb_response = requests.post(clouddb_url, data=data)
                        clouddb_access = clouddb_response.json()
                        bearer = (clouddb_access['access'])
                        headers = {"Authorization": 'Bearer ' + bearer}
                        creator_account_list_url = "https://db.multicloud.int.sap/sapmc/users/{}".format(
                            user['primaryEmail'])
                        creator_account_list_request = requests.get(creator_account_list_url, headers=headers)
                        creator_account_list_response = creator_account_list_request.json()
                        # data = json.loads(creator_account_list_response)
                        # print(creator_account_list_response['inum'])
                        if 'inum' in creator_account_list_response:
                            userlist_append.write(creator_account_list_response['inum'] + "\n")

        if results.get('nextPageToken') is not None:
            # print(results.get('nextPageToken'))
            nextPageToken = results.get('nextPageToken')
        else:
            print("loop done")
            break


if __name__ == '__main__':
    main()
