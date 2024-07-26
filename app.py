from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def squarenumber():
    if request.method == 'GET':
        return render_template("squarenum.html")
    
    if request.method == 'POST':
        if(request.form["num"] == ''):
            return '<html><body><h1>Invalid Number</h1></body></html>'
        else:
            number = request.form["num"]
            sq = int(number) * int(number)
            return render_template("answer.html",squareofnum=sq,num=number)

@app.route("/mid",methods=['GET'])
def mid():
    return redirect(location="/kazu",code=403)

if __name__ == "__main__":
    
    app.run(debug=True)