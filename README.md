# Discord Notify

Forward Alliance Auth notifications to users on Discord

[![release](https://img.shields.io/pypi/v/aa-discordnotify?label=release)](https://pypi.org/project/aa-discordnotify/)
[![python](https://img.shields.io/pypi/pyversions/aa-discordnotify)](https://pypi.org/project/aa-discordnotify/)
[![django](https://img.shields.io/pypi/djversions/aa-discordnotify?label=django)](https://pypi.org/project/aa-discordnotify/)
[![pipeline](https://gitlab.com/ErikKalkoken/aa-discordnotify/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/aa-discordnotify/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/aa-discordnotify/branch/master/graph/badge.svg?token=QHMCUAFZBV)](https://codecov.io/gl/ErikKalkoken/aa-discordnotify)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/aa-discordnotify/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your AA settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name | Description | Default
-- | -- | --
`DISCORDNOTIFY_SUPERUSER_ONLY`| When set to True, only superusers will be get their notifications forwarded. | `False`
