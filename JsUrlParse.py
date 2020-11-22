import re, jsbeautifier
import datetime
import requests
import json

class ViewParseAjaxHandler():
    def initialize(self):
        return

    def find_str(self, s, char):
        index = 0
        if char in s:
            c = char[0]
            for ch in s:
                if ch == c:
                    if s[index:index + len(char)] == char:
                        return index
                index += 1
        return -1

    def findEntireLine(self, contents, str):
        lineNum = 0
        for item in contents.split("\n"):
            if str in item:
                linkPos = self.find_str(item, str)
                return item, lineNum, linkPos
            lineNum = lineNum + 1

    def parseForLinks(self, contents):
        discoveredLinks = []
        outputLinks = []
        # ugh lol
        # regex = r"[^/][`'\"]([\/][a-zA-Z0-9_.-]+)+(?!([gimuy]*[,;\s])|\/\2)"
        regex = r"([\/][a-zA-Z0-9_.-]+)+"
        links = re.finditer(regex, contents)
        for link in links:
            linkStr = link.group(0)
            # discoveredLinks list to avoid dupes and complex dupe checks
            if linkStr not in discoveredLinks:
                # get the entire line, line number, and link position
                entireLine, lineNum, linkPos = self.findEntireLine(contents, linkStr)
                discoveredLinks.append(linkStr)
                outputLinks.append({
                    "line": entireLine,
                    "link": linkStr,
                    "lineNum": lineNum,
                    "linkPos": linkPos
                })
        return outputLinks

    def getFormattedTimestamp(self):
        d = datetime.datetime.now()
        formatted = "{}_{}_{}_{}-{}".format(d.month, d.day, d.year, d.hour, d.minute)
        return formatted


    def beautifyJS(self, content):
        return jsbeautifier.beautify(content)

    def isLongLine(self, line):
        if len(line) > 1000:
            return True
        return False

    def fileRoutine(self, url, content):
        html = ""

        # beautify the JS for cleaner parsing
        # note: this can be slow against large JS files and can lead to failure
        prettyContent = self.beautifyJS(content)

        # parse all the links out
        parsedLinks = self.parseForLinks(prettyContent)
        return parsedLinks

    def fetchURL(self, url, headers=[]):
        res=requests.get(url=url,headers=headers)
        return res.text

    def parseLinks(self, url, headers=[]):
        file = self.fetchURL(url, headers)
        return self.fileRoutine(url, file)



tool=ViewParseAjaxHandler()
ret=tool.parseLinks('https://www.anquanke.com/js/site.min.js?v1.0.5')
print(json.dumps(ret, indent=4, sort_keys=True))
