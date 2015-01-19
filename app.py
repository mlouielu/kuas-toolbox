# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/number/captial/<int:n>', methods=['GET', 'POST'])
def to_chinese_captial(n):
    if request.method == "POST":
        number = [u"零", u"壹", u"貳", u"參", u"肆", u"伍", u"陸", u"柒", u"捌", u"玖"]
        value = [u"拾", u"億", u"仟", u"佰", u"拾", u"萬", u"仟", u"佰", u"拾", u""]

        num = int(n)
        num_divide = [0 for i in range(15)]
        digit = 9
        while num:
            num_divide[digit] = num % 10;
            digit -= 1
            num //= 10

        result = []
        for i in range(digit + 1, 10):
            if num_divide[i] != 0:
                result.append(number[num_divide[i]])
                result.append(value[i])
            elif i == 1 or i == 5:
                result.append(value[i])
            elif num_divide[i + 1] != 0:
                result.append(number[num_divide[i]])

        result.append(u"圓整")

        return "".join(result)
    else:
        return redirect("")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
