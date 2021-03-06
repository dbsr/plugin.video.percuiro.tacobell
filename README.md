# Percuiro Taco Bell


### Version

* 0.6
    -Fixed filestube resolve logic
    -Added various providers
    -Ditched urlresolver requirement.For now only works with Real Debrid

* 0.5
    Install addon using my repo. Download the repo.zip here: 
    [repository.dbsr.xbmc_addons.zip](https://github.com/dbsr/repository.dbsr.xbmc_addons/raw/master/repository.dbsr.xbmc_addons.zip)
### Description

Percurio Taco Bell is a video plugin for xbmc. You can use it to search for
video files using a combination of search providers.
Default search providers:

- filestube.com
- downtr.co
- theextopia.com
- mega-search.me


### Features

- ####Search & Play

  This will search all providers in turn (sorted by customizable provider
  priority) until it finds a playable result. Playable means the file exists
  on the filehost in question and is resolvable to a link the user can
  download.

- ####Search all enabled providers

  Although it's possible to search a specific provider it's way more
  delicious to search all providers at once. Fiesta!

- ####Add custom search providers

  Although it still requires you to write some code you wont need a lot programming exprience
  to add your own search providers. Have a look at the user provider documentation and study 
  the format of the default providers if you want to give it a try. Please submit your
  new providers so we can make them available for everyone!


## User Providers

```python
'''
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
```

### Important

This addon uses the module urlresolver to resolve search results to playable links. Without a subscribtion
of some kind to a premium (multi) file host you will be one sad donkey.

### ?Por que lo llamas percuiro Taco Bell?

    *Me gustan mucho los tacos y mi espanol es terrible.*

### Contact

dydrmntion at gmail punkto com
