import filecmp
import glob
import os
import pytest

from click.testing import CliRunner
from render_mail import main


path_j2 = '../templates/sponsorship/spam_sponsors_2020.j2'
path_receivers_json = '../examples/sponsorship/spam_sponsors_2020.json'
path_mails_to_send_no_separator = '/tmp/mails_to_send/no-separator'
path_mails_to_send_with_separator = '/tmp/mails_to_send/with-separator'
path_pre_rendered_mails_no_separator = './data/no-separator'
path_pre_rendered_mails_with_separator = './data/with-separator'


@pytest.fixture
def all_mails_base_no_separator():
    return get_all_mail_names_from_path(glob.glob('/'.join((path_pre_rendered_mails_no_separator, '*@*'))))


@pytest.fixture
def all_mails_base_with_separator():
    return get_all_mail_names_from_path(glob.glob('/'.join((path_pre_rendered_mails_with_separator, '*@*'))))


def get_all_mail_names_from_path(mails):
    all_mail_names = []
    for mail in mails:
        all_mail_names.append(os.path.basename(mail))

    return all_mail_names


def compare_rendered_mail_all(targets, base_prefix='./data', target_prefix='../examples'):
    for mail_name in targets:
        if not compare_rendered_mail('/'.join((base_prefix, mail_name)), '/'.join((target_prefix, mail_name))):
            return False

    return True


def compare_rendered_mail(base, target):
    return filecmp.cmp(base, target, shallow=False)


def test_rendered_mail_no_separator(all_mails_base_no_separator):
    runner = CliRunner()
    result = runner.invoke(main, [path_j2, path_receivers_json, '--output_path', path_mails_to_send_no_separator])

    all_mails_target = get_all_mail_names_from_path(glob.glob('/'.join((path_mails_to_send_no_separator, '*@*'))))

    assert result.exit_code == 0
    assert len(all_mails_base_no_separator) == len(all_mails_target)
    assert compare_rendered_mail_all(all_mails_target,
                                     base_prefix=path_pre_rendered_mails_no_separator,
                                     target_prefix=path_mails_to_send_no_separator)


def test_rendered_mail_with_separator_dash(all_mails_base_with_separator):
    runner = CliRunner()
    result = runner.invoke(main, [path_j2, path_receivers_json,
                                  '--output_path', path_mails_to_send_with_separator,
                                  '--separator', ' - '])

    all_mails_target = get_all_mail_names_from_path(glob.glob('/'.join((path_mails_to_send_with_separator, '*@*'))))

    assert result.exit_code == 0
    assert len(all_mails_base_with_separator) == len(all_mails_target)
    assert compare_rendered_mail_all(all_mails_target,
                                     base_prefix=path_pre_rendered_mails_with_separator,
                                     target_prefix=path_mails_to_send_with_separator)
