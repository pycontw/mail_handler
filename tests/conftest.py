import glob
import os
import shutil

import pytest

from tests.utils import path_pre_rendered_mails_no_separator, path_pre_rendered_mails_with_separator, \
    get_all_mail_names_from_path, path_mails_to_send_no_separator, path_mails_to_send_with_separator, send_mail_debug_dump_path

@pytest.fixture
def all_mails_base_no_separator():
    yield get_all_mail_names_from_path(
        glob.glob("/".join((path_pre_rendered_mails_no_separator, "*@*")))
    )
    if os.path.isdir(path_mails_to_send_no_separator):
        shutil.rmtree(path_mails_to_send_no_separator)
    if os.path.isdir(send_mail_debug_dump_path):
        shutil.rmtree(send_mail_debug_dump_path)


@pytest.fixture
def all_mails_base_with_separator():
    yield get_all_mail_names_from_path(
        glob.glob("/".join((path_pre_rendered_mails_with_separator, "*@*")))
    )
    if os.path.isdir(path_mails_to_send_with_separator):
        shutil.rmtree(path_mails_to_send_with_separator)
    if os.path.isdir(send_mail_debug_dump_path):
        shutil.rmtree(send_mail_debug_dump_path)
