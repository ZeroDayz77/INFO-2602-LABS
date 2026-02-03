from typing import Annotated
import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User, Todo, TodoCategory, Category
from fastapi import Depends
from sqlmodel import select
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

cli = typer.Typer()

@cli.command()
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        bob = User(username='bob', email='bob@mail.com', password='bobpass') # Create a new user (in memory)
        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)

        new_todo = Todo(text='Wash dishes', user_id=bob.id)

        db.add(new_todo) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(new_todo) # Update the user (we use this to get the ID from the db)

        print("Database Initialized")

@cli.command()
def get_user(username: Annotated[str, typer.Argument(help="Username of the user to retrieve")]):
    with get_session() as db: # Get a connection to the database
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f'{username} not found!')
            return
        print(user)

@cli.command()
def get_all_users():
    with get_session() as db:
        users = db.exec(select(User)).all()
        if not users:
            print("No users found!")
            return
        else:
            for user in users:
                print(user)


@cli.command()
def change_email(username: Annotated[str, typer.Argument(help="Username of the user to update")], new_email: Annotated[str, typer.Argument(help="New email address")]):
    with get_session() as db: # Get a connection to the database
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f'{username} not found! Unable to update email.')
            return
        user.email = new_email
        db.add(user)
        db.commit()
        print(f"Updated {user.username}'s email to {user.email}")

@cli.command()
def create_user(username: Annotated[str, typer.Argument(help="Username of the new user")], email: Annotated[str, typer.Argument(help="Email of the new user")], password: Annotated[str, typer.Argument(help="Password of the new user")]):
    with get_session() as db: # Get a connection to the database
        new_user = User(username=username, email=email, password=password)
        try:
            db.add(new_user)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            print(e.orig)
            print("Username or email already exists. Unable to create user.")
        else:
            print(new_user)

@cli.command()
def delete_user(username: Annotated[str, typer.Argument(help="Username of the user to delete")]):
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f'{username} not found! Unable to delete user.')
            return
        db.delete(user)
        db.commit()
        print(f'{username} deleted')

@cli.command()
def find_user_partial(partial_word: Annotated[str, typer.Argument(help="Partial username or email to search for")]):
    with get_session() as db:
        users = db.exec(
            select(User).where(
                or_(
                    User.username.contains(partial_word),
                    User.email.contains(partial_word),
                )
            )
        ).all()
        if not users:
            print(f'No users found with username containing "{partial_word}".')
            return
        for user in users:
            print(user)
            
@cli.command()
def list_users(limit: Annotated[int, typer.Argument(help="Number of users to display")] = 10, offset: Annotated[int, typer.Argument(help="Number of users to skip")] = 0):
    with get_session() as db:
        users = db.exec(select(User).offset(offset).limit(limit)).all()
        if not users:
            print("No users found!")
            return
        for user in users:
            print(user)

@cli.command()
def add_task(username:str, task:str):
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User doesn't exist")
            return
        user.todos.append(Todo(text=task))
        db.add(user)
        db.commit()
        print("Task added for user")

@cli.command()
def toggle_todo(todo_id:int, username:str):
    with get_session() as db:
        todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
        if not todo:
            print("This todo doesn't exist")
            return
        if todo.user.username != username:
            print(f"This todo doesn't belong to {username}")
            return

        todo.toggle()
        db.add(todo)
        db.commit()

        print(f"Todo item's done state set to {todo.done}")

@cli.command()
def list_todo_categories(todo_id:int, username:str):
    with get_session() as db: # Get a connection to the database
        todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
        if not todo:
            print("Todo doesn't exist")
        elif not todo.user.username == username:
            print("Todo doesn't belong to that user")
        else:
            print(f"Categories: {todo.categories}")

@cli.command()
def create_category(username:str, cat_text:str):
    with get_session() as db: # Get a connection to the database
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User doesn't exist")
            return

        category = db.exec(select(Category).where(Category.text== cat_text, Category.user_id == user.id)).one_or_none()
        if category:
            print("Category exists! Skipping creation")
            return
        
        category = Category(text=cat_text, user_id=user.id)
        db.add(category)
        db.commit()

        print("Category added for user")

@cli.command()
def list_user_categories(username:str):
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User does not exist")
            return
        categories = db.exec(select(Category).where(Category.user_id == user.id)).all()
        print([category.text for category in categories])

@cli.command()
def assign_category_to_todo(username:str, todo_id:int, category_text:str):
    with get_session() as db: # Get a connection to the database
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User doesn't exist")
            return
        
        category = db.exec(select(Category).where(Category.text == category_text, Category.user_id==user.id)).one_or_none()
        if not category:
            category = Category(text=category_text, user_id=user.id)
            db.add(category)
            db.commit()
            print("Category didn't exist for user, creating it")
        
        todo = db.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id==user.id)).one_or_none()
        if not todo:
            print("Todo doesn't exist for user")
            return
        
        todo.categories.append(category)
        db.add(todo)
        db.commit()
        print("Added category to todo")

@cli.command()
def list_all_todos():
    with get_session() as db:
        todos =  db.exec(select(Todo)).all()

        for todo in todos:
            print(todo.id, todo.text, todo.user.username, todo.done)

@cli.command()
def delete_todo_by_id(id:int):
    with get_session() as db:
        todo = db.exec(select(Todo).where(Todo.id == id)).one_or_none()
        if not todo:
            print(f"Todo does not exist for id: {id}")
            return
        else:
            db.delete(todo)
        
        db.commit()
        

@cli.command()
def complete_all_todos(username:str):
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User doesn't exist")
            return
        todos =  db.exec(select(Todo).where(Todo.user_id == user.id)).all()

        for todo in todos:
            if not todo.done:
                todo.toggle()
                db.add(todo)
            else:
                continue
        
        db.commit()
        print("All todos completed")


if __name__ == "__main__":
    cli()