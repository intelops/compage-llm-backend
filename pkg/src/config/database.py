from pkg.src.config.env_config import settings
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra import Unauthorized



settings = settings()

BASE_DIR = settings.BASE_DIR
SOURCE_DIR = BASE_DIR / "connect_bundle"
ASTRADB_CONNECT_BUNDLE = BASE_DIR / SOURCE_DIR / "secure-connect-compage.zip"


def get_session():
    cloud_config = {"secure_connect_bundle": ASTRADB_CONNECT_BUNDLE}
    auth_provider = PlainTextAuthProvider(
        settings.ASTRADB_CLIENT_ID, settings.ASTRADB_CLIENT_SECRET
    )
    try:
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()
        connection.register_connection(str(session), session=session)
        connection.set_default_connection(str(session))
        return session
    except Unauthorized as auth_error:
        # Handle authorization error here (e.g., log, raise custom exception)
        print(f"Authorization Error: {auth_error}")
        raise  # Optionally, re-raise the exception for higher-level handling
    except Exception as e:
        # Handle other exceptions (e.g., connection errors)
        print(f"Error: {e}")
        raise  # Optionally, re-raise the exception for higher-level handling

