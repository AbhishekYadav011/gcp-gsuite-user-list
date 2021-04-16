# gcp-gsuite-user-list
This repo is created to get the user list from G-suite using Workspace Admin SDK

## Set the value of below [varibales](https://developers.google.com/admin-sdk/directory/v1/guides/delegation#python) before executing this code:
1. SERVICE_ACCOUNT_EMAIL = 'service account email id'
2. SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'p12 file path'
3. user_eamil_id


# execute the code ,it will download userlist.txt file in your working directory.
> python getgcpuserlist.py
