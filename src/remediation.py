import logging

logger = logging.getLogger(__name__)

def diagnose_logs(logs):
    """Analyzes logs to determine the failure reason and proposed fix."""
    if not logs:
        return "Unknown", "No logs available"

    logs_lower = logs.lower()
    
    if "outofmemoryerror" in logs_lower or "oom" in logs_lower or "java.lang.outofmemoryerror" in logs_lower:
        return "OutOfMemoryError Detected", "Increase memory limit by 256Mi"
    
    if "connection refused" in logs_lower:
        return "Database Connection Refused", "Restart pod / Check DB status"
    
    if "timeout" in logs_lower:
        return "Service Timeout", "Scale up dependencies or restart pod"
    
    return "Unknown Application Crash", "Delete pod to force reschedule"

