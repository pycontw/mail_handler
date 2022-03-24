#!/usr/bin/env python
import json
import logging
import os
import pickle
import smtplib
from collections import defaultdict
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional

import click
from typing_extensions import TypedDict


class MailConfig(TypedDict):
    host: str
    port: int


MAIL_SERVER_CONFIG: Dict[str, MailConfig] = {
    "gmail": {"host": "smtp.gmail.com", "port": 465}
}


logging.basicConfig(level=logging.INFO)


def load_mails(input_dir: str) -> DefaultDict[str, List[str]]:
    addr_to_content = defaultdict(list)
    for filename in os.listdir(input_dir):
        with open(f"{input_dir}/{filename}", "r", encoding="utf-8") as input_file:
            if "@" not in filename:
                continue

            # remove "__" at multiple mails with same address
            filenames = filename.split("__")
            if len(filenames) > 1:
                filename = "".join(filenames[:-1])
            else:
                filename = filenames[0]

            addr_to_content[filename].append(input_file.read())
    return addr_to_content


def build_mail(
    receiver_addr: str,
    mail_content: str,
    config: Dict[str, str],
    separator: str,
    attachment_file: Optional[str] = None,
    suffix: str = None,
) -> MIMEMultipart:
    mail = MIMEMultipart()
    mail.attach(MIMEText(mail_content))
    if suffix:
        mail["Subject"] = "".join([config.get("Subject", ""), separator, suffix])
    else:
        mail["Subject"] = config.get("Subject", "")
    mail["From"] = formataddr((config.get("SenderName", ""), config.get("From", "")))
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


def send_mail(
    mail: MIMEMultipart,
    user: str,
    password: str,
    server_config: MailConfig = None,
) -> None:
    if not server_config:
        server_config = MAIL_SERVER_CONFIG["gmail"]

    server = smtplib.SMTP_SSL(server_config["host"], int(server_config["port"]))
    server.ehlo()
    server.login(user, password)
    server.send_message(mail)
    logging.info("Email sent to %s!", mail["To"])
    server.quit()


def dump_mail(
    mail: MIMEMultipart,
    suffix: Optional[str],
    debug_dump_path: str = "/tmp/mail_handler",
) -> None:
    if suffix:
        dump_path = "/".join((debug_dump_path, "with-separator"))
    else:
        dump_path = "/".join((debug_dump_path, "no-separator"))
    Path(dump_path).mkdir(parents=True, exist_ok=True)
    with open(f"{dump_path}/{mail['To']}", "wb") as dumpf:
        pickle.dump(mail, dumpf)
    print(f"Debug mode is on. Dump mails to {dump_path} instead of sending them.")


@click.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--mails_path",
    type=click.Path(exists=False),
    default="mails_to_sent",
    show_default=True,
)
@click.option("--debug", is_flag=True)
@click.option(
    "--separator",
    default=" - ",
    show_default=True,
    help="Separator used for subject suffix",
)
@click.option("--attachment_file", type=click.Path(exists=False))
def main(
    mails_path: str,
    config_path: str,
    debug: bool,
    separator: str,
    attachment_file: Optional[str] = None,
) -> None:
    if click.confirm(
        f'You are about to send the mails under "{mails_path}". Do you want to continue?',
        abort=True,
    ):

        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)

        smtp: MailConfig = MAIL_SERVER_CONFIG["gmail"]
        if not config.get("SMTP"):
            print(f'{"Using default Gmail SMTP server..."}')
        else:
            print(
                f'Using configured SMTP server "{config.get("SMTP").get("Host")}:{config.get("SMTP").get("Port")}"...'
            )
            smtp = {
                "host": config.get("SMTP").get("Host"),
                "port": config.get("SMTP").get("Port"),
            }

        user = click.prompt("Please enter your mail account", type=str)
        password = click.prompt(
            "Please enter you mail password", type=str, hide_input=True
        )

        # now address_suffix id defaultdict with values of list
        address_suffix_to_content = load_mails(mails_path)

        for mail_addr_suffix, mails_content in address_suffix_to_content.items():
            for mail_content in mails_content:
                mail_addr, *mail_suffix_and_more = mail_addr_suffix.split(
                    separator, maxsplit=1
                )
                mail_suffix = mail_suffix_and_more[0] if mail_suffix_and_more else None
                mail = build_mail(
                    mail_addr,
                    mail_content,
                    config,
                    separator,
                    attachment_file=attachment_file,
                    suffix=mail_suffix,
                )

                if debug:
                    dump_mail(mail, mail_suffix)
                else:
                    send_mail(mail, user, password, smtp)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
# pylint: enable=no-value-for-parameter
