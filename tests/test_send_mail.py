from click.testing import CliRunner

from mail_handler.send_mail import main
from tests.utils import (
    compare_on_sending_mail_all,
    get_all_mail_names_from_path,
    path_attachment,
    path_mail_config,
    path_pre_rendered_mails_no_separator,
    path_pre_rendered_mails_with_separator,
)


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
