import preprocessor as p


p.set_options(
        p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.HASHTAG
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
    x = x.replace("|LBR|","")

    return x


