# -*- coding: utf-8 -*-
# dydrmntion@gmail.com


providers = (
    dict(
        name='filestube.com',
        base_url='http://www.filestube.com',
        query_url=('http://www.filestube.com/query.html?hosting=,23,99,15,24,13,'
                   '22,27,25,8,28,2,40,11,46,47,51,55,59,60,64,65,67,68,70,71,81,'
                   '87,92,97,102,104&q={query}'),
        result_selector=[('div', {'id': 'newresult'}), ('a',)],
        result_title=lambda result: result.text,
        result_link=lambda result: result.get('href'),
        thumbnail_url='http://www.userlogos.org/files/logos/teekay/filestube.png'
    ),
    dict(
        name='downtr.co',
        base_url='http://www.downtr.co',
        query_url='http://www.downtr.co/?do=search&subaction=search&story={query}',
        result_selector=[('div', {'class': 'result'}), ('div', {'class': 'name'}), ('a',)],
        result_title=lambda result: result.text,
        result_link=lambda result: result.get('href'),
        thumbnail_url='http://www.userlogos.org/files/imagecache/thumbnail/logos/Efreak15/12400474740-orig.png'
    ),
    dict(
        name='theextopia.com',
        base_url='http://www.theextopia.com',
        query_url='http://www.theextopia.com/?s={query}',
        result_selector=[('div', {'class': 'single'})],
        result_title=lambda result: result.find('div', {'class': 'title'}).text,
        result_link=lambda result: result.find('a', {'rel': 'bookmark'}).get('href'),
        thumbnail_url='http://www.theextopia.com/wp-content/themes/mobipress-theme/images/blogname.png'
    ),
    dict(
        name='rapidlibrary.biz',
        base_url='http://rapidlibrary.biz',
        query_url=lambda query: 'http://rapidlibrary.biz/{}/{}.html'.format(
            query[0], query.replace('+', '-')),
        result_selector=[('h3',)],
        result_title=lambda soup: soup.find('a').text,
        result_link=lambda soup: soup.find('a').get('href'),
        thumbnail_url='http://filespart.com/static/img/logo.png'
    )
)
