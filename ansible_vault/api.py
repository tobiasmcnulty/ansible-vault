#
# Copyright (C) 2017, Tomohiro NAKAMURA <quickness.net@gmail.com>
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
#
from __future__ import absolute_import

import yaml

from ._compat import VaultLib, decode_text, make_secrets


class Vault(object):
    """R/W an ansible-vault yaml file"""

    def __init__(self, password):
        self.secret = password.encode("utf-8")
        self.vault = VaultLib(make_secrets(self.secret))

    def load_raw(self, stream):
        """Read vault stream and return raw data."""
        return self.vault.decrypt(stream)

    def dump_raw(self, text, stream=None):
        """Encrypt raw data and write to stream."""
        encrypted = decode_text(self.vault.encrypt(text))
        if stream:
            stream.write(encrypted)
        else:
            return encrypted

    def load(self, stream):
        """Read vault steam and return python object."""
        return yaml.safe_load(self.load_raw(stream))

    def dump(self, data, stream=None):
        """Encrypt data and print stdout or write to stream."""
        yaml_text = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        return self.dump_raw(yaml_text, stream=stream)
