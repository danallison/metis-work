from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# secrets.py contains credentials, etc.
import secrets

def with_remote_sql_session(function):
    # Hat tip: https://stackoverflow.com/a/38001815
    with SSHTunnelForwarder(
            (secrets.server_ip_address, 22),
            ssh_username=secrets.ssh_username,
            ssh_pkey=secrets.ssh_private_key_path,
            ssh_private_key_password=secrets.ssh_private_key_password,
            remote_bind_address=('127.0.0.1', 5433)
        ) as tunnel:

        tunnel.start()

        engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=secrets.pg_user,
            password=secrets.pg_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            db=secrets.pg_user
        ))

        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return function(session)
        finally:
            session.close()
