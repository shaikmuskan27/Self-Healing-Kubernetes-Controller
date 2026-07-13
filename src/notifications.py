import os
import requests
import logging

logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_notification(app_name, diagnostic_reason, proposed_fix, pr_url=None):
    """Sends an interactive Block Kit message to Slack."""
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not configured. Skipping notification.")
        return

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 Self-Healing Controller: Incident Detected"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Application:* {app_name}\n*Diagnostics:* {diagnostic_reason}\n*Proposed Fix:* {proposed_fix}"
            }
        }
    ]

    if pr_url:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"🔀 *Action Taken:* Created PR for review: {pr_url}"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Review PR"
                },
                "url": pr_url,
                "action_id": "button-action"
            }
        })

    payload = {"blocks": blocks}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logger.info(f"Notification sent to Slack for {app_name}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Slack notification: {e}")
