import glob

from click.testing import CliRunner

from mail_handler.render_mail import main
from tests.utils import (
    compare_rendered_mail_all,
    get_all_mail_names_from_path,
    path_mails_to_send_no_separator,
    path_mails_to_send_no_separator_and_csv,
    path_mails_to_send_with_separator,
    path_mails_to_send_with_separator_and_csv,
)

path_j2 = "./templates/sponsorship/spam_sponsors_2020.j2"
path_receivers_json = "./examples/sponsorship/spam_sponsors_2020.json"
path_receivers_json_no_unique = (
    "./examples/sponsorship/spam_sponsors_2020_no_unique.json"
)
path_unique_csv = "./examples/sponsorship/spam_sponsors_2020_unique_data.csv"
path_pre_rendered_mails_no_separator = "./tests/data/no-separator"
path_pre_rendered_mails_no_separator_and_csv = "./tests/data/no-separator-and-csv"
path_pre_rendered_mails_with_separator = "./tests/data/with-separator"
path_pre_rendered_mails_with_separator_and_csv = "./tests/data/with-separator-and-csv"


def test_rendered_mail_no_separator(all_mails_base_no_separator):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            path_j2,
            path_receivers_json,
            "--output_path",
            path_mails_to_send_no_separator,
        ],
    )
    all_mails_target = get_all_mail_names_from_path(
        glob.glob("/".join((path_mails_to_send_no_separator, "*@*")))
    )

    assert result.exit_code == 0
    assert len(all_mails_base_no_separator) == len(all_mails_target)
    assert compare_rendered_mail_all(
        all_mails_target,
        base_prefix=path_pre_rendered_mails_no_separator,
        target_prefix=path_mails_to_send_no_separator,
    )


def test_rendered_mail_no_separator_and_csv(all_mails_base_no_separatorr_and_csv):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            path_j2,
            path_receivers_json_no_unique,
            "--unique_csv",
            path_unique_csv,
            "--output_path",
            path_mails_to_send_no_separator_and_csv,
        ],
    )

    all_mails_target = get_all_mail_names_from_path(
        glob.glob("/".join((path_mails_to_send_no_separator_and_csv, "*@*")))
    )

    assert result.exit_code == 0
    assert len(all_mails_base_no_separatorr_and_csv) == len(all_mails_target)
    assert compare_rendered_mail_all(
        all_mails_target,
        base_prefix=path_pre_rendered_mails_no_separator_and_csv,
        target_prefix=path_mails_to_send_no_separator_and_csv,
    )


def test_rendered_mail_with_separator_dash(all_mails_base_with_separator):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            path_j2,
            path_receivers_json,
            "--output_path",
            path_mails_to_send_with_separator,
            "--separator",
            " - ",
        ],
    )

    all_mails_target = get_all_mail_names_from_path(
        glob.glob("/".join((path_mails_to_send_with_separator, "*@*")))
    )

    assert result.exit_code == 0
    assert len(all_mails_base_with_separator) == len(all_mails_target)
    assert compare_rendered_mail_all(
        all_mails_target,
        base_prefix=path_pre_rendered_mails_with_separator,
        target_prefix=path_mails_to_send_with_separator,
    )


def test_rendered_mail_with_separator_dash_and_csv(
    all_mails_base_with_separator_and_csv,
):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            path_j2,
            path_receivers_json_no_unique,
            "--unique_csv",
            path_unique_csv,
            "--output_path",
            path_mails_to_send_with_separator_and_csv,
            "--separator",
            " - ",
        ],
    )

    all_mails_target = get_all_mail_names_from_path(
        glob.glob("/".join((path_mails_to_send_with_separator_and_csv, "*@*")))
    )

    assert result.exit_code == 0
    assert len(all_mails_base_with_separator_and_csv) == len(all_mails_target)
    assert compare_rendered_mail_all(
        all_mails_target,
        base_prefix=path_pre_rendered_mails_with_separator_and_csv,
        target_prefix=path_mails_to_send_with_separator_and_csv,
    )
