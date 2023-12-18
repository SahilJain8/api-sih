from flask import Flask, json, request
import requests
import polyline

app = Flask(__name__)


@app.route('/handle_post', methods=['POST'])
def data():
    if request.method == 'POST':
        start = request.form['origin']
        end = request.form['destination']
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

            return_list.append(points[0])
        return return_list


if __name__ == "__main__":
    app.run()
