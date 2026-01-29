import logging

import asyncio
import aiohttp

from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = None


async def fetch_html_content(url):
    global session
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DWK-Dummy-CRD/1.0;)"
    }
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                content = await response.text()
                return content
            else:
                logger.error(
                    f"{response.status} Failed to get {url}."
                )
                return None
    except Exception as e:
        logger.error(f"Exception while getting {url}: {str(e)}")
        return None


def create_configmap(name, namespace, html_content):
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": f"{name}-html-content",
            "namespace": namespace,
        },
        "data": {"index.html": html_content},
    }
    return configmap


def create_deployment(name, namespace):
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"{name}-dummysite-deployment",
            "namespace": namespace,
        },
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": f"{name}-dummysite"}},
            "template": {
                "metadata": {"labels": {"app": f"{name}-dummysite"}},
                "spec": {
                    "containers": [
                        {
                            "name": "nginx",
                            "image": "nginx:alpine",
                            "ports": [{"containerPort": 80}],
                            "volumeMounts": [
                                {
                                    "name": "html-content",
                                    "mountPath": "/usr/share/nginx/html",
                                }
                            ],
                        }
                    ],
                    "volumes": [
                        {
                            "name": "html-content",
                            "configMap": {"name": f"{name}-html-content"},
                        }
                    ],
                },
            },
        },
    }
    return deployment


def create_service(name, namespace):
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"{name}-dummysite-service",
            "namespace": namespace,
        },
        "spec": {
            "selector": {"app": f"{name}-dummysite"},
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": 80}],
            "type": "ClusterIP",
        },
    }
    return service


async def handle_dummysite_creation(
    api_instance, apps_v1_api_instance, custom_api_instance, dummysite
):
    metadata = dummysite["metadata"]
    spec = dummysite["spec"]

    name = metadata["name"]
    namespace = metadata["namespace"]
    website_url = spec["website_url"]

    logger.info(
        f"Processing DummySite creation: {name} in namespace {namespace} with URL: {website_url}"
    )

    html_content = await fetch_html_content(website_url)
    if not html_content:
        logger.error(f"Could not fetch HTML content for {name}, skipping...")
        return

    configmap = create_configmap(name, namespace, html_content)
    try:
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: api_instance.create_namespaced_config_map(namespace, configmap),
        )
        logger.info(f"ConfigMap {configmap['metadata']['name']} created successfully")
    except ApiException as e:
        if e.status == 409:
            logger.warning(
                f"ConfigMap {configmap['metadata']['name']} already exists, updating..."
            )
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: api_instance.patch_namespaced_config_map(
                    configmap["metadata"]["name"], namespace, configmap
                ),
            )
        else:
            logger.error(f"Exception when creating ConfigMap: {e}")
            return

    deployment = create_deployment(name, namespace)
    try:
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: apps_v1_api_instance.create_namespaced_deployment(
                namespace, deployment
            ),
        )
        logger.info(f"Deployment {deployment['metadata']['name']} created successfully")
    except ApiException as e:
        if e.status != 409:
            logger.error(f"Exception when creating Deployment: {e}")
        else:
            logger.warning(
                f"Deployment {deployment['metadata']['name']} already exists"
            )

    service = create_service(name, namespace)
    try:
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: api_instance.create_namespaced_service(namespace, service)
        )
        logger.info(f"Service {service['metadata']['name']} created successfully")
    except ApiException as e:
        if e.status != 409:
            logger.error(f"Exception when creating Service: {e}")
        else:
            logger.warning(f"Service {service['metadata']['name']} already exists")


async def watch_dummysites():
    global session

    try:
        config.load_incluster_config()
        logger.info("Loaded in-cluster configuration")
    except:
        config.load_kube_config()
        logger.info("Loaded kube config from local machine")

    api_instance = client.CoreV1Api()
    apps_v1_api_instance = client.AppsV1Api()
    custom_api_instance = client.CustomObjectsApi()

    connector = aiohttp.TCPConnector(limit=10)
    session = aiohttp.ClientSession(connector=connector)

    group = "stable.dwk"
    version = "v1"
    plural = "dummiesites"

    w = watch.Watch()

    try:
        logger.info("Starting to watch DummySite resources...")

        for event in w.stream(
            custom_api_instance.list_cluster_custom_object,
            group=group,
            version=version,
            plural=plural,
            timeout_seconds=600,
        ):
            event_type = event["type"]
            dummysite = event["object"]

            logger.info(
                f"Received event: {event_type} for DummySite: {dummysite['metadata']['name']}"
            )

            if event_type == "ADDED":
                await handle_dummysite_creation(
                    api_instance, apps_v1_api_instance, custom_api_instance, dummysite
                )
            elif event_type == "MODIFIED":
                await handle_dummysite_creation(
                    api_instance, apps_v1_api_instance, custom_api_instance, dummysite
                )
            elif event_type == "DELETED":
                logger.info(f"DummySite {dummysite['metadata']['name']} was deleted")

    except Exception as e:
        logger.error(f"Exception in watch loop: {str(e)}")
    finally:
        await session.close()


async def main():
    logger.info("Starting DummySite Controller")
    await watch_dummysites()


if __name__ == "__main__":
    asyncio.run(main())
