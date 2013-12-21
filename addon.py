import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/percuiro_lib'))
import json

from xbmcswift2 import Plugin, xbmc
import urlresolver

from percuiro import (util, get_plugin_providers, get_plugin_provider,
                      user_providers)

plugin = Plugin()
plugin.user_providers = tuple()
no_click = lambda: plugin.url_for('_nowhere')


@plugin.route('/')
def index():
    items = [
        dict(
            label='search & play',
            path=plugin.url_for('search_and_play'),
        ),
        dict(
            label='search all providers',
            path=plugin.url_for('global_search')
        ),
        dict(
            label='search specific provider',
            path=plugin.url_for('search')
        ),
        dict(
            label='settings:',
            path=no_click()
        ),
        dict(
            label='  percuiro settings',
            path=plugin.url_for('percuiro_settings')
        ),
        dict(
            label='  provider settings',
            path=plugin.url_for('provider_settings')
        ),
        dict(
            label='  urlresolver settings',
            path=plugin.url_for('urlresolver_settings'))]
    if plugin.user_providers:
        items.append(
            dict(
                label='  reload my providers file',
                path=plugin.url_for('reload_user_providers')
            ))
    return items


@plugin.route('/search/<provider>', name='search_provider')
@plugin.route('/search')
def search(provider=None):
    if provider:
        p = get_plugin_provider(plugin, provider)
        query = get_keyboard_query()
        results = p.search(query)
        return list_results(results, provider)
    else:
        return map(
            lambda provider: dict(
                label='search {0}'.format(provider.name),
                path=plugin.url_for('search_provider', provider=provider.name),
                thumbnail=provider.thumbnail),
            get_plugin_providers(plugin, include_disabled=True))


@plugin.route('/search-and-play')
def search_and_play(query=None):
    '''
    Queries available providers in order of priority and plays first
    available result

    '''
    orig_query = None
    if not query:
        query = get_keyboard_query()
        orig_query = query
        if plugin.get_setting('prefer_720p'):
            if '720p' not in query or 'mkv' not in query:
                query += ' 720p'
    for provider in get_plugin_providers(plugin):
        plugin.notify(msg='Querying {0}...'.format(provider.name))
        results = provider.search(query)
        links = []
        for result in filter(
                lambda result: util.query_in_label(query, result['label']),
                results):
            plugin.notify(msg='{1}: Resolving link: {0}'.format(provider.name,
                          result['url']))
            if result.get('is_playable'):
                links.append(result)
            if not links:
                links = provider.get_link_page(result['url'])
            for link in links:
                resolved = urlresolver.resolve(link['url'])
                if resolved:
                    xbmc.Player().play(resolved)
                    return
                plugin.notify(msg='Failed resolving: {0}'.format(link['url']))
    if orig_query and orig_query is not query:
        plugin.notify('Search for 720p results failed...')
        return search_and_play(query)
    plugin.notify('Search & Play for query: {0!r} failed.'.format(query))


@plugin.route('/global-search/<next_pages>', name='global_search_next')
@plugin.route('/global-search')
def global_search(next_pages=None):
    provider_results = []
    if next_pages:
        next_pages = json.loads(next_pages)
        for provider_name, url in next_pages:
            plugin.notify(msg='Requesting next page for {0}..'.format(provider_name))
            provider = get_plugin_provider(plugin, provider_name)
            provider_results.append((provider_name, provider.parse_next_page(url)))
    else:
        query = get_keyboard_query()
        for provider in get_plugin_providers(plugin):
            plugin.notify(msg='Querying {0}..'.format(provider.name))
            provider_results.append((provider.name, provider.search(query)))
    items = []
    next_pages = []
    for provider_name, results in provider_results:
        if results:
            if results[-1]['label'] == 'Next >>':
                next_pages.append((provider_name, results.pop(-1)['url']))
            results = list_results(results, provider_name, indentation=4)
            results.insert(0, dict(
                label='{0} results:'.format(provider_name).upper(),
                path=plugin.url_for('_nowhere')))
            items.extend(results)
    if next_pages:
        items.append(dict(
            label='Next >>',
            path=plugin.url_for('global_search_next',
                                next_pages=json.dumps(next_pages))))
    return items


