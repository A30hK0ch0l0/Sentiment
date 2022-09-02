import re
from cleantext import clean
import hazm

normalizer = hazm.Normalizer()


def cleanhtml(raw_html):
    cleaner = re.compile('<.*?>')
    cleantext = re.sub(cleaner, '', raw_html)
    return cleantext


def cleaning(text):
    text = text.strip()

    # regular cleaning
    text = clean(text,
                 fix_unicode=True,
                 to_ascii=False,
                 lower=True,
                 no_line_breaks=True,
                 no_urls=True,
                 no_emails=True,
                 no_phone_numbers=True,
                 no_numbers=False,
                 no_digits=False,
                 no_currency_symbols=True,
                 no_punct=False,
                 replace_with_url="",
                 replace_with_email="",
                 replace_with_phone_number="",
                 replace_with_number="",
                 replace_with_digit="0",
                 replace_with_currency_symbol="",
                 )

    # cleaning htmls
    text = cleanhtml(text)

    # normalizing
    text = normalizer.normalize(text)

    # removing wierd patterns
    wierd_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               # u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)

    text = wierd_pattern.sub(r'', text)

    # removing extra spaces, hashtags
    text = re.sub("#", "", text)
    text = re.sub("\s+", " ", text)
    text = text.replace(u"\u200c", ' ')

    return text


def preprocessor(text: str):
    text = str(text).replace("\n", " ")
    text = f' {text.strip()} '

    pattern_retweet = re.compile(r'^ RT', re.IGNORECASE)
    pattern_mention = re.compile(r' @\S+')
    pattern_links = re.compile(r' (https?|ftp)://\S+')
    pattern_links_2 = re.compile(r' www\.\S+\.\S+')
    pattern_3_dot = re.compile(r"…")
    pattern_punctuation_in_first = re.compile(r'^[؟!،.:]')
    for reg in [pattern_retweet, pattern_mention, pattern_links, pattern_links_2, pattern_3_dot,
                pattern_punctuation_in_first]:
        text = re.sub(reg, ' ', text)

    # remove extra char
    text = re.sub(r'[^\w\u0621-\u06cc\u06F0-\u06F9؟?!:،.,]+', ' ', text)

    # bad punctuation
    text = re.sub(r'([?!:.,\u060C\u061B\u061F\u0640\u066A\u066B\u066C])+', r' \1 ', text)

    # Remove extra spaces
    text = re.sub(r'\s{2,}', ' ', text.strip())
    text = cleaning(text)
    text = text.replace(u"\u200c", ' ')

    return text
