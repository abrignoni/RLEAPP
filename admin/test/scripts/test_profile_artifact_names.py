"""Profiles name artifacts that exist, and a name that does not is reported.

A profile selects artifacts by exact name. zProfileExample.rlprofile listed 'iOSnotes', which is iNotes, and 'reddit', which this version does not have. Loading it
ran one of its three artifacts and said nothing.
These tests check every profile shipped in the repository against the artifacts that load,
and the helper the command line uses to warn about names it cannot find.
"""
import json
import pathlib
import sys
import types
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

import rleapp  # pylint: disable=wrong-import-position
from scripts import plugin_loader  # pylint: disable=wrong-import-position


class ProfileArtifactNamesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.plugins = list(plugin_loader.PluginLoader().plugins)

    def test_every_shipped_profile_names_only_available_artifacts(self):
        profiles = sorted(REPO_ROOT.glob('*.rlprofile'))
        self.assertTrue(profiles)
        for profile in profiles:
            names = json.loads(profile.read_text(encoding='utf-8'))['plugins']
            self.assertEqual(rleapp.profile_plugins_not_found(names, self.plugins), [], profile.name)

    def test_names_not_found_are_returned_sorted_and_case_matters(self):
        plugins = [types.SimpleNamespace(name='addressBook'), types.SimpleNamespace(name='voicemail')]

        self.assertEqual(
            rleapp.profile_plugins_not_found({'voicemail', 'calendar', 'addressbook'}, plugins),
            ['addressbook', 'calendar'])
        self.assertEqual(rleapp.profile_plugins_not_found({'voicemail', 'addressBook'}, plugins), [])


if __name__ == '__main__':
    unittest.main()
