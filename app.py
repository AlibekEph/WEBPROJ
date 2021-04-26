from flask import Flask, render_template, request, redirect, session, url_for, make_response, Response, json
from flask_sqlalchemy import SQLAlchemy
from data.member import Member

from random import randint

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u1081710_root:A5w9E7n4@localhost/u1081710_crypto'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'hfjajjAJFJSJHFSHFjs74jJSFJSFJJF942949HSFJSFSFKSFKFHS1714'


db = SQLAlchemy(application)






def randint_to(num=100):
    from time import sleep, time
    sleep(0.00000000000001)
    millis = int(round(time() * 10**32))
    random_int = millis % num + 1 

    return random_int



@application.route('/')
def about():
	return redirect('/info/')


@application.route('/info/')
def info():
	return render_template('info.html')

@application.route('/quiz/')
def quiz_default():
	return redirect('/quiz/0/')


correct_answers = ['2', '1', '3', '3', '4', '3', '2', '3', '2', '2']

answers = []


@application.route('/quiz/<int:id>/', methods=['GET', 'POST'])
def quiz(id):
	global answers
	if request.method == 'POST':
		if id==0:
			answers.append(request.form['name'])
			return redirect('/quiz/1/')
		if id > 0 and id < 10:
			answers.append(request.form['question'])
			print(answers)
			return redirect('/quiz/{}/'.format(id + 1))
		if id == 10:
			answers.append(request.form['question'])
			print(answers)
			return redirect('/quiz-result/')



	return render_template('quiz.html')


@application.route('/quiz-result/')
def quiz_result():
	global answers
	print(answers)
	name = answers[0]
	correct = 0
	mark = ''
	for i in range(1,len(answers)):
		if answers[i] == correct_answers[i-1]:
			correct += 1

	answers = []

	if correct <= 4:
		mark = 'Так не пойдет! Изучи материал, а потом проходи викторину'
	elif correct >=5 and correct <=8:
		mark = 'Неплохой результат! Но для идеала придется лучше изучить теорию на сайте'
	else:
		mark = 'Молодец! Ты отлично изучил теорию на сайте и успешно справился с викториной'

	member = Member(scores=correct, mark=mark, name=name)
	try:
		db.session.add(member)
		db.session.commit()
		return render_template('quiz-result.html', mark=mark, correct=correct)
	except:
		return 'error'


@application.route('/quiz-top/')
def quiz_top():
	members = Member.query.order_by(-(Member.scores)).all()
	return render_template('quiz-top.html', members=members)

@application.route('/caesar/', methods=['GET', 'POST'])
def caesar():
	e_final = ''
	d_final = ''
	if request.method == 'POST':
		if request.form['btn'] == 'Зашифровать':
			text = request.form['e_text'].upper()
			for symbol in text:
				key = int(request.form['e_key'])
				e_final += chr((ord(symbol) + key - 13)%26 + ord('A'))

		elif request.form['btn'] == 'Дешифровать':
			text = request.form['d_text'].upper()
			for symbol in text:
				key = int(request.form['d_key'])
				d_final += chr((ord(symbol) - key - 13)%26 + ord('A'))

		return render_template('caesar.html', e_final=e_final, d_final=d_final)

	return render_template('caesar.html')



@application.route('/at/', methods=['GET', 'POST'])
def at():
	e_final = ''
	d_final = ''
	e_key_final = ''
	if request.method == 'POST':
		if request.form['btn'] == 'Зашифровать':
			text = request.form['e_text']
			key = []
			for char in text:
				position = ord(char)
				change = randint_to(position)
				key.append(change)
				position -= change
				e_final += str(position) + ' '
			for i in key:
				e_key_final += str(i) + " "


		elif request.form['btn'] == 'Дешифровать':
			text = request.form['d_text'].split()
			key = request.form['d_key']
			key = list(map(int, key.split()))

			print(key, text)

			for i in range(0, len(text)):
				char = key[i] + int(text[i])
				d_final += chr(char)

		return render_template('at.html', e_final=e_final, e_key_final=e_key_final, d_final=d_final)

	return render_template('at.html')



@application.route('/xor/', methods=['GET', 'POST'])
def xor():
	e_final = ''
	d_final = ''
	if request.method == 'POST':
		if request.form['btn'] == 'Зашифровать':
			text = list(request.form['e_text'])
			key = int(request.form['e_key'])
			for symbol in range(len(text)):
				try: text[symbol] = chr(ord(text[symbol]) ^ int(key))
				except ValueError: text[symbol] = chr(ord(text[symbol]) ^ ord(key))

			e_final = "".join(text)

		elif request.form['btn'] == 'Дешифровать':
			text = list(request.form['d_text'])
			key = int(request.form['d_key'])
			for symbol in range(len(text)):
				try: text[symbol] = chr(ord(text[symbol]) ^ int(key))
				except ValueError: text[symbol] = chr(ord(text[symbol]) ^ ord(key))

			d_final = "".join(text)

		return render_template('xor.html', e_final=e_final, d_final=d_final)

	return render_template('xor.html')


@application.route('/replacement/', methods=['GET', 'POST'])
def replacement():
	e_final = ''
	d_final = ''

	keys={
		'a':['Q','1','!','`','Я','М','Ь','З'],
		'b':['W','2'],
		'c':['E','3','@'],
		'd':['R','4','#',':'],
		'e':['T','5','$',';','Ц','Е','Ш','Ж',',','ф','ч','ш'],
		'f':['Y','6'],
		'g':['U','7'],
		'h':['I','8','%','"','Ы','П'],
		'i':['O','9','^','/','Ч','И'],
		'j':['P'],
		'k':['A'],
		'l':['S','0','&','?'],
		'm':['D','*'],
		'n':['F','(','<','У','Н','Л'],
		'o':['G',')','>','В','Р','Б','Х'],
		'p':['H','-'],
		'q':['J'],
		'r':['K','_','|','С','Т','Щ'],
		's':['L','+','№','К','Г','Д'],
		't':['M','=','Й','А','О','Ю','Ъ','.','й'],
		'u':['N','[','Ф'],
		'v':['B'],
		'w':['V',']'],
		'x':['C'],
		'y':['X','{'],
		'z':['Z'],
		' ':['}']
	}

	if request.method == 'POST':

		if request.form['btn'] == 'Зашифровать':
			text = request.form['e_text']
			crypt = ""
			for i in text:
			    if i in keys:
			        lenght=len(keys[i])
			        crypt+=keys[i][randint(0,lenght-1)]
			e_final = crypt

		elif request.form['btn'] == 'Дешифровать':
			text = request.form['d_text']
			decrypt = ""
			for i in text:
			    for j in keys:
			       if i in keys[j]:
			        decrypt+=j
			d_final = decrypt

		return render_template('replacement.html', e_final=e_final, d_final=d_final)

	return render_template('replacement.html')



if __name__ == '__main__':
	application.secret_key = 'hfjajjAJFJSJHFSHFjs74jJSFJSFJJF942949HSFJSFSFKSFKFHS1714'
	application.run(debug=False)
