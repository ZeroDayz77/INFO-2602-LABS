from typing import Annotated
import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User
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


if __name__ == "__main__":
    cli()