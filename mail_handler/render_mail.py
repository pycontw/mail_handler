#!/usr/bin/env python
import csv
import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Sequence

import click
from jinja2 import Template


def load_template(tmpl_path: str) -> Template:
    with open(tmpl_path, "r", encoding="utf-8") as input_tmpl:
        return Template(input_tmpl.read())


def render_all_content(
    template: Template,
    common_data: Dict[str, str],
    unique_data: Sequence[Dict[str, str]],
    separator: str,
) -> Dict[str, str]:
    addr_to_content: Dict[str, str] = dict()
    mail_defdict: DefaultDict[str, int] = defaultdict(int)
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

        addr_to_content[subject] = template.render(**data)
    return addr_to_content


def export_mails(recv_to_mail: Dict[str, str], output_path: str) -> None:
    for receiver_mail, mail_content in recv_to_mail.items():
        with open(
            output_path / Path(receiver_mail), "w", encoding="utf-8"
        ) as output_file:
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
@click.option(
    "--unique_csv",
    type=click.Path(exists=True),
    help="Use CSV file to import unique data",
)
def main(
    template_path: str,
    receiver_data: str,
    separator: str,
    output_path: str,
    unique_csv: str,
) -> None:
    """
    Application entry point
    """
    if not os.path.isdir(output_path):
        logging.info('Create directory "%s"', output_path)
        Path(output_path).mkdir(parents=True)

    if unique_csv:
        with open(receiver_data, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
            common_data = data["common_data"]

        with open(unique_csv, "r", encoding="utf-8-sig") as input_file:
            unique_data = [row for row in csv.DictReader(input_file)]
    else:
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
