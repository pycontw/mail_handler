
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
