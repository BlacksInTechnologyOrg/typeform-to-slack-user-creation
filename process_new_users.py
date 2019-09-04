import requests
import time
import os
import sys
import logging

from logging.handlers import TimedRotatingFileHandler
from config import config


"""
TODO

- Switch Slack to OAuth (09/03/2019 Seems maybe switching to Oauth might not work since client scope is not available for
Oauth Tokens. Client scope permission is needed for user.admin.invite Slack api call)
- Remove processed email file logic and create logic to delete Typeform entry after a user is added.

"""


LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "logs"))
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

EMAIL_LIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "private", "processed_email_addresses.txt")
)

# Setting up logging
log = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

fh = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, "bot.log"), when="h", interval=1, backupCount=6
)
fh.setFormatter(formatter)
log.addHandler(fh)

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
log.addHandler(sh)


class TypeFormToSlack:
    def __init__(self, config_name):
        self.config = config[config_name]
        self.processed_email_addresses = self.get_processed_email_addresses()
        self.new_email_addresses = []

        log.setLevel(self.config.LOG_LEVEL)
    def run(self):
        try:
            log.info("Starting script...")
            data = self.getNewSignUps()
            for new_sub in data["items"]:
                email_address = ""
                first_name = ""
                last_name = ""
                if "answers" in new_sub:
                    for answer in new_sub["answers"]:
                        if answer["type"] == "email":
                            email_address = answer["email"]
                            log.debug("email: {}".format(email_address))
                        if answer["field"]["id"] == self.config.TYPEFORM_FIRST_NAME_ID:
                            first_name = answer["text"]
                            log.debug("First Name: {}".format(first_name))
                        if answer["field"]["id"] == self.config.TYPEFORM_LAST_NAME_ID:
                            last_name = answer["text"]
                            log.debug("Last Name: {}".format(last_name))
                self.inviteToSlack(email_address, first_name, last_name)
                time.sleep(1)
            self.writeToEmailFile(self.new_email_addresses)
            log.info("Finished")
        except Exception:
            log.exception("Error in main")

    def get_processed_email_addresses(self):
        try:
            f = open(EMAIL_LIST, "r")
            return f.read().splitlines()
        except:
            return []

    def validateTypeFormResponse(self, resp):
        """
        First check to see if there are any TypeForm entries then check to see if First Name and Last Name field IDs did not change.
        Using Field ID because Typefrom does not store the names of its fields.
        """
        try:
            if resp["items"]:
                pass
            else:
                log.info("There aren't any new sign ups, exiting...")
                exit()
            assert any(
                answer["field"]["id"] == self.config.TYPEFORM_FIRST_NAME_ID
                for answer in resp["items"][0]["answers"]
            ), "TypeForm First Name Field ID changed, please verify Field ID from Typeform response"
            assert any(
                answer["field"]["id"] == self.config.TYPEFORM_LAST_NAME_ID
                for answer in resp["items"][0]["answers"]
            ), "TypeForm Last Name Field ID changed, please verify Field ID from Typeform response"
        except Exception:
            log.exception("Error validating Typeform response")
            exit(1)

    def getNewSignUps(self):
        try:
            log.debug(f"Typeform API Key: {self.config.TYPEFORM_API_KEY}")
            log.debug(f"Typeform UID: {self.config.TYPEFORM_UID}")
            typeform_url = "https://api.typeform.com/forms/{typeform_uid}/responses".format(
                typeform_uid=self.config.TYPEFORM_UID
            )
            headers = {"Authorization": f"Bearer {self.config.TYPEFORM_API_KEY}"}
            resp = requests.get(typeform_url, headers=headers)
            if resp.status_code != 200:
                raise Exception(resp.json())
            else:
                self.validateTypeFormResponse(resp.json())
                return resp.json()
        except Exception:
            log.exception("Error while retrieving Typeform data")
            exit(1)

    def inviteToSlack(self, email_address, first_name, last_name):
        try:
            slack_invite_url = "https://{workspacename}.slack.com/api/users.admin.invite?t={timenow}".format(
                workspacename=self.config.SLACK_HOST_NAME, timenow=str(int(time.time()))
            )
            if email_address and email_address not in self.processed_email_addresses:
                payload = {
                    "email": email_address,
                    "first_name": first_name,
                    "last_name": last_name,
                    "token": self.config.SLACK_API_KEY,
                    "set_active": "true",
                    "_attempts": 1,
                }
                response = requests.post(slack_invite_url, data=payload)
                log.debug(response.text)
                slackresp = response.json()
                # (Herman) Left in check against processed emails, need to verify if Typeform entries will be deleted
                if slackresp["ok"]:
                    log.info("New email invited to Slack " + email_address)
                    self.new_email_addresses.append(email_address)
                elif (
                    slackresp["error"] == "already_in_team_invited_user"
                    or slackresp["error"] == "already_in_team"
                    or slackresp["error"] == "'already_invited"
                ):
                    log.info(f"{email_address} already processed, adding to file")
                    self.new_email_addresses.append(email_address)
                else:
                    log.error(
                        "Email not added: {email} {response}".format(
                            email=email_address, response=slackresp
                        )
                    )

        except Exception:
            log.exception("Error while inviting email to Slack - " + email_address)

    def writeToEmailFile(self, new_email_addresses):
        try:
            if new_email_addresses:
                f = open(EMAIL_LIST, "a")
                for email_address in new_email_addresses:
                    log.info("New email written to email file " + email_address)
                    f.write(email_address + "\n")
        except Exception:
            log.exception("Error writing emails to file - " + new_email_addresses)
