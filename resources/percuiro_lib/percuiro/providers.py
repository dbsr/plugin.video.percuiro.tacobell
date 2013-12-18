# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

'''
This are the default providers. It is very easy to add your own provider.
It should follow the same structure as the providers listed below.

PROVIDER DICTIONARY KEYWORDS:

    name (str):
        The name of the provider

    base_url (str):
        The url of the provider without any arguments / resources.
        This is used to resolve internal urls to their fully
        qualified urls. Eg. When a link has /foo as its url.
        Percuiro will add this to the base_url
        (http://ohhi.com/foo) before it makes the request.

    query_url (str):
        The url used by percuiro to query the provider. Percuiro expects
        this str to have a `{query}` placeholder.

    result_selector (list):
        A list of tuples where each tuple is a selector step to get to
        the query result(s). If you're familiar with jQuery or BeautifulSoup
        this should be pretty self explanatory.
        Percuiro uses the html of a page to filter out results. The
        result_selector describes the path from the top of the html document
        to the elements containing information about the results we are
        interested in.

    get_result_label (lambda):
        This should be a lambda (function) which takes one argument, a soup
        object of one result element. It should return a str which percuiro
        uses as a title for the result in question.

    get_link_label (lambda):
        Much like `get_result_label` but instead returns the link of the result.

    next_page_format (regex_str):
        Optional, this can be used for providers which do not use 'next'
        in their pagination to designate the next page of the result set.
        The regex should be as exclusive as possible and only capture the
        part of the url containing the page number.
        Example:
            A provider uses this url for the 2nd page of results:
                http://provider.net/?q=blah&p=2
            A good regex_str in this case would be:
                r'.*&p=([0-9]+)$'
            Note: don't forget the capture braces. Percuiro uses this to
            increment from the current page to the next.

    thumbnail_url (str):
        Optional, an external url to the logo of the provider. Percuiro will
        only download this once and use it in the xbmc menu's.


MY_PROVIDERS FILE STRUCTURE:

    Percuiro expects the my_providers.py file to have one variable called
    `my_providers`. This variable should be a tuple containing your customo
    provider(s).

MY_PROVIDERS FILE LOCATION:

    You can specify the location of the `my_providers.py` file in the
    percuiro settings. Make sure xbmc has access / read rights to the file.

SUBMIT PROVIDERS TO ME

    Please share your providers with us so we can make them available to everyone!

'''

providers = (
    dict(
        name='filestube.com',
        base_url='http://www.filestube.com',
        query_url=('http://www.filestube.com/query.html?hosting=,23,99,15,24,13,'
                   '22,27,25,8,28,2,40,11,46,47,51,55,59,60,64,65,67,68,70,71,81,'
                   '87,92,97,102,104&q={query}'),
        result_selector=[('div', {'id': 'newresult'})],
        get_result_label=lambda result: result.find('a').text,
        get_result_url=lambda result: result.find('a').get('href'),
        thumbnail_url='http://www.userlogos.org/files/logos/teekay/filestube.png'
    ),
    dict(
        name='downtr.co',
        base_url='http://www.downtr.co',
        query_url='http://www.downtr.co/?do=search&subaction=search&story={query}',
        result_selector=[('div', {'class': 'result'}), ('div', {'class': 'name'}), ('a',)],
        get_result_label=lambda result: result.text,
        get_result_url=lambda result: result.get('href'),
        thumbnail_url='http://www.userlogos.org/files/imagecache/thumbnail/logos/Efreak15/12400474740-orig.png'
    ),
    dict(
        name='theextopia.com',
        base_url='http://www.theextopia.com',
        query_url='http://www.theextopia.com/?s={query}',
        result_selector=[('div', {'class': 'single'})],
        get_result_label=lambda result: result.find('div', {'class': 'title'}).text,
        get_result_url=lambda result: result.find('a', {'rel': 'bookmark'}).get('href'),
        thumbnail_url='http://www.theextopia.com/wp-content/themes/mobipress-theme/images/blogname.png'
    ),
    dict(
        name='rapidlibrary.biz',
        base_url='http://rapidlibrary.biz',
        query_url=lambda query: 'http://rapidlibrary.biz/{}/{}.html'.format(
            query[0], query.replace('+', '-')),
        result_selector=[('ol', {'class': 'results-list'}), ('li',)],
        get_result_label=lambda soup: soup.find('a').text,
        get_result_url=lambda soup: soup.find('a').get('href'),
        thumbnail_url='http://filespart.com/static/img/logo.png'
    )
)
