import glob

import pytest

from tests.utils import path_pre_rendered_mails_no_separator, path_pre_rendered_mails_with_separator, \
    get_all_mail_names_from_path

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
