from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Cimbom68'


    koz1=[]
    koz2=[]
    koz3=[]
    koz4=[]
    harf1 = []
    harf2 = []
    harf3 = []
    dict2 = {}


    # Load words once, globally
    my_file = open("sgb-words.txt", "r")
    content = my_file.read()
    words = content.split("\n")
    my_file.close()
    words.sort()
    words.pop(0)


    @app.route('/')
    def index():
        my_file = open("sgb-words.txt", "r")
        content = my_file.read()
        words = content.split("\n")
        my_file.close()
        words.sort()
        words.pop(0)
        session.clear()
        session.pop('remaining_words', None)
        session.pop('previous_guesses', None)
        session.pop('feedback', None)

        guess = random.choice(words)
        session['guess'] = guess

        return render_template('index.html', guess=guess)

    @app.route('/solve', methods=['POST'])
    def solve():
        my_file = open("sgb-words.txt", "r")
        content = my_file.read()
        words = content.split("\n")
        my_file.close()
        words.sort()
        words.pop(0)
        feedback = [request.form[f'feedback{i}'] for i in range(5)]
        guess = session.get('guess')
        action = request.form.get('action')


        if action == 'win':  # Win
            return render_template('win.html', history=session.get('history', [])[-5:], winner=guess)

        elif action == 'quit':  # Quit
            return render_template('quit.html', history=session.get('history', [])[-5:])
        elif action == 'new_game':  # New Game
            session.clear()
            return redirect(url_for('new_session'))

        
        else:
            if 'history' not in session:
                session['history'] = []
            session['history'].append((guess, feedback))

            j = 0
            while (j < 5):
                if feedback[j].lower() == 'g':
                    n = 0
                    koz1=[]
                    while (n < len(words)):
                        if guess[j] == words[n][j]:
                            koz1.append(words[n])
                            harf1.append(guess[j])
                        n=n+1
                    words = koz1
                if feedback[j].lower() == 'y':
                    m = 0
                    koz2=[]
                    while (m < len(words)):
                        if guess[j] in words[m]:
                            koz2.append(words[m])
                            harf2.append(guess[j])
                            dict2[guess[j]]=j
                        m=m+1
                    words = koz2
                if feedback[j].lower() == "b":
                    k=0
                    koz=[]
                    while(k < len(words)):
                        if words[k].count(guess[j]) > 1:
                            if (guess[j] not in harf1) or (guess[j] not in harf2):
                                koz.append(words[k])
                            k += 1
                            continue
                        if (guess[j] in words[k]) and (guess[j] not in harf1) and (guess[j] not in harf2):
                            koz.append(words[k])
                        k=k+1
                    for eleman in koz:
                        aa=words.index(eleman)
                        words.pop(aa)
                words.sort()
                j=j+1
            if guess in words:
                a = words.index(guess)
                words.pop(a)
            words.sort()
            for kelime in words:
                if words.count(kelime)>1:
                    a=words.index(kelime)
                    words.pop(a)
            for kk, vv in dict2.items():
                for kelime in words[:]:  # Use a slice to iterate over a copy of the list
                    if (kk in kelime) and (vv == kelime.index(kk)):
                        koz4.append(kelime)

            for unsur in koz4:
                if unsur in words:
                    words.remove(unsur)  # Remove directly instead of using index


            if words == []:
                return render_template('index.html', guess="No valid words found. Please check your feedback.")
            
        
            guess = random.choice(words)
            session['guess'] = guess
            return render_template('index.html', guess=guess, history=session.get('history', [])[-5:])
    
    @app.route('/new_session')
    def new_session():
        session.clear()
        return render_template('new.html')

    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

