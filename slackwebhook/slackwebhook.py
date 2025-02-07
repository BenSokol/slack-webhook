#!/usr/local/bin/python3
# @Filename: slackwebhook.py
# @Author:   Ben Sokol
# @Email:    ben@bensokol.com
# @Created:  September 10th, 2020 [6:56pm]
#
# Copyright (C) 2020-2022 by Ben Sokol. All Rights Reserved.

import sys
if (sys.version_info < (3, 0)):
  print("Slack requires python3\n\npython3 " + ' '.join(sys.argv) + "\n")
  sys.exit(100)

import argparse
import enum
import json
import logging
import os
import pathlib
import pprint
import socket
import sys
import typing
import urllib.request

__all__ = ["send_message", "main"]

logger = logging.getLogger(__name__)
logging.addLevelName(logging.DEBUG - 1, "DEBUG")
logging.addLevelName(logging.INFO - 1, "INFO")


def logger_debug(*args, **kwargs):
  logger.log(logging.DEBUG - 1, *args, **kwargs)


def logger_info(*args, **kwargs):
  logger.log(logging.INFO - 1, *args, **kwargs)


class ReturnCode(enum.IntEnum):
  success = 0
  error = 1


class Attachments(typing.TypedDict):
  title: str
  text: str


class Data(typing.TypedDict):
  text: str
  attachments: typing.List[Attachments]


def has_internet(url="1.1.1.1", port=53, timeout=5):
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((url, port))
    return True
  except socket.error:
    return False


def send_message(webhook: pathlib.Path, markdown: bool, message: str, subtitle: str, subtext: str, noexec: bool = False, timeout: int = 10) -> ReturnCode:
  if not pathlib.Path(webhook).expanduser().exists():
    logger.error("ERROR: Unable to locate a webhook at " + str(webhook))
    logger.error("       The file should only contain the full url of the webhook")
    logger.error("       Slack Incoming WebHooks 'https://slack.com/apps/A0F7XDUAZ-incoming-webhooks'")
    return ReturnCode.error

  url = None
  logger_debug("Webhook: " + str(webhook).replace(os.path.expanduser('~'), '~'))
  with open(webhook.expanduser(), 'r') as file:
    url = file.read().replace('\n', '')
    logger_debug("Url: " + url)

  if url is None:
    logger.error("Failed to obtain url")
    return ReturnCode.error

  data: Data = {}
  if message is not None:
    logger_info("message: " + message)
    data["text"] = message.replace('\\n', '\n')
    if markdown:
      data["type"] = "mrkdwn"

  if subtitle is not None or subtext is not None:
    data["attachments"] = [{}]
    if subtitle is not None:
      logger_info("subtitle: " + subtitle)
      data["attachments"][0]["title"] = subtitle.replace('\\n', '\n')
    if subtext is not None:
      logger_info("subtext: " + subtext)
      data["attachments"][0]["text"] = subtext.replace('\\n', '\n')
    if markdown:
        data["attachments"][0]["type"] = "mrkdwn"

  data = json.dumps(data)
  logger_debug("data: " + pprint.pformat(data))
  if not noexec:
    result: typing.Union[None, str] = None
    request = None
    try:
      if not has_internet():
        logger.error("No internet...")
        return
      req = urllib.request.Request(
        url,
        data=data.encode(),
        headers={"Content-type": "application/json"},
        method="POST")
      request = urllib.request.urlopen(req, timeout=timeout)
      result = request.read().decode()
    except urllib.error.URLError:
      logger.error("URLError: Invalid webhook URL")
      result = 'error'
    finally:
      if request is not None:
        request.close()

    if result == 'ok':
      logger_info("Result: " + result)
    else:
      logger.error("Result: " + result)
      return ReturnCode.error

  return ReturnCode.success


def main() -> typing.NoReturn:
  """ Main script entry point. """
  default_slack_webhook_filename = "~/.config/slackwebhook"
  default_slack_webhook_filename_path = pathlib.Path(default_slack_webhook_filename).expanduser()

  description = '''
Sends messages to a slack webhook.
A webhook should be specified either at '{webhook}' or provided using --webhook <webhook>
See 'https://slack.com/apps/A0F7XDUAZ-incoming-webhooks' for more information.

The message consists of:
message
| subtitle (bold)
| subtext
'''.format(webhook=default_slack_webhook_filename)
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description)

  message_options = parser.add_argument_group("Message Options")
  message_options.add_argument('--message', '-m', action='store', help='The message', default=None)
  message_options.add_argument('--subtitle', action='store', help='The title of the nested message', default=None)
  message_options.add_argument('--subtext', action='store', help='The text of the nested message', default=None)
  message_options.add_argument('--markdown', action='store_true', help='Use markdown for message contents', default=False)

  configuration_options = parser.add_argument_group("Configuration options")
  configuration_options.add_argument('--webhook', action='store', type=pathlib.Path, help="The webhook to use. (Default: " + default_slack_webhook_filename + ")", default=default_slack_webhook_filename_path)

  dev_options = parser.add_argument_group(pathlib.Path(__file__).name + " developer options")
  dev_options.add_argument('--noexec', '-n', action="store_true", help="No execute. Does not send anything to the webhook.", default=False)
  dev_options.add_argument('--verbose', '-v', action="store_true", help="Prints additional information.", default=False)

  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(level=logging.DEBUG - 1, format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
  else:
    logging.basicConfig(level=logging.INFO - 1, format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

  if args.message is None and args.subtitle is None and args.subtext is None:
    parser.error("At least 1 message option is required.")
    logging.shutdown()
    parser.exit(ReturnCode.error)

  ret_code = send_message(webhook=args.webhook, markdown=args.markdown, message=args.message, subtitle=args.subtitle, subtext=args.subtext, noexec=args.noexec)
  logging.shutdown()
  sys.exit(ret_code)


# Run the script
if __name__ == '__main__':
  try:
    main()
  except SystemExit:
    # SystemExit exception gets thrown on sys.exit() calls.
    # This has the exit code in the exception info.
    sys.exit(sys.exc_info()[1])
  except KeyboardInterrupt:
    # Dont print exception info for KeyboardInterrupt exceptions (CTRL + C)
    # Keyboard interrputs default to a return value of 130, so return that.
    sys.exit(130)
