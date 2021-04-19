#!/usr/bin/env python
import json
import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

import click

MAIL_SERVER_CONFIG = {"gmail": {"host": "smtp.gmail.com", "port": 465}}


logging.basicConfig(level=logging.INFO)


def load_mails(input_dir) -> Dict[str, str]:
    addr_to_content = dict()
    for filename in os.listdir(input_dir):
        with open(f"{input_dir}/{filename}", "r") as input_file:
            if "@" not in filename:
                continue
            addr_to_content[filename] = input_file.read()
    return addr_to_content


def build_mail(
    receiver_addr: str,
    mail_content: str,
    config: Dict[str, str],
    attachment_file: str = None,
    suffix: str = None,
) -> MIMEMultipart:
    mail = MIMEMultipart()
    mail.attach(MIMEText(mail_content))
    if suffix:
        mail['Subject'] = ''.join([config.get('Subject', ''), ' - ', suffix])
    else:
        mail['Subject'] = config.get('Subject', '')
    mail["From"] = config.get("From", "")
    mail["To"] = receiver_addr
    mail["CC"] = config.get("CC", "")

    if attachment_file:
        with open(attachment_file, "rb") as f:
            attach = MIMEApplication(f.read())
        attach.add_header(
            "Content-Disposition",
            "attachment",
            filename=str(os.path.basename(attachment_file)),
        )
        mail.attach(attach)

    return mail


def send_mail(mail, user, password, server_config=None):
    if not server_config:
        server_config = MAIL_SERVER_CONFIG["gmail"]

    server = smtplib.SMTP_SSL(server_config["host"], int(server_config["port"]))
    server.ehlo()
    server.login(user, password)
    server.send_message(mail)
    logging.info("Email sent to %s!", mail["To"])
    server.quit()


@click.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--mails_path",
    type=click.Path(exists=False),
    default="mails_to_sent",
    show_default=True,
)
@click.option("--attachment_file", type=click.Path(exists=False))
def main(mails_path, config_path, attachment_file=None):
    if click.confirm(
        f'You are about to send the mails under "{mails_path}". Do you want to continue?',
        abort=True,
    ):
        user = click.prompt("Please enter your mail account", type=str)
        password = click.prompt(
            "Please enter you mail password", type=str, hide_input=True
        )
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        address_suffix_to_content = load_mails(mails_path)
        for mail_addr_suffix, mail_content in address_suffix_to_content.items():
            try:
                seperator = ' - '
                mail_addr_suffix_list = mail_addr_suffix.split(seperator)
                mail_addr = mail_addr_suffix_list[0]
                mail_suffix = mail_addr_suffix_list[1]
            except IndexError:
                mail_suffix = ''

            mail = build_mail(mail_addr, mail_content, config, attachment_file, suffix=mail_suffix)
            send_mail(mail, user, password)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
# pylint: enable=no-value-for-parameter
