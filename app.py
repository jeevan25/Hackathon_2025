import re
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import shlex
from datetime import datetime
import time
from dotenv import load_dotenv
from bitbucket_try import create_branch_with_file_changes
from sample_generated_output import sample_output, extract_files_and_contents
from Test_generator.test_generator import *
from global_store import globalStore

load_dotenv()

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
SIGNING_TOKEN = os.getenv('SLACK_SIGNING_TOKEN')

NEW_BRANCH_NAME = f'autotestgen-branch-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
FILE_CHANGES = {
    'README2.md': '# Updated by Python script\nThis is an automated update.\n'
}
ai_output_global_store = globalStore()

def get_file_changes(ai_output, module_name):
    files = extract_files_and_contents(ai_output)
    for file in files["test_files"]:
        FILE_CHANGES[f"tests/backend_tc/open_api/tests_{module_name}_api.py"] = file

    for file in files["helper_files"]:
        FILE_CHANGES[f"apiLibrary/open_api/{module_name}_api.py"] = file
    
    return FILE_CHANGES


app = App(
    token=os.getenv(SLACK_BOT_TOKEN),
    signing_secret=SIGNING_TOKEN
)

@app.message("hello")
def message_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")


@app.event("app_mention")
def handle_greet_command(body, say):
    # Acknowledge command request within 3 seconds
    user_id = body['event']['user']
    team_id = body['team_id']

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚀 Generate API Automation Testcases!",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey <@{user_id}>! Here's the latest on *Project Phoenix*:"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Status:*\n:large_green_circle: On Track"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Next Milestone:*\nBeta Release"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Due Date:*\n2025-06-15"
                }
            ]
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "Project Phoenix Logo",
                "emoji": True
            },
            "image_url": "https://api.slack.com/img/blocks/bkb_template_images/goldengate.png", # Replace with your image URL
            "alt_text": "Logo for Project Phoenix"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                    "alt_text": "warning"
                },
                {
                    "type": "mrkdwn",
                    "text": " *Reminder:* Please submit your individual progress reports by EOD."
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Full Report",
                        "emoji": True
                    },
                    "style": "primary", # "primary" or "danger"
                    "url": "https://www.example.com/report", # Link to an external URL
                    "action_id": "button_view_report" # For interactivity if you handle button clicks
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create Branch",
                        "emoji": True
                    },
                    "url": f"slack://user?team={team_id}&id={user_id}", # Opens a DM with the user
                    "action_id": "button_create_branch"
                }
            ]
        },
        {
            "type": "divider"
        }
    ]

    # The 'text' argument is a fallback for notifications and older Slack clients
    fallback_text = "Project Phoenix Update: On Track for Beta Release."
    say(text=fallback_text, blocks=blocks)
        
@app.command("/generate-testcases")
def handle_generate_testcases_command(ack, say, command):
    ack()
    user_input_text = command.get('text', '')
    user_id = command['user_id']
    team_id = command['team_id']

    if not user_input_text:
        say(f"<@{user_id}>, you need to provide some parameters! Try `/additem <item_name> [endpoint] [instructions]`")
        return

    try:
        params = shlex.split(user_input_text) 
    except ValueError:
        say(f"<@{user_id}>, there was an issue parsing your parameters. Ensure quotes are properly matched if used.")
        return

    endpoint = params[0] if len(params) > 0 else None
    module = params[1] if len(params) > 1 else None
    instructions = params[2] if len(params) > 2 else ""  
    if not endpoint:
        say(f"<@{user_id}>, please specify the CSAP endpoint you want to generate automation testcases for.")
        return

    if not module:
        say(f"<@{user_id}>, please provide which CSAP module you want to generate automation testcases for: ")
    
    say("Generating Testcases, this may take a while....")
    ai_output = generate_test_code(endpoint, instructions)
    files = extract_files_and_contents(ai_output)
    
    for file in files["test_files"]:
        say(f"```{file}```")
        
    for file in files["helper_files"]:
        say(f"```{file}```")
        
    ai_output_global_store.store_ai_output(ai_output)

    confirmation_text = f"Would you like to add them to your bitbucket repository?"
    
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": confirmation_text
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create Branch",
                        "emoji": True
                    },
                    "action_id": "button_create_branch",
                    "value" : module
                }
            ]
        }
    ]

    # The 'text' argument is a fallback for notifications and older Slack clients.
    say(text=confirmation_text, blocks=blocks)

@app.action("button_create_branch")
def handle_create_branch_button(ack, body, logger, respond):
    user_id = body['user']['id']
    original_message_text = "No original message context found."
    ack(f"Button 'button_create_branch' clicked by user <@{user_id}>")
    logger.info(f"Full body of the action: {body}")
    try:
        module = body['actions'][0]['value']
        ai_output = ai_output_global_store.get_ai_output()
        print(f"Inside Create Branch Button: {ai_output}")
        file_changes = get_file_changes(ai_output, module)
        create_branch_with_file_changes(NEW_BRANCH_NAME,file_changes)
        respond(f"Sucessfully Created a Branch in CSAP Automation Repo with name: `{NEW_BRANCH_NAME}`")
    except:
        respond(f"Was Unable to Create a Branch through bitbucket")

# Start your app
if __name__ == "__main__":
    print("🚀 Simple Bot is running with Socket Mode!")
    SocketModeHandler(app, os.getenv(SLACK_APP_TOKEN)).start()