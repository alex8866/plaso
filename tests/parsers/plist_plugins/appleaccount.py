#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Apple account plist plugin."""

import unittest

# pylint: disable=unused-import
from plaso.formatters import plist as plist_formatter
from plaso.parsers.plist_plugins import appleaccount

from tests.parsers.plist_plugins import test_lib


class AppleAccountPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the Apple account plist plugin."""

  def testProcess(self):
    """Tests the Process function."""
    plist_file = (
        u'com.apple.coreservices.appleidauthenticationinfo.'
        u'ABC0ABC1-ABC0-ABC0-ABC0-ABC0ABC1ABC2.plist')
    plist_name = plist_file

    plugin_object = appleaccount.AppleAccountPlugin()
    storage_writer = self._ParsePlistFileWithPlugin(
        plugin_object, [plist_name], plist_name)

    self.assertEqual(len(storage_writer.events), 3)

    expected_timestamps = sorted([
        1372106802000000, 1387980032000000, 1387980032000000])
    timestamps = sorted([
        event_object.timestamp for event_object in storage_writer.events])

    self.assertEqual(timestamps, expected_timestamps)

    event_object = storage_writer.events[0]
    self.assertEqual(event_object.root, u'/Accounts')
    self.assertEqual(event_object.key, u'email@domain.com')

    expected_description = (
        u'Configured Apple account email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event_object.desc, expected_description)

    expected_message = u'/Accounts/email@domain.com {0:s}'.format(
        expected_description)
    expected_message_short = u'{0:s}...'.format(expected_message[:77])
    self._TestGetMessageStrings(
        event_object, expected_message, expected_message_short)

    event_object = storage_writer.events[1]
    expected_description = (
        u'Connected Apple account '
        u'email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event_object.desc, expected_description)

    event_object = storage_writer.events[2]
    expected_description = (
        u'Last validation Apple account '
        u'email@domain.com (Joaquin Moreno Garijo)')
    self.assertEqual(event_object.desc, expected_description)


if __name__ == '__main__':
  unittest.main()
