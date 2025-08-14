# services/slack_service.py

def create_scp_onboarding_modal() -> dict:
    """
    Creates the Block Kit JSON for the SCP Onboarding Modal.
    """
    modal_view = {
        "type": "modal",
        # This ID is crucial for identifying submission events
        "callback_id": "scp_modal_submission",
        "title": {"type": "plain_text", "text": "Sales-OS Setup"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Welcome! Please provide the initial context for your subsidiary."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "offer_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "offer_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Primary Offer"
                }
            },
            {
                "type": "input",
                "block_id": "price_band_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "price_band_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "e.g., $25k-$150k"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Typical Price Band"
                }
            },
            {
                "type": "input",
                "block_id": "icp_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "icp_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "e.g., Construction QS in UAE"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Ideal Customer Profile (ICP)"
                }
            }
        ]
    }
    return modal_view