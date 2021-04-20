import preprocessor as p

import re

p.set_options(
        p.OPT.URL, 
        #p.OPT.EMOJI,      ## this demoji is also removing umlaut...
        p.OPT.MENTION, 
        p.OPT.RESERVED,  
        p.OPT.SMILEY, 
        p.OPT.HASHTAG
    )

def clean_tweet(x):
    """ 
    URL	p.OPT.URL
    Mention	p.OPT.MENTION
    Hashtag	p.OPT.HASHTAG
    Reserved Words	p.OPT.RESERVED
    Emoji	p.OPT.EMOJI
    Smiley	p.OPT.SMILEY
    Number	p.OPT.NUMBER
    """
    x = p.clean(x)
    x = remove_emoji(x)
    x = x.replace('|LBR|', "")
    return x

def remove_emoji(string):
     
    emoji_pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])', 
    flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)