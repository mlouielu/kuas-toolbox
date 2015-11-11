# -*- coding: utf-8 -*-

ga_string = """
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-56307180-3', 'auto');
  ga('send', 'pageview');
"""

committee_list = [
    {
        "name": u"行政會議",
        "scripts_url": "http://sa.kuas.cc/bameeting",
        "scripts_name": u"行政會議紀錄",
        "members_url": "",
        "members_name": u"會議名單",
        "committee_rule": "",
        "affiliation": u"校務",
        "student_member": False
    },
    {
        "name": u"校務會議",
        "scripts_url": "http://sa.kuas.cc/bameeting",
        "scripts_name": u"校務會議紀錄",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "",
        "affiliation": u"校務",
        "student_member": True
    },
    {
        "name": u"學務會議",
        "scripts_url": "http://student.kuas.edu.tw/files/11-1002-29.php",
        "scripts_name": u"學務會議紀錄",
        "members_url": "http://student.kuas.edu.tw/files/11-1002-29.php",
        "members_name": u"會議名單",
        "committee_rule": "",
        "affiliation": u"校務",
        "student_member": True
    },
    {
        "name": u"教務會議",
        "scripts_url": "http://academic.kuas.edu.tw/files/11-1001-24.php",
        "scripts_name": u"教務會議紀錄",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "",
        "affiliation": u"校務",
        "student_member": True
    },
    {
        "name": u"總務會議",
        "scripts_url": "http://b0013.kuas.edu.tw/files/11-1013-53.php",
        "scripts_name": u"總務會議記錄",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "",
        "affiliation": u"校務",
        "student_member": True
    },
    {
        "name": u"性別平等教育委員會",
        "scripts_url": "http://gender.kuas.edu.tw/files/11-1005-4.php?Lang=zh-tw",
        "scripts_name": u"性別平等教育專區",
        "members_url": "http://gender.kuas.edu.tw/files/11-1005-5.php?Lang=zh-tw",
        "members_name": u"會議名單",
        "committee_rule": "http://student.kuas.edu.tw/files/14-1002-3689,r68-1.php",
        "affiliation": u"學務處",
        "student_member": True
    },
    {
        "name": u"車輛管理委員會",
        "scripts_url": "http://b0013.kuas.edu.tw/files/11-1013-34.php",
        "scripts_name": u"車輛管理委員會會議記錄",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://gen.kuas.edu.tw/files/14-1013-21361,r8-1.php",
        "affiliation": u"總務處",
        "student_member": True
    },
    {
        "name": u"校園規劃委員會",
        "scripts_url": "http://gen.kuas.edu.tw/files/11-1013-61.php",
        "scripts_name": u"校園規劃委員會會議記錄",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://gen.kuas.edu.tw/files/14-1013-16783,r39-1.php",
        "affiliation": u"組織章程委員會",
        "student_member": False
    },
    {
        "name": u"校務基金管理委員會",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://accounting.kuas.edu.tw/files/15-1010-14681,c18-1.php",
        "affiliation": u"組織章程委員會",
        "student_member": False
    },
    {
        "name": u"校園發展委員會",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://secretary.kuas.edu.tw/files/15-1003-5318,c6-1.php",
        "affiliation": u"",
        "student_member": False
    },
    {
        "name": u"衛生委員會",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://student.kuas.edu.tw/ezfiles/2/1002/img/633/973177.pdf",
        "affiliation": u"學務處",
        "student_member": True
    },
    {
        "name": u"圖書諮詢委員會",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://www.lib.kuas.edu.tw/library2/file/rule/17.pdf",
        "affiliation": u"",
        "student_member": True
    },
    {
        "name": u"學生申訴評議委員會",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "http://student.kuas.edu.tw/files/14-1002-40499,r240-1.php",
        "affiliation": u"",
        "student_member": True
    },
    {
        "name": u"空間管理委員會議",
        "scripts_url": "",
        "scripts_name": u"",
        "members_url": "",
        "members_name": u"",
        "committee_rule": "b0013.kuas.edu.tw/ezfiles/13/1013/img/592/EE005.pdf",
        "affiliation": u"總務處",
        "student_member": False
    },
]
