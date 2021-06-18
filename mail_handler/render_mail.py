#!/usr/bin/env python
import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List

import click
from jinja2 import Template


def load_template(tmpl_path: Path) -> Template:
    with open(tmpl_path, "r", encoding="utf-8") as input_tmpl:
        return Template(input_tmpl.read())


def render_all_content(
    template: Template,
    common_data: Dict[str, str],
    unique_data: List[Dict[str, str]],
    separator: str,
) -> Dict[str, str]:
    recv_to_mail = dict()
    mail_defdict = defaultdict(int)  # type: DefaultDict[str, int]
    for data in unique_data:
        data.update(common_data)
        if separator:
            subject = separator.join([data["receiver_email"], data["receiver_name"]])
        else:
            subject = data["receiver_email"]
        mail_defdict[subject] += 1
        # multi-mail
        if mail_defdict[subject] > 1:
            subject = "{}__{:03n}".format(subject, mail_defdict[subject])

        recv_to_mail[subject] = template.render(**data)
    return recv_to_mail


def export_mails(recv_to_mail, output_path):
    for mail, mail_content in recv_to_mail.items():
        with open(output_path / Path(mail), "w", encoding="utf-8") as output_file:
            output_file.write(mail_content)


@click.command()
@click.argument("template_path", type=click.Path(exists=True))
@click.argument("receiver_data", type=click.Path(exists=True))
@click.option(
    "--separator",
    default="",
    show_default=False,
    help="Separator used for subject suffix. It is disabled with empty string by default.",
)
@click.option(
    "--output_path",
    type=click.Path(exists=False),
    default="mails_to_sent",
    show_default=True,
    help="Output path of rendered mails",
)
def main(template_path, receiver_data, separator, output_path):
    """
    Application entry point
    """
    if not os.path.isdir(output_path):
        logging.info('Create directory "%s"', output_path)
        Path(output_path).mkdir(parents=True)

    with open(receiver_data, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)
        common_data = data["common_data"]
        unique_data = data["unique_data"]

    template = load_template(template_path)
    recv_to_mail = render_all_content(template, common_data, unique_data, separator)
    export_mails(recv_to_mail, output_path)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
# pylint: enable=no-value-for-parameter
