

To run this application, you must have vagrant installed and connected via ssh.

Then cd into the current directory. It's best you have 2 command windows:

- 1st is used for **psql** environment. so type ``` psql ```. Because the database creation, connection and table creation are all writen in the **tournament.sql** file. To import this file, type ``` \i tournament.sql```then the setup is done. 
- 2nd is used for **python** environment. type ``` python tournament_test.py``` to run the test. 


Note that vagrant has preinstalled the above 2 languages with versions: psql 9.3 and python 2.7.6


