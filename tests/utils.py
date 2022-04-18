import filecmp
import json
import os
import pickle
from email.utils import parseaddr

path_mail_config = "./examples/sponsorship/spam_sponsors_2020_mail_config.json"
path_receivers = "./examples/sponsorship/spam_sponsors_2020.json"
path_attachment = "./tests/data/attachment-file/attachment01.txt"
path_pre_rendered_mails_no_separator = "./tests/data/no-separator"
path_pre_rendered_mails_no_separator_and_csv = "./tests/data/no-separator-and-csv"
path_pre_rendered_mails_with_separator = "./tests/data/with-separator"
path_pre_rendered_mails_with_separator_and_csv = "./tests/data/with-separator-and-csv"
path_mails_to_send_no_separator = "/tmp/mails_to_send/no-separator"
path_mails_to_send_no_separator_and_csv = "/tmp/mails_to_send/no-separator-and-csv"
path_mails_to_send_with_separator = "/tmp/mails_to_send/with-separator"
path_mails_to_send_with_separator_and_csv = "/tmp/mails_to_send/with-separator-and-csv"
send_mail_debug_dump_path = "/tmp/mail_handler"


def get_all_mail_names_from_path(mails):
    return [os.path.basename(mail) for mail in mails]


def compare_rendered_mail_all(
    targets, base_prefix="./data", target_prefix="../examples"
):
    for mail_name in targets:
        if not compare_rendered_mail(
            "/".join((base_prefix, mail_name)), "/".join((target_prefix, mail_name))
        ):
            return False

    return True


def compare_rendered_mail(base, target):
    return filecmp.cmp(base, target, shallow=False)


def get_mail_config():
    with open(path_mail_config, "rb") as f:
        return json.load(f)


def get_receivers():
    with open(path_receivers, "rb") as f:
        return json.load(f)


def compare_on_sending_mail_all(
    targets,
    target_prefix="../examples",
    separator=" - ",
):
    receivers = get_receivers()
    receiver_emails = []
    for mail_name in targets:
        mail_name, ishtml = os.path.splitext(mail_name)
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
        mail_name, ishtml = os.path.splitext(mail_name)
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
        target_content_sender_name, target_content_from = parseaddr(
            target_content["From"]
        )
        if target_content_from != mail_config["From"]:
            return False

        if target_content_sender_name != mail_config["SenderName"]:
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
            if dispositions[0].lower() == "attachment":
                target_data = part.get_payload(decode=True)
                with open(path_attachment, "rb") as fattachment:
                    base_data = fattachment.readlines()
                    data_str_target = target_data.decode("utf-8")
                    data_str_base = "".join(
                        [line.decode("utf-8") for line in base_data]
                    )

                    if data_str_base != data_str_target:
                        return False

    return True
