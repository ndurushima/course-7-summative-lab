import argparse
from models.project import Project
from models.user import User

#Global dictionary to store user projects and tasks
users = {}

# Function to add a project
def add_project(args):
    if args.user not in users:
        # Create a new user if it doesn't exist
        users[args.user] = User(name=args.user, email=args.email)

    user = users[args.user]
    project = Project.create(
        user_id=user.id,
        title=args.title,
        description=args.description,
        due_date=args.due_date
    )
    print(f"Project '{project.id}' created for user '{user.name}' with title '{project.title}' (due: {project.due_date})")
    

# Function to add a task to a project
def add_task(args):
    user = users.get(args.user)
    if user is None:
        print(f"User '{args.user}' does not exist.")
        return
        
    project = Project.get(args.project_id)
    if project is None:
        print(f"Project with ID '{args.project_id}' does not exist.")
        return
    
    task = project.add_task(
        title=args.title,
        status=args.status,
        assigned_to=user.id
    )
    print(f"Task created for project {project.id}: [{task.id}] {task.title} - {task.status}")

#CLI Entry Point
def main():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers()

    # Subparser for adding a project
    parser_add_project = subparsers.add_parser('add_project', help='Add a new project')
    parser_add_project.add_argument('user', type=str, help='User name')
    parser_add_project.add_argument('email', type=str, help='User email')
    parser_add_project.add_argument('title', type=str, help='Project title')
    parser_add_project.add_argument('description', type=str, help='Project description')
    parser_add_project.add_argument('due_date', type=str, help='Project due date (YYYY-MM-DD)')
    parser_add_project.set_defaults(func=add_project)   

    # Subparser for adding a task
    parser_add_task = subparsers.add_parser('add_task', help='Add a new task')
    parser_add_task.add_argument('user', type=str, help='User name')
    parser_add_task.add_argument('project_id', type=int, help='Project ID')
    parser_add_task.add_argument('title', type=str, help='Task title')
    parser_add_task.add_argument('status', type=str, help='Task status')
    parser_add_task.set_defaults(func=add_task)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

