import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/percuiro_lib'))

from xbmcswift2 import Plugin, xbmcplugin, xbmcgui, actions
import urlresolver

plugin = Plugin()
from percuiro._module import module
plugin.register_module(module, '/_')

import percuiro
from percuiro import browser, QUERIES_TV, QUERIES_ALL



@plugin.route('/')
def index():
    menu_items = [
        {
            'label': 'search',
            'path': plugin.url_for('manual_search'),
            'is_playable': False
        },
        {
            'label': 'browser',
            'path': plugin.url_for('_browser')
        },
        {
            'label': 'urlresolver settings',
            'path': plugin.url_for('urlresolver_settings'),
            'is_playable': False
        }
    ]
    return menu_items


@plugin.route('/urlresolver-settings')
def urlresolver_settings():
    urlresolver.display_settings()


@plugin.route('/manual-search')
def manual_search():
    query = module.keyboard(heading='Search Filestube:')
    return search_tv_show(query)


@plugin.route('/search-tv-show/<query>')
def search_tv_show(query):
    results = percuiro.search(QUERIES_TV, query)
    return list_results(results)


def list_results(results):
    items = []
    for provider, results in results.items():
        items.append(dict(
            label='[{0}]'.format(provider),
            path=''
        ))
        for result in results:
            if result['resolved']:
                path = plugin.url_for('resolve', url=result['url'])
            else:
                path = plugin.url_for('provider_resolve', url=result['url'], provider=provider)
            items.append(dict(
                label=result['label'],
                path=path
            ))
    return items


@plugin.route('/resolve/<provider>/<url>', name='provider_resolve')
@plugin.route('/resolve/<url>')
def resolve(url, provider=None):
    resolved_url = None
    if provider:
        host_url = percuiro.resolve_provider_url(provider, url)
    else:
        host_url = url
    if host_url:
        result_url = urlresolver.resolve(host_url)
        if result_url:
            resolved_url = result_url
    plugin.set_resolved_url(resolved_url)


@plugin.route('/browser')
def _browser():
    menu_items = [
        {
            'label': 'my tv shows',
            'path': plugin.url_for('my_tv_shows')
        },
        {
            'label': 'add tv show',
            'path': plugin.url_for('add_tv_show')
        }
    ]
    return menu_items


@plugin.route('/browser/add-tv-show/<name>/<id>', name='do_add_tv_show')
@plugin.route('/browser/add-tv-show')
def add_tv_show(name=None, id=None):
    if not name:
        name = plugin.keyboard(heading='add tv show')
        results = browser.search_tvshow(name)
        return map(
            lambda result: dict(
                label=result['name'],
                path=plugin.url_for('do_add_tv_show', name=result['name'], id=result['id'])
            ), results
        )
    browser.add_tvshow(name, id)
    return plugin.redirect(plugin.url_for('tv_show', name=name))

@plugin.route('/browser/my-tv-shows')
def my_tv_shows():
    shows = map(
        lambda show: dict(
            label='{} - {}'.format(show['name'], show['status']),
            path=plugin.url_for('tv_show', name=show['name']),
            thumbnail=show['banner'],
            context_menu=[
                ('remove tv show', actions.background(
                    plugin.url_for('remove_tv_show', name=show['name'])))
            ]
        ), browser.get_tvshows())
    return shows



@plugin.route('/browser/remove-tv-show/<name>')
def remove_tv_show(name):
    browser.remove_tvshow(name)


@plugin.route('/browser/show/<name>/<season>', name='tv_show_season')
@plugin.route('/browser/show/<name>')
def tv_show(name, season=None):
    show = browser.get_tvshow(name)
    if not season:
        return map(
            lambda s: dict(
                label='{} - Season {:>2}'.format(name, s),
                path=plugin.url_for('tv_show_season', name=name, season=s)
            ), show['seasons'].keys())
    return map(
        lambda ep: dict(
            label='{season_episode} {title}'.format(**ep),
            path=plugin.url_for('search', query='{} {}'.format(
                show['name'], ep['season_episode']))
        ), show['seasons'][int(season)]
    )
 


if __name__ == '__main__':
    plugin.run()
