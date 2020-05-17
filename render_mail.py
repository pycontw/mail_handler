#!/usr/bin/env python
import json
import os
import logging
from pathlib import Path
from typing import Dict, List

import click
from jinja2 import Template


def load_template(tmpl_path: Path) -> Template:
    with open(tmpl_path, 'r') as input_tmpl:
        return Template(input_tmpl.read())


def render_all_content(template: Template,
                       common_data: Dict[str, str],
                       unique_data: List[Dict[str, str]]) -> Dict[str, str]:
    recv_to_mail = dict()
    for data in unique_data:
        data.update(common_data)
        recv_to_mail[data['receiver_email']] = template.render(**data)
    return recv_to_mail


def export_mails(recv_to_mail, output_path):
    for mail, mail_content in recv_to_mail.items():
        with open(output_path / Path(mail), 'w') as output_file:
            output_file.write(mail_content)


@click.command()
@click.argument('template_path', type=click.Path(exists=True))
@click.argument('receiver_data', type=click.Path(exists=True))
@click.option('--output_path', type=click.Path(exists=False), default='mails_to_sent', show_default=True)
def main(template_path, receiver_data, output_path):
    if not os.path.isdir(output_path):
        logging.info('Create directory "%s"', output_path)
        os.mkdir(output_path)

    with open(receiver_data, 'r') as input_file:
        data = json.load(input_file)
        common_data = data['common_data']
        unique_data = data['unique_data']

    template = load_template(template_path)
    recv_to_mail = render_all_content(template, common_data, unique_data)
    export_mails(recv_to_mail, output_path)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
# pylint: enable=no-value-for-parameter
