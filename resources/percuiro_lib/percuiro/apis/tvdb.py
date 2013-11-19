# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from pytvdbapi import api

from .._exc import PercuiroException

db = api.TVDB('2B8557E0CBF7D720')

def query_tvdb(name):
    response = db.search(name, 'en')
    if not response.result:
        raise PercuiroException('TVDB db ERROR :: Query for show: {} returned 0 results'.format(name))
    results = []
    for show in response.result:
        show.update()
        results.append(dict(
            id=show.id,
            name=show.SeriesName,
            status=show.Status,
            banner='http://thetvdb.com/banners/{}'.format(show.banner),
            seasons= dict((
                season, [
                    dict(
                        season_episode='S{:0>2}E{:0>2}'.format(
                            episode.SeasonNumber,
                            episode.EpisodeNumber
                        ),
                        title=episode.EpisodeName
                    ) for episode in episodes ]
                ) for season, episodes in show.seasons.items())
            )
        )
    return results
