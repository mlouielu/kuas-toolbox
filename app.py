# -*- coding: utf-8 -*-

import const
import requests
from lxml import etree
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = False
app.secret_key = 'ggalkjfds;aksjdf@@'


def get_meeting_list():
    r = requests.get("http://bameeting.kuas.edu.tw/Meeting_Html_Ok_Sel.asp")
    r.encoding = "big5"

    root = etree.HTML(r.text)

    university_affairs_meeting = [(i.text, i.values()[0]) for i in root.xpath(
        "//select[@name='State0']")[0].iter()][1:]
    administrative_council_meeting = [(i.text, i.values()[0]) for i in root.xpath(
        "//select[@name='State']")[0].iter()][1:]

    return university_affairs_meeting, administrative_council_meeting


@app.route("/sitemap.xml")
def sitemap():
    url_root = request.url_root[:-1]

    uam, acm = get_meeting_list()
    rules = list(app.url_map.iter_rules()) + \
        ["/bameeting/" + i[1] for i in uam] + \
        ["/bameeting/" + i[1] for i in acm]

    return render_template("sitemap.xml", url_root=url_root, rules=rules)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/capital")
def capital():
    return render_template("capital.html")


@app.route("/space")
def space():
    return render_template("space.html")


@app.route("/memo")
def memo():
    return render_template("memo.html")


@app.route("/fuckthis")
def fuckthis():
    return render_template("fuckthis.html",
                           ga=const.ga_string)


@app.route("/club/beginning")
def club_beginning():
    return render_template("club_beginning.html")


@app.route("/committee")
def committee():
    return render_template("committee.html",
                           committee_list=const.committee_list,
                           ga=const.ga_string)


@app.route("/bameeting")
def bameeting():
    uam, acm = get_meeting_list()

    return render_template("bameeting.html",
                           uam=uam,
                           acm=acm)


@app.route("/bameeting/<string:issue_no>")
def bameeting_issue(issue_no):
    if issue_no.startswith(u"(104)高應臨校字第1號"):
        return render_template("principle.html")
    else:
        r = requests.post("http://bameeting.kuas.edu.tw/Meeting_Html_Ok.asp",
                          data={
                              "Meeting_ID": issue_no.encode("big5"),
                              "Meeting_ID0": ""
                          })

        r.encoding = "big5"
        content = r.text
        content = content.replace(
            ".\\ftpdata\\", "http://bameeting.kuas.edu.tw/.\\ftpdata\\")
        content = content.replace(
            ".\\Sign\\", "http://bameeting.kuas.edu.tw/.\\Sign\\")

        root = etree.HTML(content)

        # Change titles
        root.xpath("//title")[0].text = u"國立高雄應用科技大學 - %s - 會議記錄" % (issue_no)

        # Remove scripts tag
        for script in root.xpath("//script"):
            script.getparent().remove(script)

        # Remove basefont tag
        for basefont in root.xpath("//basefont"):
            basefont.getparent().remove(basefont)

        # Add id to font tags
        for index, font in enumerate(root.xpath("//font")):
            font.attrib["id"] = str(index + 1)

            # Check follow-up report div
            if not font.xpath("div/text()") and font.xpath("div"):
                font.xpath("div")[0].text = "DELETE"

        # Add GA tag
        ga_tag = etree.SubElement(root.xpath("/html/head")[0], "script")
        ga_tag.text = const.ga_string

        content = etree.tostring(root, encoding="utf-8").decode("utf-8")
        content = content.replace("&#13;", "")

        return content


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
