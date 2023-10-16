from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# import the model
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company = request.form['company']
        type = request.form['TypeName']
        ram_input = request.form.get('ram')

        try:
            ram = int(ram_input)
        except ValueError:
            # Handle the case where 'ram_input' is not a valid integer
            # For example, you can set a default value or show an error message
            ram = 0  # Set a default value or handle it according to your requirements

        weight = float(request.form['weight'])
        touchscreen_input = request.form.get('touchscreen')

        if touchscreen_input == 'Yes':
            touchscreen = 1
        elif touchscreen_input == 'No':
            touchscreen = 0
        else:
            # Handle the case where 'touchscreen_input' is neither 'Yes' nor 'No'
            # You can set a default value or show an error message
            touchscreen = 0  # Set a default value or handle it as needed

        ips_input = request.form.get('ips')

        if ips_input == 'Yes':
            ips = 1
        elif ips_input == 'No':
            ips = 0
        else:
            # Handle the case where 'ips_input' is neither 'Yes' nor 'No'
            # You can set a default value or show an error message
            ips = 0  # Set a default value or handle it as needed

        screen_size = float(request.form['screen_size'])
        resolution = request.form['screen_resolution']
        cpu = request.form['cpu']
        hdd = int(request.form['hdd'])
        ssd = int(request.form['ssd'])
        gpu = request.form['gpu']
        os = request.form['os']
        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])
        ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size
        query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os])
        query = query.reshape(1, 12)
        predicted_price = int(np.exp(pipe.predict(query)[0]))
        return render_template('result.html', predicted_price=predicted_price)

    return render_template('index.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)
