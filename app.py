# -*- coding: utf-8 -*-

import re
import meeting
import const
import requests
from lxml import etree
from flask import Flask, render_template, request
from flask.ext.misaka import Misaka


app = Flask(__name__)
Misaka(app)
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


def get_latest_meeting_list():
    r = requests.get("http://bameeting.kuas.edu.tw/Meeting_Html_Sel.asp")
    r.encoding = "big5"

    root = etree.HTML(r.text)

    return [(i.text, i.values()[0]) for i in root.xpath(
        "//select[@name='State']")[0].iter()][1:]


def get_cameeting_list():
    r = requests.get(
        "http://cameeting.kuas.edu.tw/EducationalAdministrateMeeting.asp")
    r.encoding = "big5"

    root = etree.HTML(r.text)

    ca_meeting = [(i.text, i.values()[0]) for i in root.xpath(
        "//select[@name='State0']")[0].iter()][1:]

    return ca_meeting


def get_latest_cameeting_list():
    r = requests.get("http://cameeting.kuas.edu.tw/Meeting_Html_Sel.asp")
    r.encoding = "big5"

    root = etree.HTML(r.text)

    return [(i.text, i.values()[0]) for i in root.xpath(
        "//select[@name='State']")[0].iter()][1:]


@app.route("/sitemap.xml")
def sitemap():
    url_root = request.url_root[:-1]

    uam, acm = get_meeting_list()
    #cam = get_cameeting_list()
    rules = list(app.url_map.iter_rules()) + \
        ["/bameeting/" + i[1] for i in uam] + \
        ["/bameeting/" + i[1] for i in acm]
        #["/cameeting/" + i[1] for i in cam]

    return render_template("sitemap.xml", url_root=url_root, rules=rules)


@app.route("/robots.txt")
def robots():
    return "User-agent: *"


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


@app.route("/fuckthis/2015")
def fuckthis2015():
    return render_template("2015fuckthis.html",
                           ga=const.ga_string)


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


@app.route("/law")
def kuaslaw():
    content = requests.get(
        "https://raw.githubusercontent.com/kuassp/kuaslaw/master/README.md").content

    try:
        return render_template("law.html", content=content)
    except UnicodeDecodeError:
        return render_template("law.html", content=content.decode("utf-8"))


@app.route("/ppp")
def ppp():
    p = {
        "name": "會計系", "link": "https://www.facebook.com/acckuas",
        "name": "觀光管理系", "link": "https://www.facebook.com/KUASTMA",
        "name": "土木工程系", "link": "https://www.facebook.com/KUASCivilEngineering",
        "name": "財富與稅務管理學系", "link": "https://www.facebook.com/KUAS103rdWTM",
        "name": "企業管理系", "link": "https://www.facebook.com/kuasba",
        "name": "資訊管理系", "link": "https://www.facebook.com/KUASMISSA",
        "name": "資訊工程系", "link": "https://www.facebook.com/kuascsie",
        "name": "應用外語系", "link": "https://www.facebook.com/KUASxAFLD",
        "name": "文化創意產業學系", "link": "https://www.facebook.com/I.LIKE.CCI",
        "name": "模具工程系", "link": "https://www.facebook.com/國立高雄應用科技大學-模具工程系學會-446635782136841",
        "name": "電子工程系學會", "link": "https://www.facebook.com/國立高雄應用科技大學-電子工程系學會-200392033367356",
        "name": "金融系", "link": "https://www.facebook.com/KUAS.FIN",
        "name": "工業與工程管理系", "link": "https://www.facebook.com/kuasiem",
        "name": "機械工程系", "link": "https://www.facebook.com/kuasme",
        "name": "電機工程系", "link": "https://www.facebook.com/國立高雄應用科技大學-電機工程系學會-483608054998190",
        "name": "國際企業系", "link": "https://www.facebook.com/kuasib",
        "name": "人力資源發展系", "link": "https://www.facebook.com/HRD102nd",
        "name": "化學工程與材料工程系", "link": "https://www.facebook.com/103CME",
    }

    return ""


@app.route("/bameeting")
def bameeting():
    uam, acm = get_meeting_list()
    #cam = get_cameeting_list()

    return render_template("bameeting.html",
                           uam=uam,
                           acm=acm)
                           #cam=cam)


#@app.route("/bameeting/latest")
def bameeting_latest():
    uam = get_latest_meeting_list()
    #cam = get_latest_cameeting_list()

    return render_template("bameeting_latest.html",
                           uam=uam)
                           #cam=cam)


#@app.route("/bameeting/latest/<string:issue_no>")
def bameeting_latest_issue(issue_no):
    r = requests.post("http://bameeting.kuas.edu.tw/Meeting_Html.asp",
                      data={"Meeting_ID": issue_no.encode("big5")})

    r.encoding = "big5"
    content = r.text
    content = content.replace(
        ".\\ftpdata\\", "http://bameeting.kuas.edu.tw/.\\ftpdata\\")
    content = content.replace(
        ".\\Sign\\", "http://bameeting.kuas.edu.tw/.\\Sign\\")

    content = meeting.meeting_parse(content, issue_no)

    return content


@app.route("/bameeting_detail/<string:issue_no>")
def bameeting_detail_issue(issue_no):
    root = meeting.get_meeting_root(issue_no)


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

        content = meeting.meeting_parse(content, issue_no)

        return content


@app.route("/cameeting/latest/<string:issue_no>")
def cameeting_latest_issue(issue_no):
    r = requests.post("http://cameeting.kuas.edu.tw/Meeting_Html.asp",
                      data={"Meeting_ID": issue_no.encode("big5")})

    r.encoding = "big5"
    content = r.text
    content = content.replace(
        ".\\ftpdata\\", "http://cameeting.kuas.edu.tw/.\\ftpdata\\")
    content = content.replace(
        ".\\Sign\\", "http://cameeting.kuas.edu.tw/.\\Sign\\")

    content = meeting.meeting_parse(content, issue_no)

    return content


@app.route("/cameeting/<string:issue_no>")
def cameeting_issue(issue_no):
    r = requests.post("http://cameeting.kuas.edu.tw/EducationalAdministrateMeetingRecord.asp",
                      data={
                          "Meeting_ID": issue_no.encode("big5"),
                          "Meeting_ID0": ""
                      })

    r.encoding = "big5"
    content = r.text
    content = content.replace(
        ".\\ftpdata\\", "http://cameeting.kuas.edu.tw/.\\ftpdata\\")
    content = content.replace(
        ".\\Sign\\", "http://cameeting.kuas.edu.tw/.\\Sign\\")

    content = meeting.meeting_parse(content, issue_no)

    return content


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
