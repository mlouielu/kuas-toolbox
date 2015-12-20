# -*- coding: utf-8 -*-

import re
import requests
from lxml import etree


def _get_working_block(report):
    block = []
    working_title = list(report.itertext())[0]

    if working_title.startswith(u"肆、提案討論"):
        raise IndexError("Out of working reports")

    report = report.getnext().getnext()
    while report.tag.startswith("div"):
        block.append(report)
        report = report.getnext()

    report = report.getnext()

    return report, working_title, block


def _parse_working_block(divs):
    """This shit is very buggy now,
    In year of 94, 93, this function will mess up when the web is very dirty
    Help, Help, Help
    """
    indent = [(2, 2), (3, 4), (2, 4), (3, 6), ]

    level_offset = 0
    level_pool = []
    for div in divs:
        # Get style indent
        if "width" not in div.attrib["style"]:
            level = tuple(map(int, re.findall("\d", div.attrib["style"])))

            # Bad data, see you next timeT
            if level[0] == 0:
                continue

            if level[0] == level[1]:
                level = (2, 2)

            try:
                level = indent.index(level)
            except:
                raise IndexError
        else:
            level += 1

        # Check for level_offset (admin-94-4-電子計算機中心)
        if not level_pool and level != 0:
            level_offset = level

        # Using level_offset
        if level - level_offset > -1:
            level -= level_offset

        # Append to pool
        if level == 0:
            level_pool.append({"content": div.text, "child": []})
        else:
            while level:
                pool = level_pool[-1]["child"]
                level -= 1

            pool.append({"content": div.text, "child": []})

    return level_pool


def _print_working_block(pools, level):
    for p in pools:
        print("%s%s" % ("..." * level, p["content"]))
        if p["child"]:
            _print_working_block(p["child"], level + 1)


def _parse_working_reports(report):
    working_reports = []

    while True:
        try:
            report, title, divs = _get_working_block(report)
        except IndexError:
            break

        pools = _parse_working_block(divs)
        working_reports.append({"title": title, "reports": pools})

    return report, working_reports


def _parse_follow_up(report):
    resolutions = []

    while "size" not in report.attrib:
        proposer_text = report.xpath("div/text()")[0]
        proposer = proposer_text[proposer_text.find(
            "、") + 1: proposer_text.find("：") - 1]

        resolution = report.xpath(
            "following-sibling::font[1]/div/text()")[0].replace("\u3000", " ")
        reporting = report.xpath("following-sibling::font[2]/div/text()")[0]

        # Append to resolutions
        resolutions.append(
            {"proposer": proposer, "proposer_text": proposer_text,
             "resolution": resolution, "report": reporting})

        # Advance report
        report = report.xpath("following-sibling::font[3]")[0]

    return report, resolutions


def parse_header(root):
    header = {}

    header['title'] = root.xpath("id('1')/b/text()")[0]
    header['time'] = root.xpath("id('2')/following-sibling::text()[1]")[0]
    header['place'] = root.xpath("id('3')/following-sibling::text()[1]")[0]
    header['chairman'] = root.xpath(
        "id('4')/following-sibling::text()[1]")[0].replace("\u3000", " ")
    header['note_taker'] = root.xpath(
        "id('5')/following-sibling::text()[1]")[0].replace("\u3000", " ")

    # Case for attendee
    header['attendee'] = root.xpath("id('6')")[0].getnext()
    if "href" in header['attendee'].attrib:
        header['attendee'] = header['attendee'].attrib["href"]
    else:
        header['attendee'] = root.xpath(
            "id('6')/following-sibling::text()[1]")[0]

    return header


def parse_introduction(root):
    introduction = []
    intro = root.xpath("id('8')/preceding-sibling::br")[-2]
    while "id" not in intro.getprevious().attrib:
        introduction.append(
            intro.xpath("preceding-sibling::text()")[-1])
        intro = intro.getprevious()

    introduction = introduction[::-1]

    return introduction


