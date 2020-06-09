
from xml.sax import make_parser, handler

class StopPositionHandler(handler.ContentHandler):
    def __init__(self):
        self.lines = set()
        self.stopPlaces = set()
        self.parents = dict()
        self.currentStop = ""
        self.current_content = ""
        self.parentTag = ""

    def startElement(self, name, attrs):
        self.current_content=""
        if name == "StopPlace":
            self.parentTag = "StopPlace"
            if "id" in attrs:
                self.currentStop = attrs['id']
                self.stopPlaces.add(attrs['id'])
        elif name == "ParentSiteRef" and self.parentTag == "StopPlace":
            if "ref" in attrs:
                self.parents[self.currentStop] = attrs['ref']
        elif name == "Line":
            self.parentTag = "Line"


    def characters(self, content):
        self.current_content += content.strip()

    def endElement(self, name):
        if name=="StopPlace":
            self.parentTag = ""
        elif name=="Line":
            self.parentTag = ""
        elif name == "PublicCode" and self.parentTag == "Line":
            self.lines.add(self.current_content)




