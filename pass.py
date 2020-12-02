import click
from pysqlcipher3 import dbapi2 as sqlite

conn = sqlite.connect('notpass.db')
c = conn.cursor()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def SetMaster(password):
    """Set a Master password"""
    c.execute(f"PRAGMA key='{password}'")
    c.execute("CREATE TABLE pass(id TEXT, pass TEXT)")
    conn.commit()
    c.close()

@cli.command()
@click.argument('id')
@click.argument("password")
@click.option('--mpassword', prompt=True, hide_input=True)
def Insert(id, password, mpassword):
    """insert password"""
    try:
        c.execute(f"PRAGMA key='{mpassword}'")
        c.execute(f'INSERT INTO pass VALUES ("{id}","{password}")')
        conn.commit()
        c.close()
    except:
        click.echo("Password was incorrect")


@cli.command()
@click.argument('id')
@click.option('--mpassword', prompt=True, hide_input=True)
def get(id, mpassword):
    """Get a specific password"""
    c.execute(f"PRAGMA key='{mpassword}'")
    Get = c.execute(f"SELECT pass FROM pass WHERE id='{id}'").fetchall()
    click.echo(Get)
    c.close()

@cli.command()
@click.option('--mpassword', prompt=True, hide_input=True)
def allid(mpassword):
    """Get all id's"""
    c.execute(f"PRAGMA key='{mpassword}'")
    all = c.execute(f"SELECT id FROM pass").fetchall()
    click.echo(all)
    c.close()


if __name__ == "__main__":
    cli()
