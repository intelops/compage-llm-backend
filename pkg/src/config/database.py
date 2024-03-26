""" Module providing a function returning a cassandra session. """

from cassandra.cluster import Cluster  # pylint: disable = no-name-in-module
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.cqlengine.connection import register_connection, set_default_connection

KEYSPACE = "backend_llm"


def get_session():
    """
    A function to get the cluster and establish a session to a specific keyspace.
    """
    cluster = Cluster(
        ["127.0.0.1"],
        port=9042,
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc="datacenter1"),
        protocol_version=4,
    )
    session = cluster.connect(keyspace=KEYSPACE, wait_for_all_pools=True)
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


def get_keyspace() -> str:
    """
    A function to get the cluster and establish a session to a specific keyspace.
    """
    return KEYSPACE
