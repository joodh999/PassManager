# Python 3.8.6

import click
from pysqlcipher3 import dbapi2 as sqlite
from clint.textui import colored, puts, indent
import pyperclip

conn = sqlite.connect('notpass.db')
c = conn.cursor()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def SetMaster(password):
    c.execute(f"PRAGMA key='{password}'")
    c.execute("CREATE TABLE pass(id TEXT, pass TEXT)")
    conn.commit()
    c.close()

@cli.command()
@click.argument('id')
@click.argument("password")
@click.option('--mpassword', prompt=True, hide_input=True)
def Insert(id, password, mpassword):
    try:
        c.execute(f"PRAGMA key='{mpassword}'")
        c.execute(f'INSERT INTO pass VALUES ("{id}","{password}")')
        conn.commit()
        c.close()
    except:
        puts(colored.red("Password is incorrect"))


@cli.command()
@click.argument('id')
@click.option('--mpassword', prompt=True, hide_input=True)
def getpassfor(id, mpassword):
    try:
        c.execute(f"PRAGMA key='{mpassword}'")
        Get = c.execute(f"SELECT pass FROM pass WHERE id='{id}'").fetchall()
        pyperclip.copy(Get[0][0])
        puts(colored.red("Password was copied to clipboard"))
        c.close()
    except:
        puts(colored.red("Password is incorrect"))


@cli.command()
@click.option('--mpassword', prompt=True, hide_input=True)
def allid(mpassword):
    try:
        c.execute(f"PRAGMA key='{mpassword}'")
        all=c.execute(f"SELECT id FROM pass").fetchall()
        for i in all:
            with indent(2, quote='~'):
                puts(colored.green(i[0]))
            c.close()
    except:
        puts(colored.red("Password is incorrect"))





if __name__ == "__main__":
    cli()