@plugin.route('/resolve-provider-page/<provider>/<url>/<label>')
def resolve_provider_page(provider, url, label):
    p = get_plugin_provider(plugin, provider)
    if label == 'Next >>':
        results = p.parse_next_page(url)
        return list_results(results, provider)
    else:
        results = p.get_link_page(url)
    return map(
        lambda result: dict(
            label=result['label'],
            path=plugin.url_for('resolve', url=result['url']),
            is_playable=True),
        results)


@plugin.route('/urlresolver-settings')
def urlresolver_settings():
    urlresolver.display_settings()


@plugin.route('/resolve/<url>')
def resolve(url):
    url = url.replace('#', '%23')
    resolved = urlresolver.resolve(url)
    return plugin.set_resolved_url(resolved)


@plugin.route('/percuiro-settings')
def percuiro_settings():
    plugin.open_settings()


@plugin.route('/provider-settings/<provider>/<setting>', name='provider_settings_set')
@plugin.route('/provider-settings')
def provider_settings(provider=None, setting=None):
    if provider:
        p = get_plugin_provider(plugin, provider)
        if setting == 'priority':
            # ask user for priority using keyboard
            priority = plugin.keyboard(
                default=str(p.priority),
                heading='Please enter new priority for {0}'.format(p.name))
            try:
                p.priority = priority
            except ValueError as e:
                plugin.notice(msg=e.message, title='ERROR!')
        else:
            p.toggle_status()
    items = [
        dict(
            label='PROVIDER SETTINGS:',
            path=no_click()
        ),
        dict(
            label=' priority = determines which provider is used first.',
            path=no_click()
        ),
        dict(
            label=' enabled = use provider for global search and search & play.',
            path=no_click()
        )]
    for provider in get_plugin_providers(plugin, include_disabled=True):
        items.extend([
            dict(
                label='{0}'.format(provider.name),
                path=plugin.url_for('_nowhere'),
                thumbnail=provider.thumbnail
            ),
            dict(
                label='  status    =   {0}'.format(provider.status),
                path=plugin.url_for(
                    'provider_settings_set',
                    provider=provider.name, setting='status'),
                thumbnail=provider.thumbnail
            ),
            dict(
                label='  priority  =  {0}'.format(provider.priority),
                path=plugin.url_for(
                    'provider_settings_set',
                    provider=provider.name,
                    setting='priority'),
                thumbnail=provider.thumbnail
            )
        ])
    return items


@plugin.route('/reload-user-providers')
def reload_user_providers():
    plugin.notify('Reloading user providers..')
    init_user_providers()
    plugin.notify('User providers reloaded..')


@plugin.route('/_nowhere')
def _nowhere():
    pass


def list_results(results, provider, indentation=0):
    items = []
    for result in results:
        item = {}
        url = result.pop('url')
        item['label'] = util.label_from_result(result)
        if result.get('is_playable'):
            item['path'] = plugin.url_for('resolve', url=url)
            item['is_playable'] = True
        else:
            item['path'] = plugin.url_for(
                'resolve_provider_page', provider=provider, url=url, label=result['label'])
        items.append(item)
    return items


def get_keyboard_query():
    last_search_storage = plugin.get_storage('last_search')
    last_search = last_search_storage.get('last_search', '')
    query = plugin.keyboard(default=last_search, heading='Enter search terms')
    if query:
        last_search_storage['last_search'] = query
    return query


def init_user_providers():
    user_providers_fpath = plugin.get_setting('user_providers_fpath')
    if user_providers_fpath:
        try:
            my_providers = user_providers.get_user_providers(user_providers_fpath)
        except user_providers.PercuiroUserProvidersException as e:
            plugin.notify(msg=e.message)
        else:
            plugin.user_providers = my_providers


if __name__ == '__main__':
    init_user_providers()
    plugin.run()
