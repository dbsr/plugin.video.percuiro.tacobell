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

    query_url (str|lambda|tuple):
        The url used by percuiro to query the provider.
        When its a str Percuiro expects it to have a `{query}` placeholder.
        When its a lambda it should take the query as its argument and return
        an url.
        When its a tuple percuiro assumes the query method should be post. Its'
        first item should be the full action post url, the second value should
        be the name of the the post data.

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

    test_data (dict):
        Optional. This data is used to test the provider.
        keys:
            query (str): the query to search for
            num_search_results (int): how many results should the provider return
            first_link_url (str): the url of the first result


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
                   '22,27,25,8,28,2,40,11,46,47,51,55,59,60,64,65,67,70,71,81,'
                   '87,92,97,102,104&q={query}'),
        result_selector=[('div', {'class': 'newresult'})],
        get_result_label=lambda result: result.find('a', {'class': 'resultsLink'}).text,
        get_result_url=lambda result: result.find('a', {'class': 'resultsLink'}).get('href'),
        thumbnail_url='http://www.userlogos.org/files/logos/teekay/filestube.png',
        test_data=dict(
            query='veep s01e01',
            num_search_results=10,
            first_link_url='/c0r25p5wgATB2eaJktPx1o'
        )
    ),
    dict(
        name='downtr.co',
        base_url='http://www.downtr.co',
        query_url='http://www.downtr.co/?do=search&subaction=search&story={query}',
        result_selector=[('div', {'class': 'result'}), ('div', {'class': 'name'}), ('a',)],
        get_result_label=lambda result: result.text,
        get_result_url=lambda result: result.get('href'),
        thumbnail_url='http://www.userlogos.org/files/imagecache/thumbnail/logos/Efreak15/12400474740-orig.png',
        test_data=dict(
            query='parks and recreation s06e08',
            num_search_results=10,
            first_link_url='http://www.downtr.co/2747314-parks-and-recreation-s06e08-720p-hdtv-x264-dimension.html'
        )
    ),
    dict(
        name='theextopia.com',
        base_url='http://www.theextopia.com',
        query_url='http://www.theextopia.com/?s={query}',
        result_selector=[('div', {'class': 'single'})],
        get_result_label=lambda result: result.find('div', {'class': 'title'}).text,
        get_result_url=lambda result: result.find('a', {'rel': 'bookmark'}).get('href'),
        thumbnail_url='http://www.theextopia.com/wp-content/themes/mobipress-theme/images/blogname.png',
        test_data=dict(
            query='modern family s04e01',
            num_search_results=6,
            first_link_url='http://www.theextopia.com/modern-family-s04e01-hdtv-x264-2hd-modern-family-s04e01-720p-hdtv-x264-dimension/'
        )
    ),
    dict(
        name='filetram.com',
        base_url='http://filetram.com',
        query_url=lambda query: 'http://filetram.com/{0}'.format(query.replace(' ', '-')),
        result_selector=[('a', {'class': 'highlight-item'})],
        get_result_label=lambda soup: soup.text,
        get_result_url=lambda soup: soup.get('href'),
        thumbnail_url='http://d1.filetram.com/cb3661976221/images/logos.png',
        test_data=dict(
            query='modern family s05e03',
            num_search_results=1,
            first_link_url='http://mega-search.me/goto-136240'
        )
    ),
    dict(
        name='sharedir.com',
        base_url='http://sharedir.com',
        query_url='http://sharedir.com/index.php?s={query}&ftype=4&stype=0,3,4,8,9,10,11,12,13,15,20,22,23,28,29,32,33,34,35,38,40,48,53,54,56,59,64,66,68,71,75,78,80,82,86,87,88,89,91,92,93&sort=dd',
        result_selector=[('a', {'class': 'big'})],
        get_result_label=lambda soup: soup.text,
        get_result_url=lambda soup: soup.get('href'),
        thumbnail_url='http://uploadcity.com/images/uc.gif',
        test_data=dict(
            query='modern family s05e03',
            num_search_results=1,
            first_link_url='http://mega-search.me/goto-136240'
        )
    )
)
