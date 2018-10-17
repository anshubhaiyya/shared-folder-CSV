import json
import requests, base64
import os                             # Allows for the clearing of the Terminal Window
import glob
import getpass
import dropbox
import numpy as np
import csv
# -*- coding: utf-8 -*-


print("This program will export all Shared Folder relationships in your Dropbox account as a CSV")

print("First we need a Dropbox API token from you: ")
dbxtoken = getpass.getpass()

dbx = dropbox.Dropbox(dbxtoken)
listSharedFolders = []
initFolder = dbx.sharing_list_folders()
listSharedFolders = listSharedFolders + initFolder.entries
cursor = initFolder.cursor
while cursor is not None:
    folderLoop = dbx.sharing_list_folders_continue(initFolder.cursor)
    cursor = folderLoop.cursor
    listSharedFolders = listSharedFolders + folderLoop.entries
sharedFolders = np.asarray(listSharedFolders)
CSV = ['Name,Location,Owner Name,Membership Policy,Team Folder?,Preview URL\n']
for i in range(0, len(sharedFolders)):
    CSV = CSV + [str(sharedFolders[i].name.encode('latin1')) + ',' +
                 str(sharedFolders[i].path_lower) + ',' +
                 str(sharedFolders[i].owner_team.name.encode('latin1')) + ',' +
                 str(sharedFolders[i].policy.member_policy).split("'")[1] + ',' +
                 str(sharedFolders[i].is_team_folder) + ',' +
                 str(sharedFolders[i].preview_url.encode('latin1')) + '\n']

'''
    print(CSV[j])
    print('line ' + str(j))
'''

with open("test.csv", "wb") as exportFile:
    wr = csv.writer(exportFile, lineterminator='\n', dialect="excel")
    wr.writerow(CSV)

print('file written')