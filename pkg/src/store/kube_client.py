"""
This module provides functionality for interacting with the Kubernetes client.
It initializes the Kubernetes client using the kubernetes library and environment settings.
"""
# pkg/src/store/kube_client.py
from kubernetes import client, config
from pkg.src.config.env_config import settings
from pkg.src.constants.store import (
    compage_gpt_group,
    compage_gpt_version,
    compage_gpt_plural,
    compage_gpt_kind,
)

settings = settings()


def initialize_kube_client():
    if settings.ENVIRONMENT == "development":
        config.load_kube_config()
    else:
        config.load_incluster_config()

    return client.CustomObjectsApi()


def create_compage_gpt_resource(namespace, payload):
    kube_client = initialize_kube_client()
    resource_body = {
        "apiVersion": f"{compage_gpt_group}/{compage_gpt_version}",
        "kind": compage_gpt_kind,
        "metadata": {"namespace": namespace, "name": payload["username"]},
        "spec": payload,
    }

    try:
        return kube_client.create_namespaced_custom_object(
            compage_gpt_group,
            compage_gpt_version,
            namespace,
            compage_gpt_plural,
            resource_body,
        )
    except client.rest.ApiException as e:
        print(f"Error creating CompageGPT resource: {e}")
        return None


def get_compage_gpt_resource(namespace, username):
    kube_client = initialize_kube_client()
    try:
        resource = kube_client.get_namespaced_custom_object(
            compage_gpt_group,
            compage_gpt_version,
            namespace,
            compage_gpt_plural,
            username,
        )
        return resource
    except client.rest.ApiException as e:
        print(f"Error getting CompageGPT resource: {e}")
        return None
