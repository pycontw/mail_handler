import pickle
import glob
import json
import os
import pytest

from click.testing import CliRunner
from send_mail import main


path_mail_config = "./examples/sponsorship/spam_sponsors_2020_mail_config.json"
path_receivers = "./examples/sponsorship/spam_sponsors_2020.json"
path_pre_rendered_mails_no_separator = "./tests/data/no-separator"
path_pre_rendered_mails_with_separator = "./tests/data/with-separator"
path_attachment = "./tests/data/attachment-file/attachment01.txt"


@pytest.fixture
def all_mails_base_no_separator():
    return get_all_mail_names_from_path(
        glob.glob("/".join((path_pre_rendered_mails_no_separator, "*@*")))
    )


@pytest.fixture
def all_mails_base_with_separator():
    return get_all_mail_names_from_path(
        glob.glob("/".join((path_pre_rendered_mails_with_separator, "*@*")))
    )


def get_mail_config():
    with open(path_mail_config, "rb") as f:
        return json.load(f)


def get_receivers():
    with open(path_receivers, "rb") as f:
        return json.load(f)


def get_all_mail_names_from_path(mails):
    all_mail_names = []
    for mail in mails:
        all_mail_names.append(os.path.basename(mail))

    return all_mail_names


def compare_on_sending_mail_all(
    targets, target_prefix="../examples", separator=" - ",
):
    receivers = get_receivers()
    receiver_emails = []
    for mail_name in targets:
        for receiver in receivers["unique_data"]:
            mail_addr, *mail_suffix_and_more = mail_name.split(separator, maxsplit=1)
            mail_suffix = mail_suffix_and_more[0] if mail_suffix_and_more else None
            print(f"Mail suffix is {mail_suffix}")
            if receiver["receiver_email"] == mail_addr:
                receiver_emails.append(mail_name)

    # Not all target emails could have the corresponding answers
    if len(receiver_emails) != len(targets):
        return False

    for mail_name in targets:
        for receiver in receivers["unique_data"]:
            if receiver["receiver_email"] == mail_name:
                if not compare_on_sending_mail(
                    "/".join((target_prefix, mail_name)), receivers
                ):
                    return False

    return True


def compare_on_sending_mail(target, receivers):
    mail_name = os.path.basename(target)
    mail_config = get_mail_config()

    with open(target, "rb") as f:
        target_content = pickle.load(f)
        if target_content["From"] != mail_config["From"]:
            return False

        if mail_name != target_content["To"]:
            return False

        if target_content["CC"] != mail_config["CC"]:
            return False

        for receiver in receivers["unique_data"]:
            if receiver["receiver_email"] == target_content["To"]:
                receiver_name = receiver["receiver_name"]

                if (
                    "no-separator" in target
                    and mail_config["Subject"] != target_content["Subject"]
                ):
                    return False

                if "with-separator" in target:
                    subject = " - ".join((mail_config["Subject"], receiver_name))
                    if subject != target_content["Subject"]:
                        return False

        if not is_attachment_expected(target_content):
            return False

    return True


def is_attachment_expected(target_content):
    for part in target_content.walk():
        content_disposition = part.get("Content-Disposition", None)
        if content_disposition:
            dispositions = content_disposition.strip().split(";")
            if bool(content_disposition and dispositions[0].lower() == "attachment"):
                target_data = part.get_payload(decode=True)
                with open(path_attachment, "rb") as fattachment:
                    base_data = fattachment.readlines()
                    data_str_target = target_data.decode("utf-8")
                    base_data_tmp = []

                    for line in base_data:
                        base_data_tmp.append(line.decode("utf-8"))
                    data_str_base = "".join(base_data_tmp)

                    if data_str_base != data_str_target:
                        return False

    return True


def test_send_mail_no_separator_no_attachment(all_mails_base_no_separator):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--debug",
            "--mails_path",
            path_pre_rendered_mails_no_separator,
            path_mail_config,
        ],
        input="y\nusername\npassword\n",
    )

    targets = get_all_mail_names_from_path(all_mails_base_no_separator)

    assert result.exit_code == 0
    assert compare_on_sending_mail_all(
        targets, target_prefix="/tmp/mail_handler/no-separator"
    )


def test_send_mail_no_separator_with_attachment(all_mails_base_no_separator):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--debug",
            "--mails_path",
            path_pre_rendered_mails_no_separator,
            "--attachment_file",
            path_attachment,
            path_mail_config,
        ],
        input="y\nusername\npassword\n",
    )

    targets = get_all_mail_names_from_path(all_mails_base_no_separator)

    assert result.exit_code == 0
    assert compare_on_sending_mail_all(
        targets, target_prefix="/tmp/mail_handler/no-separator"
    )


def test_send_mail_with_separator_dash_no_attachment(all_mails_base_with_separator):
    separator = " - "

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--debug",
            "--separator",
            separator,
            "--mails_path",
            path_pre_rendered_mails_with_separator,
            path_mail_config,
        ],
        input="y\nusername\npassword\n",
    )

    targets = get_all_mail_names_from_path(all_mails_base_with_separator)

    assert result.exit_code == 0
    assert compare_on_sending_mail_all(
        targets, target_prefix="/tmp/mail_handler/with-separator", separator=separator
    )


def test_send_mail_with_separator_dash_with_attachment(all_mails_base_with_separator):
    separator = " - "

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--debug",
            "--separator",
            separator,
            "--mails_path",
            path_pre_rendered_mails_with_separator,
            "--attachment_file",
            path_attachment,
            path_mail_config,
        ],
        input="y\nusername\npassword\n",
    )

    targets = get_all_mail_names_from_path(all_mails_base_with_separator)

    assert result.exit_code == 0
    assert compare_on_sending_mail_all(
        targets, target_prefix="/tmp/mail_handler/with-separator", separator=separator
    )
