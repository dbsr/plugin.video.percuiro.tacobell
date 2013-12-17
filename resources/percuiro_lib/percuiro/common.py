# -*- coding: utf-8 -*-
# dydrmntion@gmail.com


REAL_DEBRID_REGEX = (
    r'1fichier.com|1st-files.com|2shared.com|4shared.com|aetv.com' +
    '|bayfiles.com|bitshare.com|canalplus.fr|cbs.com|cloudzer.net|crocko.com' +
    '|cwtv.com|dailymotion.com|dengee.net|depfile.com|dizzcloud.com|dl.free.fr' +
    '|extmatrix.com|filebox.com|filecloud.io|filefactory.com|fileflyer.com' +
    '|fileover.net|filepost.com|filerio.com|filesabc.com|filesend.net|filesflash.co' +
    '|filesmonster.com|freakshare.net|gigasize.com|hipfile.com|hotfile.co' +
    '|hugefiles.net|hulkshare.com|hulu.com|jumbofiles.com|justin.tv|keep2share.c' +
    '|letitbit.net|load.to|mediafire.com|mega.co.nz|megashares.com|mixturevideo.co' +
    '|netload.in|nowdownload.eu|nowvideo.eu|purevid.com|putlocker.com|rapidgator.net' +
    '|rapidshare.com|redtube.com|rutube.ru|scribd.com|sendspace.com|share-online.bi' +
    '|sharefiles.co|shareflare.net|slingfile.com|sockshare.com|soundcloud.co' +
    '|speedyshare.com|turbobit.net|ultramegabit.com|unibytes.co' +
    '|uploaded.to|uploaded.net|ul.to|uploadhero.co|uploading.com|uptobox.co' +
    '|userporn.com|veevr.com|vimeo.com|vip-file.com|wat.tv|youporn.com|youtube.com'
)

PROVIDERS_THUMBNAIL_PATH = 'provider_thumbnails'

FILTER_EXTENSIONS = 'rar', 'zip', 'exe', 'pdf', 'mp3', 'epub'
VIDEO_EXTENSIONS = 'mkv', 'avi', 'mp4', 'wmv', 'flv', 'mpeg', 'mpg'
FILE_EXTENSIONS_REGEX = r'\.({})'.format('|'.join(FILTER_EXTENSIONS + VIDEO_EXTENSIONS))
