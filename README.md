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
[Task Manager deployed to Render](https://task-manager-uf55.onrender.com/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/task-manager.git
   
2. **Navigate to the project directory:**
   ```bash
   cd task-manager
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
4. **Apply database migrations:**
   ```bash
   python manage.py migrate
5. **Start the development server:**
   ```bash
   python manage.py runserver
6. **Access the application:**
Open a web browser and go to http://127.0.0.1:8000/ to access the Task Manager application.


Use the following command to load prepared data from fixture to test and debug your code:
  
`python manage.py loaddata data.json`

- After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin`
  - Password: `admin123`

Feel free to add more data using admin panel, if you need.