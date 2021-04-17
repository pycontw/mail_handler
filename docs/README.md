# Mail Handler

Generate emails through the template and send mails

## Prerequisite

* [Python 3](https://www.python.org/downloads/)
* [click](http://click.palletsprojects.com/en/7.x/)

## Usage

This CLI tool is designed as two steps to avoid accidental sending.

### Step 1: Install pycontw-mail-handler through pipx (or install in your virtual environment)

```sh
# Install pipx
python -m pip install pipx

# Install pycontw-mail-hanlder through pipx
python -m pipx install pycontw-mail-handler
```

After install `pycontw-mail-handler`, you can run `render_mail` and `send_mail` commands in your environment.

### Step 2: Generate mails through the template

```sh
render_mail [OPTIONS] TEMPLATE_PATH RECEIVER_DATA

Options:
  --mails_path PATH  [default: mails_to_sent]
```

* `TEMPLATE_PATH`: The path to the jinja2 template.
* `RECEIVER_DATA`: The path to receivers' data.
    * The following json sample is the least required content. All other data can be added to fit the need of the template.
    * "common_data": Common data used in each mail
    * "unique_data": Unique content for each mail

```json
{
    "common_data": {},
    "unique_data": [
        {"receiver_email": "somerec@somedomain"}
    ]
}
```

Please note the comma is able to be used as a receiver separator to send multiple people. For example, the following 3
formats are all working:

A space following a comma
```json
{
    "common_data": {},
    "unique_data": [
        {"receiver_email": "somerec01@somedomain, somerec02@somedomain"}
    ]
}
```

No space following a comma
```json
{
    "common_data": {},
    "unique_data": [
        {"receiver_email": "somerec01@somedomain,somerec02@somedomain"}
    ]
}
```

Or mix both of the above two types
```json
{
    "common_data": {},
    "unique_data": [
        {"receiver_email": "somerec01@somedomain, somerec02@somedomain,somerec03@somedomain"}
    ]
}
```


* `--mails_path PATH`: The output path of the mails. The mail will be named as the receivers email address.

Usage example:

```
render_mail  ./templates/sponsorship/spam_sponsors_2020.j2 examples/sponsorship/spam_sponsors_2020.json
```


### Step 3: Send the generated mails

```sh
send_mail [OPTIONS] CONFIG_PATH

Options:
  --mails_path PATH  [default: mails_to_sent]
  --attachment_file PATH
```

* `CONFIG_PATH`: The path to mail config.

```json
{
    "Subject": "some subject",
    "From": "somebody@somedomain",
    "CC": "somebody1@somedomain, somebody2@somedomain"
}
```

Please note the comma is used as a receiver separator to send multiple people.

* `--mails_path PATH`: The path of the mails to sent.

Usage example:

```
send_mail ./examples/sponsorship/spam_sponsors_2020_mail_config.json
```


By issuing the `send_mail.py` command,
you will be prompted to input the corresponding password of your smtp server.

```plaintext
You are about to send the mails under "mails_to_sent". Do you want to continue? [y/N]: y
Please enter your mail account: <sender email address in mail config>
Please enter you mail password:
INFO:root:Email sent to <receiver address in RECEIVER_DATA>!
```

Currently we only support the smtp server of `gmail`,
so you may want to use the one-time app password for security concern.
To use gmail one-time app password, please go to
`Manage your Goolge Account > Security > Signning to Google > App passwords` and then
`Select app > Other`
to generate your one-time app password. The generated password could be removed anytime
if you are sure that you won't use it anymore.

## Contributing
See [Contributing](contributing.md)

## Authors

[Lee-W](https://github.com/Lee-W)
