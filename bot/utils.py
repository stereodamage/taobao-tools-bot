ITEM_ID = 'id='
ITEM = 'item/'
SHOP_ID = 'shop_id='
TAOBAO_URL = 'https://item.taobao.com/item.htm?id='
TMALL_URL = 'https://detail.tmall.com/item.htm?id='
SHOP_URL = 'https://shop{}.taobao.com'
TAOBAO_POSTLINK = 'taobao.com'
M_INTL = f'm.intl.{TAOBAO_POSTLINK}'
H5 = f'h5.m.{TAOBAO_POSTLINK}'
WORLD = f'world.{TAOBAO_POSTLINK}'
SHOP_M = f'shop.m.{TAOBAO_POSTLINK}'
SEARCH_QUERY = '/search.htm?search=y'


def get_item_id(url, match_type: str):
    """

    :param url: full url string
    :param match_type: match string to look for as the beginning of potential id
    :return:
    """
    start = url.index(match_type) + len(match_type)
    end = len(url)

    for pos in range(start, end):
        if not url[pos].isdigit():
            end = pos
            break
    return url[start:end]


def build_taobao_url(url: str, match_type: str, is_shop: bool):
    return SHOP_URL.replace('{}', get_item_id(url, match_type)) if is_shop else TAOBAO_URL + get_item_id(url,
                                                                                                         match_type)


def clear_taobao_url(url: str):
    end = url.find('taobao.com/')
    if end == -1:
        return url
    else:
        end = url.index('taobao.com/') + 10
        if 'search.htm' in url:
            return url[0:end] + SEARCH_QUERY
        else:
            return url[0:end]


def convert_url(full_url):
    if 'tmall.com' in full_url:
        return TMALL_URL + get_item_id(full_url, ITEM_ID)

    if M_INTL or H5 in full_url:
        return build_taobao_url(full_url, ITEM_ID, False)
    elif WORLD in full_url:
        if 'item' in full_url:
            return build_taobao_url(full_url, ITEM, False)
        return clear_taobao_url(full_url.replace('world.taobao.com', 'taobao.com'))
    elif SHOP_M in full_url:
        return build_taobao_url(full_url, SHOP_ID, True)
    elif 'item' not in full_url:
        # Clean the store link, remove any redundant information, and conevrt from mobile if relevant
        return clear_taobao_url(full_url)
    else:
        # Already valid Taobao URL, canonise it
        return build_taobao_url(full_url, 'id=', False)
