# oktaCreateUsers
Create okta users using the okta api.  This script is meant to be used if you have to register a large number of users, which would require many clicks and a lot of data entry.  It reads in the users and defined groups the users should be added to, verifies the groups exist, then attempts to add the user and assign the specified groups.

Example
```text
# docker run -it --rm -v ./veris-support-scripts:/veris-support-scripts python:3.12.3 bash
# pip install requests
# cd veris-support-scripts/
# python oktaCreateUsers.py
[+] Attempting to create user testuser1@axoni.com,test,user1,['group1']
[+] User testuser1@axoni.com successfully created with ID: user1
[+] User testuser1@axoni.com (user1) added to group company-A (group1)

[+] Attempting to create user testuser2@axoni.com,test,user2,['group2', 'group3']
[+] User testuser2@axoni.com successfully created with ID: user2
[+] User testuser2@axoni.com (user2) added to group company-D (group2)
[+] User testuser2@axoni.com (user2) added to group role-ui-full (group3)

[+] Attempting to create user testuser3@axoni.com,test,user3,['group4', 'group5', 'group6', 'group7']
[+] User testuser3@axoni.com successfully created with ID: user3
[+] User testuser3@axoni.com (user3) added to group company-B (group4)
[+] User testuser3@axoni.com (user3) added to group role-ui-read-only (group5)
[+] User testuser3@axoni.com (user3) added to group company-AXONI (group6)
[+] User testuser3@axoni.com (user3) added to group Master Support Engineering Department (group7)
