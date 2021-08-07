
## v0.4.1 (2021-08-07)

### Refactor

- update configurations from  Lee-W/cookiecutter-python-template

## v0.4.0 (2021-07-07)

### Feat

- **send_mail**: add sender name

## v0.3.2 (2021-06-18)

### Fix

- **mail_handler/render_mail.py-mail_hander/send_mail.py**: fix sending multiple mails with same mail address
- **send_mail.py-rend_mail.py**: fix big about multiple mails with same mail address
- **send_mail,-rend_mail**: fix bug of multiple mails with same mail address

## v0.3.1 (2021-04-20)

### Fix

- **encoding**: remove
- **encoding**: default to utf-8

## v0.3.0 (2021-04-19)

### Feat

- **render_mail**: click.option help information about separator

## v0.2.0 (2021-04-18)

### Feat

- **render_mail**: add more description including command help

## v0.1.1 (2021-04-18)

### Fix

- encoding(utf-8)

## v0.1.0 (2020-08-03)

### Feat

- setup render_mail, send_mail command after installing this package
- make mail_handler a python package
- replace pipenv with poetry
- **render and send**: use separator option instead of suffix
- Use file's basename in mail header.
- Add attachment file in mail
- **examples and templates**: add more new files
- **mail_sender**: implement cli to send mails
- **templates**: fix breakline format for financial aid template
- **renderer**: initial template renderer

### Refactor

- apply more pythonic styling
- **tests**: introduce conftest.py
- **tests**: introduce utils.py
- apply more pythonic idioms
- remove unused VERSION.txt (version is specified in pyproject.toml)
- **tasks/test**: allow no tests
- **tasks**: make invoke tasks a module and add task for new tools
- **cli scripts**: rename cli script from noun to verb
- **mail_renderer.py**: rename variables

### Fix

- **send_mail.py**: use if instead of if not None
