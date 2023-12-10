# Task Manager

Task Management is a Django-based web application designed to assist users in handling tasks and optimizing task allocation within a team or organization.
## Introduction


This system simplifies the organization and delegation of tasks, enabling users to seamlessly generate, allocate, and monitor tasks. It fosters effective communication and facilitates superior task management across teams or projects.
## Program features

- User Administration: Establish and oversee user accounts, allocate roles, and manage access privileges.
- Task Generation and Allocation: Generate tasks, allocate them to team members, and establish deadlines.
- Progress Monitoring: Track task advancement and stay updated on their status.
- Dashboard: Access an overview showcasing pending tasks, completed assignments, and ongoing tasks.

## Check it out!
[Task Manager deployed to Render](https://tasks-manager-sgu4.onrender.com)

You can use following superuser (or create another one by yourself):
  - Login: `testadminuser`
  - Password: `passwordadmin`

## Database schema
[You can find it here](https://dbdiagram.io/d/656b49c956d8064ca03fcfbb)

## Installation

Clone the project

```bash
  git clone https://github.com/Daniil-Pankieiev/tasks_manager.git
```

Open cloned folder

### Create virtual environment

On windows
```
  python -m venv venv
  venv\Scripts\activate
```
On macOS
```
  python3 -m venv venv
  source venv/bin/activate
```

Install dependencies

```
  pip install -r requirements.txt
```

### Set up DB

Migrate

```
  python manage.py migrate
```

Use the following command to load prepared data from fixture to test and debug your code:

`python manage.py loaddata data.json`

After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin1`
  - Password: `admin1`

### Run server
Finally, you can run server with
```
python manage.py runserver
```
Open a web browser and go to http://127.0.0.1:8000/ to access the Task Manager application.

Feel free to add more data using admin panel, if you need.