def parse_follow_up(root):
    report = root.xpath("id('8')")[0].getnext().getnext()
    follow_up_reports = []
    other_business_reports = []

    # Check there have follow-up reports
    if report.tag == "font":
        report, follow_up_reports = _parse_follow_up(report)
    else:
        report = root.xpath("id('9')")[0]

    if report.xpath("b/text()")[0].startswith(u"(臨時動議)"):
        # bypass br
        report = report.getnext().getnext()
        report, other_business_reports = _parse_follow_up(report)

    return report, follow_up_reports, other_business_reports


def parse_working_reports(root):
    report = root.xpath("//font/b[text()='參、各單位工作報告']")[0].getparent()
    report = report.xpath("following-sibling::font[1]")[0]
    report, working_reports = _parse_working_reports(report)

    return report, working_reports


def _parse_resolution(report):
    if report.tag != "table":
        raise IndexError("Out of resolution")

    # Resolution information
    resolution_no, resolution_proposer = report.xpath("tr/td//text()")
    resolution_proposer = resolution_proposer[5:]

    # Brief of resolution
    report = report.getnext()
    brief = report.text[4:]

    # Detailed of resolution
    report = report.xpath("following-sibling::font[1]")[0]
    detail_end = report.xpath("following-sibling::b[1]")[0]

    detail = []
    while True:
        report = report.getnext()
        if report == detail_end:
            break

        for t in report.itertext():
            detail.append(t)

    # Decision of resolutionb
    decision = report.text[4:]

    resolution = {
        "no": resolution_no,
        "proposer": resolution_proposer,
        "brief": brief,
        "detail": detail,
        "decision": decision
    }

    return report.getnext().getnext(), resolution


def parse_resolutions(root):
    report = root.xpath("//font/b[text()='肆、提案討論']")[0].getparent()
    report = report.xpath("following-sibling::table[1]")[0]

    resolutions = []
    while True:
        try:
            report, resolution = _parse_resolution(report)
            resolutions.append(resolution)
        except IndexError:
            break

    return resolutions


def parse(r):
    if isinstance(r, str):
        root = etree.HTML(r)
    else:
        root = r

    content = {}

    ############################
    # Start parseing content
    # 0. Header
    ############################
    content['header'] = parse_header(root)

    ######################
    # 1. Introduction
    ######################
    introduction = parse_introduction(root)
    content["introduction"] = introduction

    ########################################
    # 2. Follow-up reports of last meeting
    #    And check if there is other business
    ########################################
    report, follow_up_reports, other_business_reports = parse_follow_up(root)
    content["follow_up_reports"] = follow_up_reports
    content["follow_up_other_business_reports"] = other_business_reports

    #######################
    # 3. Working reports
    #######################
    report, working_reports = parse_working_reports(root)
    content["working_reports"] = working_reports

    #######################
    # 4. Resolutions
    #######################
    resolutions = parse_resolutions(root)
    content["resolutions"] = resolutions

    return content


def get_meeting_content(s):
    r = requests.get("http://sa.kuas.cc/bameeting/%s" % (s)).text
    r = r.replace("\r", "").replace("\n", "").replace("\t", "")

    return r


def get_meeting_root(s):
    return etree.HTML(get_meeting_content(s))


def get_administrative_meeting_list():
    r = requests.get("http://sa.kuas.cc/bameeting")
    root = etree.HTML(r.text)

    acm_list = [i.attrib["href"][11:] for i in root.xpath("id('acm')/a")]

    return acm_list


def get_university_meeting_list():
    r = requests.get("http://sa.kuas.cc/bameeting")
    root = etree.HTML(r.text)

    uam_list = [i.attrib["href"][11:] for i in root.xpath("id('uam')/a")]

    return uam_list


def get_all_resolutions():
    acm_list = get_administrative_meeting_list()

    resolutions = []
    for acm in acm_list:
        content = parse(acm)

        for resolution in content["resolutions"]:
            pass

def test_admin_meeting_header():
    acm_list = get_administrative_meeting_list()

    for i in acm_list[:2]:
        return parse(get_meeting_content(i))
        header, content = parse(get_meeting_content(i))
        print(header['title'])
        print("-----------------------------------------")


if __name__ == "__main__":
    pass
