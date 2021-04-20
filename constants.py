from collections import namedtuple
Entity = namedtuple("Entity", " docid, entity_value, start, end, entity_type, ")
from string import Template

entity_types = {"beschwerden": "BESCHWER", "person":"PERSON"}


# Spacy: override for spacy html templates for rendering entity
TEMPLATE_ENT = """<mark data-entity="{label}">
{text}</mark>
"""

# CSS: html templates for css
MARK_OPEN = Template("""
<mark data-entity="$ner_type">
$ner_value
"""  )

MARK_CLOSE = " </mark>"

HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
<style>
h1 {
  color: orange;
}
</style>
<link rel="stylesheet" type="text/css" href="asr-style.css">
</head>
<body>

<h1>This is a heading</h1>
<p>The style of this document is a combination of an external stylesheet, and internal style</p>

<div class="entities" style="line-height: 2.5; direction: ltr">

   $mark     

</div>

</body>
</html>
"""
)