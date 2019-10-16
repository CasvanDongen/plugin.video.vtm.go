# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from time import time

from xbmc import Monitor

from resources.lib.kodiwrapper import KodiWrapper, LOG_INFO
from resources.lib.vtmgo.vtmgo import VtmGo, Content


class BackgroundService(Monitor):

    def __init__(self):
        Monitor.__init__(self)
        self.kodi = KodiWrapper()
        self.vtm_go = VtmGo(self.kodi)
        self.update_interval = 24 * 3600  # Every 24 hours

    def run(self):
        """ Background loop for maintenance tasks """
        self.kodi.log('Service started', LOG_INFO)

        while not self.abortRequested():
            # Update every `update_interval` after the last update
            if self.kodi.get_setting_as_bool('metadata_update') \
                    and int(self.kodi.get_setting('metadata_last_updated', 0)) + self.update_interval < time():
                self.update_metadata()
                self.kodi.set_setting('metadata_last_updated', str(int(time())))

            # Stop when abort requested
            if self.waitForAbort(10):
                break

        self.kodi.log('Service stopped', LOG_INFO)

    def onSettingsChanged(self):
        """ Callback when a setting has changed """
        self.kodi.log('IN VTM GO: Settings changed')

        # Refresh our VtmGo instance
        self.vtm_go = VtmGo(self.kodi)

    def update_metadata(self, delay=10):
        """ Update the metadata for the listings. """
        self.kodi.log('Updating metadata in the background')

        # Clear outdated metadata
        self.kodi.invalidate_cache(30 * 24 * 3600)  # one month

        vtm_go = self.vtm_go

        progress = self.kodi.show_progress_background(message=self.kodi.localize(30715))

        # Fetch all items from the catalogue
        items = vtm_go.get_items('all')
        count = len(items)

        # Loop over all of them and download the metadata
        for index, item in enumerate(items):
            # Update the items
            if item.video_type == Content.CONTENT_TYPE_MOVIE:
                if not vtm_go.get_movie(item.content_id, only_cache=True):
                    vtm_go.get_movie(item.content_id)
                    self.waitForAbort(delay / 1000)
            elif item.video_type == Content.CONTENT_TYPE_PROGRAM:
                if not vtm_go.get_program(item.content_id, only_cache=True):
                    vtm_go.get_program(item.content_id)
                    self.waitForAbort(delay / 1000)

            # Upgrade the progress bar
            progress.update(int(((index + 1) / count) * 100))

            # Abort when the setting is disabled or kodi is exiting
            if self.abortRequested() or not self.kodi.get_setting_as_bool('metadata_update'):
                break

        # Close the progress dialog
        progress.close()


def run():
    BackgroundService().run()