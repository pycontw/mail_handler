# Mail Handler

Generate emails through the template and send mails

## Prerequisite

* [Python 3](https://www.python.org/downloads/)
* [click](http://click.palletsprojects.com/en/7.x/)

## Usage

This CLI tool is designed as two steps to avoid accidental sending.

### Step 1: Generate mails through the template

```sh
python render_mail.py [OPTIONS] TEMPLATE_PATH RECEIVER_DATA

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
        "receiver_email": "somerec@somedomain"
    ]
}
```

* `--mails_path PATH`: The output path of the mails. The mail will be named as the receivers email address.

### Step 2: Send the generated mails

```sh
python send_mail.py [OPTIONS] CONFIG_PATH

Options:
  --output_path PATH  [default: mails_to_sent]
```

* `CONFIG_PATH`: The path to mail config.

```json
{
    "Subject": "some subject",
    "From": "somebody@somedomain"
    "CC": "somebody1@somedomain, somebody2@somedomain"
}
```

* `--mails_path PATH`: The path of the mails to sent.

## Development

### Additional Prerequiste

* [invoke](http://www.pyinvoke.org)
* [pipenv](https://pipenv.readthedocs.io)

### Environment Setup

```sh
inv init
```

### Check Style

```sh
inv lint
```

## Authors

[Lee-W](https://github.com/Lee-W)
