import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/percuiro_lib'))
import json

from xbmcswift2 import Plugin, xbmcplugin, xbmcgui, actions, xbmc, actions
import urlresolver

from percuiro import util, get_plugin_providers, get_plugin_provider

plugin = Plugin()

@plugin.route('/')
def index():
    providers = get_plugin_providers()
    items = [
        dict(
            label='search & play',
            path=plugin.url_for('search_and_play'),
        ),
        dict(
            label='search enabled providers',
            path=plugin.url_for('global_search')
        ),
        dict(
            label='provider settings',
            path=plugin.url_for('provider_settings'))]
    items.extend(map(
        lambda provider: dict(
            label=provider.name,
            path=plugin.url_for('search', provider=provider.name),
            thumbnail=provider.thumbnail),
        providers))
    return items


@plugin.route('/search/<provider>')
def search(provider):
    p = get_plugin_provider(provider)
    query = get_keyboard_query()
    results = p.search(query)
    return list_results(results, provider)


@plugin.route('/search-and-play')
def search_and_play():
    '''
    Queries available providers in order of priority and plays first
    available result
    
    '''
    query = get_keyboard_query()
    for provider in get_plugin_providers():
        plugin.notify(msg='Querying {}...'.format(provider.name))
        results = provider.search(query)
        for result in filter(
                lambda result: util.query_in_label(query, result['label']),
                results):
            plugin.notify(msg='{}: Resolving link: {}'.format(provider.name,
                result['url']))
            links = provider.get_link_page(result['url'])
            for link in links:
                resolved = urlresolver.resolve(link['url'])
                if resolved: 
                    xbmc.Player().play(resolved)
                    return xbmcswift2.finish()
                plugin.notify(msg='Failed resolving: {}'.format(link['url']))


@plugin.route('/global-search/<next_pages>', name='global_search_next')
@plugin.route('/global-search')
def global_search(next_pages=None):
    provider_results = []
    if next_pages:
        next_pages = json.loads(next_pages)
        for provider_name, url in next_pages:
            plugin.notify(msg='Requesting next page for {}..'.format(provider_name))
            provider = providers[provider_name]
            provider_results.append((provider_name, provider.parse_next_page(url)))
    else:
        query = get_keyboard_query()
        for provider in get_plugin_providers():
            plugin.notify(msg='Querying {}..'.format(provider.name))
            provider_results.append((provider.name, provider.search(query)))
    items = []
    next_pages = []
    for provider_name, results in provider_results:
        if results:
            if results[-1]['label'] == 'Next >>':
                next_pages.append((provider_name, results.pop(-1)['url']))
            results = list_results(results, provider_name, indentation=4)
            results.insert(0, dict(
                label='{} results:'.format(provider_name).upper(),
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
    p = get_plugin_provider(provider)
    if label == 'Next >>':
        results = p.parse_next_page(url)
        return list_results(results, provider)
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
    resolved = urlresolver.resolve(url)
    plugin.set_resolved_url(resolved)




@plugin.route('/provider-settings/<provider>/<setting>', name='provider_settings_set')
@plugin.route('/provider-settings')
def provider_settings(provider=None, setting=None):
    if provider:
        p = get_plugin_provider(provider)
        if setting == 'priority':
            # ask user for priority using keyboard
            priority = plugin.keyboard(default=str(p.priority),
                heading='Please enter new priority for {}'.format(p.name))
            try:
                p.priority = priority
            except ValueError as e:
                plugin.notice(msg=e.message, title='ERROR!')
        else:
            p.toggle_status()
    items = []
    for provider in get_plugin_providers():
        items.extend([
            dict(
                label=provider.name,
                path=plugin.url_for('_nowhere')
            ),
            dict(
                label='    status    =   {}'.format(provider.status),
                path=plugin.url_for('provider_settings_set', 
                    provider=provider.name, setting='status')
            ),
            dict(
                label='    priority  =  {}'.format(provider.priority),
                path=plugin.url_for('provider_settings_set', 
                    provider=provider.name,
                    setting='priority'))
        ])
    return items


def list_results(results, provider, indentation=0):
    return map(
        lambda result: dict(
            label=' '.join('' for x in xrange(indentation)) + result['label'],
            path=plugin.url_for('resolve_provider_page', provider=provider, url=result['url'], label=result['label'])),
        results)


def get_keyboard_query():
    last_search_storage  = plugin.get_storage('last_search')
    last_search = last_search_storage.get('last_search', '')
    query = plugin.keyboard(default=last_search, heading='Enter search terms')
    if query:
        last_search_storage['last_search'] = query
    return query


if __name__ == '__main__':
    plugin.run()
