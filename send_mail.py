#!/usr/bin/env python
import os
import logging
import smtplib
import json
from email.mime.text import MIMEText
from typing import Dict

import click


MAIL_SERVER_CONFIG = {
    'gmail': {'host': 'smtp.gmail.com', 'port': 465}
}


logging.basicConfig(level=logging.INFO)


def load_mails(input_dir) -> Dict[str, str]:
    addr_to_content = dict()
    for filename in os.listdir(input_dir):
        with open(f'{input_dir}/{filename}', 'r') as input_file:
            if '@' not in filename:
                continue
            addr_to_content[filename] = input_file.read()
    return addr_to_content


def build_mail(receiver_addr: str, mail_content: str, config: Dict[str, str]) -> MIMEText:
    mail = MIMEText(mail_content)
    mail['Subject'] = config.get('Subject', '')
    mail['From'] = config.get('From', '')
    mail['To'] = receiver_addr
    mail['CC'] = config.get('CC', '')
    return mail


def send_mail(mail, user, password, server_config=None):
    if not server_config:
        server_config = MAIL_SERVER_CONFIG['gmail']

    server = smtplib.SMTP_SSL(server_config['host'], int(server_config['port']))
    server.ehlo()
    server.login(user, password)
    server.send_message(mail)
    logging.info('Email sent to %s!', mail['To'])
    server.quit()


@click.command()
@click.argument('config_path', type=click.Path(exists=True))
@click.option('--mails_path', type=click.Path(exists=False), default='mails_to_sent', show_default=True)
def main(mails_path, config_path):
    if click.confirm(f'You are about to send the mails under "{mails_path}". Do you want to continue?', abort=True):
        user = click.prompt('Please enter your mail account', type=str)
        password = click.prompt('Please enter you mail password', type=str, hide_input=True)
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        addr_to_content = load_mails(mails_path)
        for mail_addr, mail_content in addr_to_content.items():
            mail = build_mail(mail_addr, mail_content, config)
            send_mail(mail, user, password)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
# pylint: enable=no-value-for-parameter
