# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from random import sample
import random
import requests
from telegram import send_message


app = Flask(__name__)
app.secret_key = '12345'


# route
@app.route("/")
def index():
    return render_template('new_index.html')
    
    
# @app.route("/ide/<string:username>/<string:workspace>")
# def username_workspace(username, workspace):
#     return render_template('ide.html', name = username, space = workspace)
    
    
# @app.route("/hi")
# def hi():
#     return "Hello SSAFY"
    

# @app.route("/lotto/<int:item1>/<int:item2>/<int:item3>/<int:item4>/<int:item5>/<int:item6>")
# def self_lotto(item1, item2, item3, item4, item5, item6):
#     your_numbers = [item1, item2, item3, item4, item5, item6]
#     win_numbers = get_lotto(837)
#     result = am_i_lucky(your_numbers, win_numbers)
    
#     return render_template('result.html', result=result)


# @app.route("/lotto/pick")
# def pick():
#     your_numbers = pick_lotto()
#     win_numbers = get_lotto(837)
#     result = am_i_lucky(your_numbers, win_numbers)
#     return render_template('result.html', result=result)
    
    
@app.route("/self", methods=['POST'])
def self_data():
    round = request.form['round']
    item1 = request.form['item1']
    item2 = request.form['item2']
    item3 = request.form['item3']
    item4 = request.form['item4']
    item5 = request.form['item5']
    item6 = request.form['item6']
    
    judge_set = set([item1, item2, item3, item4, item5, item6])
    if len(judge_set) != 6:
        flash("번호를 중복되게 입력하셨습니다. 다시 입력해주세요!")
        return redirect(url_for('index'))
        
    else:
        your_numbers = [item1, item2, item3, item4, item5, item6]
        win_numbers = get_lotto(int(round))
        result = am_i_lucky(your_numbers, win_numbers)
        
        return render_template('result.html', result=result)


@app.route('/auto', methods=['POST'])
def auto_data():
    round = request.form['round']
    
    your_numbers = pick_lotto()
    win_numbers = get_lotto(int(round))
    result = am_i_lucky(your_numbers, win_numbers)
    return render_template('result.html', result=result)


@app.route('/telegram', methods=['POST'])
def telegram():
    result = request.form['result']
    id = request.form['ID']
    
    send_message(id, result)
    
    return redirect(url_for('index'))



## functions
def pick_lotto():
    numbers = list(range(1,46))
    my_numbers = random.sample(numbers, 6)
    my_numbers.sort()
    return my_numbers


def get_lotto(round):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}'.format(round)
    response = requests.get(url)
    lotto_data = response.json()

    real_numbers = []
    for key in lotto_data:
        if 'drwt' in key:
            real_numbers.append(lotto_data[key])

    real_numbers.sort()
    bonus_number = lotto_data['bnusNo']
    return {'real_numbers' : real_numbers, 'bonus_number' : bonus_number}


def am_i_lucky(my_numbers, win_numbers):
    my_numbers = set(my_numbers)
    real_numbers = set(win_numbers['real_numbers'])
    bonus_number = win_numbers['bonus_number']

    if len(my_numbers.intersection(real_numbers)) == 6:
        result = '축하합니다. 1등 입니다!'
    elif len(my_numbers.intersection(real_numbers)) == 5:
        if bonus_number in my_numbers:
            result = '축하합니다. 2등 입니다!'
        else:
            result = '축하합니다. 3등 입니다!'  
    elif len(my_numbers.intersection(real_numbers)) == 4:
        result = '축하합니다. 4등 입니다!'
    elif len(my_numbers.intersection(real_numbers)) == 3:
        result = '축하합니다. 5등 입니다!'
    elif len(my_numbers.intersection(real_numbers)) == 2:
        result = '축하합니다. 6등 입니다!'
    elif len(my_numbers.intersection(real_numbers)) == 1:
        result = '축하합니다. 7등 입니다!'
    else:
        result = '당첨되지 않았습니다. 다음에 도전해주세요!'

    return result
    
    
## server setting   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)