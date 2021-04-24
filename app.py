from flask import Flask, request, render_template
import pickle
import calendar

app = Flask(__name__)
model=pickle.load(open('dermodel.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    features = [(x) for x in request.form.values()]
    count=1
    if len(features[0])!=10 or features[0][4]!='/' or features[0][7]!='/':
        return render_template('index.html',prediction_text='Please input date in the format YYYY/MM/DD')
    
    int_features = features[0].replace('/','')
    check = int(int_features[0:4])
    if check<1999:
        return render_template('index.html',prediction_text='Pediction is available from the year 1999')
    
    thirtyone=['01','03','05','07','08','10','12']
    thirty=['04','06','09','11']
    dates=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    
    if int_features[4:6] not in dates[:12]:
        return render_template('index.html',prediction_text='Invalid Date')
    
    if int_features[4:6] in thirtyone and int_features[6:] not in dates:
        return render_template('index.html',prediction_text='Invalid Date')
    
    if int_features[4:6] in thirty and int_features[6:] not in dates[:-1]:
        return render_template('index.html',prediction_text='Invalid Date')
    
    if int_features[4:6]=='02':
        if calendar.isleap(int(int_features[:4])) and int_features[6:] not in dates[:-2]:
            return render_template('index.html',prediction_text='Invalid Date')
        if not calendar.isleap(int(int_features[:4])) and int_features[6:] not in dates[:-3]:
            return render_template('index.html',prediction_text='Invalid Date')
    
    
    if check>2020:
        count=check-2020
        int_features = int(int_features)
        prediction=model.predict([[int_features]])
        prediction-=(2.2*count)
        prediction=str(prediction)
        return render_template('index.html', prediction_text='The estimated value on '+features[0]+' is ₹ {}'.format(prediction[2:-2]))

    if check<2009:
        count=2009-check
        int_features = int(int_features)
        prediction=model.predict([[int_features]])
        prediction+=(2.7*count)
        prediction=str(prediction)
        return render_template('index.html', prediction_text='The estimated value on '+features[0]+' is ₹ {}'.format(prediction[2:-2]))
    if 2010<=check<=2020:
        int_features = int(int_features)
        prediction=model.predict([[int_features]])
        prediction=str(prediction)
        return render_template('index.html', prediction_text='The estimated value on '+features[0]+' is ₹ {}'.format(prediction[2:-2]))
    
    return render_template('index.html',prediction_text='Invalid Date')
    
if __name__ == "__main__":
    app.run(debug=True)