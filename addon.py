import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/percuiro_lib'))

from xbmcswift2 import Plugin, xbmcplugin, xbmcgui, actions
import urlresolver

import percuiro

plugin = Plugin()

providers = percuiro.get_active_providers()

@plugin.route('/')
def index():
    return map(
        lambda provider: dict(
            label='Search {}'.format(provider),
            path=plugin.url_for('search', provider=provider)),
        providers.keys())


@plugin.route('/search/<provider>')
def search(provider):
    p = providers[provider]
    query = plugin.keyboard(heading='Enter search terms')
    results = p.search(query)
    return map(
        lambda result: dict(
            label=result['label'],
            path=plugin.url_for('resolve_provider_page', provider=provider, url=result['url'])),
        results)


@plugin.route('/resolve-provider-page/<provider>/<url>')
def resolve_provider_page(provider, url):
    p = providers[provider]
    results = p.parse_result_page(url)
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


if __name__ == '__main__':
    plugin.run()
