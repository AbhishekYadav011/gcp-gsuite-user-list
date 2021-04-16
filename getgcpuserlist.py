from __future__ import print_function
import re
import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def main():
    # Email of the Service Account
    SERVICE_ACCOUNT_EMAIL = 'service account email id'
    SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'p12 file path'
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=['https://www.googleapis.com/auth/admin.directory.user'])
    credentials = credentials.create_delegated('user_eamil_id')
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
                userlist.write(user['primaryEmail'] + "\n")
                
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
                    userlist_append.write(user['primaryEmail'] + "\n")
              
                            

        if results.get('nextPageToken') is not None:
            # print(results.get('nextPageToken'))
            nextPageToken = results.get('nextPageToken')
        else:
            print("loop done")
            break


if __name__ == '__main__':
    main()
