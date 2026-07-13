import kopf
import logging
from .k8s_client import get_pod_logs, delete_pod
from .remediation import diagnose_logs
from .github_integration import create_remediation_pr
from .notifications import send_slack_notification

logger = logging.getLogger(__name__)

# We track processed pods to avoid loop storms
PROCESSED_PODS = set()

@kopf.on.event('', 'v1', 'pods', annotations={'self-healing': 'enabled'})
def handle_pod_events(event, **kwargs):
    """
    Watches for Pod events. Specifically looks for Pods in a failed state
    or CrashLoopBackOff that have the annotation `self-healing: enabled`.
    """
    pod = event.get('object', {})
    name = pod.get('metadata', {}).get('name')
    namespace = pod.get('metadata', {}).get('namespace')
    uid = pod.get('metadata', {}).get('uid')
    status = pod.get('status', {})
    phase = status.get('phase')

    if not name or not namespace:
        return

    # Check for container statuses
    container_statuses = status.get('containerStatuses', [])
    is_failing = False
    
    for c_status in container_statuses:
        state = c_status.get('state', {})
        waiting = state.get('waiting', {})
        terminated = state.get('terminated', {})
        
        # Identify CrashLoopBackOff or Error states
        if waiting.get('reason') == 'CrashLoopBackOff' or terminated.get('reason') == 'Error':
            is_failing = True
            break
            
    # We also check for OOMKilled specifically in terminated state
    if phase == 'Failed':
        is_failing = True

    if is_failing and uid not in PROCESSED_PODS:
        logger.info(f"🚨 Detected failing pod: {name} in {namespace}")
        PROCESSED_PODS.add(uid)
        
        # 1. Diagnostic Phase
        logger.info(f"Fetching logs for {name}...")
        logs = get_pod_logs(name, namespace, lines=50)
        
        reason, fix = diagnose_logs(logs)
        logger.info(f"Diagnostic result: {reason} -> Proposed Fix: {fix}")
        
        # 2. Remediation Phase & GitOps Integration
        pr_url = None
        if "Increase memory" in fix:
            # Assume manifests are stored in 'manifests/deployment.yaml' in the repo
            filepath_in_repo = f"manifests/test-app.yaml" 
            pr_url = create_remediation_pr(name, reason, fix, filepath_in_repo)
        else:
            # Transient error, just delete the pod
            logger.info("Applying transient fix: Deleting pod...")
            delete_pod(name, namespace)
            
        # 3. Notification Phase
        send_slack_notification(name, reason, fix, pr_url)
