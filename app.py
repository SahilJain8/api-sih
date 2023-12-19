from flask import Flask, request
import requests
import polyline
import json

app = Flask(__name__)


@app.route('/handle_post', methods=['POST'])
def data():
    if request.method == 'POST':
        start = request.form['origin']
        end = request.form['destination']
        driv_loc_lat = request.form['driver_loc_lat']
        driv_loc_long = request.form['driver_loc_long']
        url = f"https://maps.googleapis.com/maps/api/directions/json?destination={end}e&origin={start}&key=AIzaSyAKObdT8TzL9VA1ipksnhtkFFVm_qS_XTI&model=bus"
        response = requests.get(url)
        response_dict = json.loads(response.text)
        polyline_points = []
        for route in response_dict['routes']:
            for step in route['legs'][0]['steps']:
                if 'polyline' in step:
                    polyline_points.append(step['polyline']['points'])
        return_list = []
        for data in polyline_points:
            points = polyline.decode(data)
            for i in range(len(points)):
                return_list.append(points[i][0])
                return_list.append(points[i][1])
      
        return_list.append(float(driv_loc_lat))
        return_list.append(float(driv_loc_long))
        return return_list


@app.route("/")
def home():
    return "hello"



if __name__ == "__main__":
    app.run()
