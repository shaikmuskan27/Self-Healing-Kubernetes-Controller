from kubernetes import client, config
import logging

logger = logging.getLogger(__name__)

# Load in-cluster or local kubeconfig
try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def get_pod_logs(name, namespace, lines=50):
    """Fetches the last N lines of logs from a pod."""
    try:
        logs = v1.read_namespaced_pod_log(
            name=name,
            namespace=namespace,
            tail_lines=lines,
            _preload_content=False # To handle large logs safely if needed
        )
        return logs.read().decode('utf-8')
    except client.rest.ApiException as e:
        logger.error(f"Error fetching logs for {name}: {e}")
        return None

def delete_pod(name, namespace):
    """Deletes a pod to force a reschedule."""
    try:
        v1.delete_namespaced_pod(name, namespace)
        logger.info(f"Deleted pod {name} in {namespace}")
        return True
    except client.rest.ApiException as e:
        logger.error(f"Error deleting pod {name}: {e}")
        return False
