#!/usr/bin/env python3

# Copyright (C) 2020 Boulder Engineering Studio
# Author: Erin Hensel <hens0093@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import argparse
import subprocess

scripts = {
    'extract': 'support/1-extract.sh',
    'build': 'support/2-build.sh',
    'compose': 'support/3-compose.sh',
    'flash': 'support/4-flash.sh',
}


def run_script(script, env=None):
    command = ['/bin/bash', scripts[script]]

    proc = subprocess.Popen(
        command, env={k.upper(): v for (k, v) in env.items() if v is not None})

    proc.wait()
    if proc.returncode == 0:
        return True
    else:
        print('Encountered error {} running {}'.format(
            proc.returncode,
            script
        ))
        return False


def main(args):
    dev_prompt_actions = ['all', 'flash']
    if args.action in dev_prompt_actions and not args.dev:
        print('ERROR: must provide device with --dev')
        return

    all_actions = [
        ('extract', lambda: run_script('extract', vars(args))),
        ('build', lambda: run_script('build', vars(args))),
        ('compose', lambda: run_script('compose', vars(args))),
        ('flash', lambda: run_script('flash', vars(args))),
    ]

    actions = None
    if args.action == 'all':
        actions = all_actions
    else:
        actions = [a for a in all_actions if a[0] == args.action]

    for action in actions:
        print('Doing {}'.format(action[0]))
        if not action[1]():
            print('Failed {}'.format(action[0]))
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['all', 'extract', 'build', 'compose', 'flash']
    )
    parser.add_argument('--host', type=str, default='raspberrypi')
    parser.add_argument('--dev', type=str)
    parser.add_argument('--passwd', type=str, default='raspberry')
    parser.add_argument('--wpa-ssid', type=str)
    parser.add_argument('--wpa-pass', type=str)
    parser.add_argument('--img', type=str, default='raspbian.img')
    args = parser.parse_args()
    main(args)
