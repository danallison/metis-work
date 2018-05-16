from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

# secrets.py contains credentials, etc.
import secrets

def get_engine_for_port(port):
    return create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=secrets.pg_user,
        password=secrets.pg_password,
        host='127.0.0.1',
        port=port,
        db=secrets.pg_user
    ))

def with_sql_session(function, args, kwargs, engine=None):
    if engine is None:
        # Default to local port
        engine = get_engine_for_port(5433)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return function(session, *args, **kwargs)
    finally:
        session.close()

def with_local_sql_session(function, *args, **kwargs):
    return with_sql_session(function, args, kwargs)

def with_remote_sql_session(function, *args, **kwargs):
    # Hat tip: https://stackoverflow.com/a/38001815
    with SSHTunnelForwarder(
            (secrets.server_ip_address, 22),
            ssh_username=secrets.ssh_username,
            ssh_pkey=secrets.ssh_private_key_path,
            ssh_private_key_password=secrets.ssh_private_key_password,
            remote_bind_address=('127.0.0.1', 5433)
        ) as tunnel:
        tunnel.start()
        engine = get_engine_for_port(tunnel.local_bind_port)
        return with_sql_session(function, args, kwargs, engine=engine)

def local_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_local_sql_session(function, *args, **kwargs)
    return wrapper

def remote_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_remote_sql_session(function, *args, **kwargs)
    return wrapper
