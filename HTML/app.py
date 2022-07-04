import header
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('mainpage.html')

# @app.route('/')
# def student():
#    return render_template('addrbook.html')

@app.route("/simpleSearch")
def simple():
    return render_template('simple.html')

@app.route("/AdvancedSearch")
def advanced():
    return render_template('advanced.html')

@app.route("/AppleSearch")
def apple():
    return render_template('apple.html')


@app.route('/simpleresult',methods = ['POST', 'GET'])
def result1():
   if request.method == 'POST':
      val = request.form #name을 통해 submit한 값들을 val 객체로 전달
      return render_template("simpleresult.html",result = val) #name은 key, name에 저장된 값은 value
  
@app.route('/advancedresult',methods = ['POST', 'GET'])
def result2():
   if request.method == 'POST':
        val = request.form
        keywords = request.form['Keywords']
        Inventor = request.form['Inventor']
        assignee = request.form['assignee']
        country = request.form['country']
        df2 = header.detail_search(keywords, Inventor, assignee, country)
        return render_template("advancedresult.html",result = val)
        #접근하는법 
        # return f'keywords = {keywords}Inventor = {Inventor}assignee = {assignee}country = {country}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80, debug = True)
