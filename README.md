# Discord Notify

Forward Alliance Auth notifications to users on Discord

[![release](https://img.shields.io/pypi/v/aa-discordnotify?label=release)](https://pypi.org/project/aa-discordnotify/)
[![python](https://img.shields.io/pypi/pyversions/aa-discordnotify)](https://pypi.org/project/aa-discordnotify/)
[![django](https://img.shields.io/pypi/djversions/aa-discordnotify?label=django)](https://pypi.org/project/aa-discordnotify/)
[![pipeline](https://gitlab.com/ErikKalkoken/aa-discordnotify/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/aa-discordnotify/-/pipelines)
[![coverage report](https://gitlab.com/ErikKalkoken/aa-discordnotify/badges/master/coverage.svg)](https://gitlab.com/ErikKalkoken/aa-discordnotify/-/commits/master)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/aa-discordnotify/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Settings](#settings)
- [Change Log](CHANGELOG.md)

## Overview

This app forwards Alliance Auth notifications to users on Discord as DM.

### Features

- Notifications are colored according to level (e.g. INFO = blue)
- Option to forward superuser notifications only

## Example

![example](https://i.imgur.com/eebZFQj.png)

## Installation

### Preconditions

1. Discord Notify is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

2. Discord Notify needs the server [Discord Proxy](https://gitlab.com/ErikKalkoken/discordproxy) to function. Please make sure it is up and running on your site, before before continuing.

3. Please also make sure you have the Discord service enabled in Alliance Auth.

### Step 1 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install git+https://gitlab.com/ErikKalkoken/aa-discordnotify
```

### Step 2a - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'discordproxy'` to `INSTALLED_APPS`
- Optional: Add additional settings if you want to change any defaults. See [Settings](#settings) for the full list.

### Step 3 - Finalize App installation

Restart your supervisor services for Auth (no migration required).

Congratulations you are now ready to use Member Audit!

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your AA settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name | Description | Default
-- | -- | --
`DISCORDNOTIFY_DISCORDPROXY_PORT`| Port used to communicate with Discord Proxy. | `50051`
`DISCORDNOTIFY_SUPERUSER_ONLY`| When set to True, only superusers will be get their notifications forwarded. | `False`
