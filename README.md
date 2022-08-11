# Elevator-problem

## Installation : 
1. Make a virtual enviornment in your preferred windows/Linux/...any system

2. Clone the repo and navigate to the directory where the manage.py file is located

3. Please read the special note point number 2 below, and go through the entire notes once.

4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the development server
```
python manage.py runserver
```

## Special Note :

1. The code is repeatative in some cases as I have used each view only for one type of request to provide a better understanding.

2. Redis caching is done for the entire site with a time limit of 5 minutes, so if you update the DB the changes in a cached device will appear 5 minutes later.

3. Please make sure redis is installed and running in your device. If it is running in a different port than 6379 then please go to Elevator/Settings.py and update it at line number : 158.

4. The elevator is running in a different thread and processes all the requests immediately. Check core/move_elevator.py and core/apps.py to know more details.

5. sqlite3 DB is used for portability in GitHub. Postgres code is also given in comment you can replace it.

4. Please check the models representation and API endpoints at [DOCS.md](https://github.com/Akash-Kumar-Sen/Elevator-problem/blob/main/DOCS.md)

5. Please share the scope of improvements you are able to see.
