from flask import Flask, request
import requests
import polyline
import json
import datetime
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://sahil:gZrTSwnfaex5I2IE@hackton.u1vq7f7.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

app = Flask(__name__)

@app.route('/handle_post', methods=['POST'])
def data():
    if request.method == 'POST':
        start = request.form['origin']
        end = request.form['destination']
        
        url = f"https://maps.googleapis.com/maps/api/directions/json?destination={end}&origin={start}&key=AIzaSyAKObdT8TzL9VA1ipksnhtkFFVm_qS_XTI&model=bus"
        response = requests.get(url)
        response_dict = json.loads(response.text)
      
        polyline_points = []
        for route in response_dict['routes']:
            for step in route['legs'][0]['steps']:
                if 'polyline' in step:
                    polyline_points.append(step['polyline']['points'])
        
        return_list = []
        max_points = 1000
        current_points = 0
        
        for data in polyline_points:
     
            points = polyline.decode(data)
            for i in range(len(points)):
                if current_points < max_points:
                    print(return_list)
                    return_list.append(points[i][0])
                    return_list.append(points[i][1])
                    current_points += 1
                else:
                    break
            if current_points >= max_points:
                break
        
        # return_list.append(float(driv_loc_lat))
        # return_list.append(float(driv_loc_long))
        
        return return_list



@app.route("/")
def home():
    return "hello"


@app.route("/driver_data", methods=['POST'])
def driver_data():
    if request.method == 'POST':
        driv_loc_lat = request.form['driver_loc_lat']
        driv_loc_long = request.form['driver_loc_long']
        

        data = {"driv_loc_lat":driv_loc_lat,
                "driv_loc_long": driv_loc_long ,
                   "date": datetime.datetime.now(tz=datetime.timezone.utc) }
        
        print(data)
        
        db = client["sih"]
        collection = db["driver_data"]

        post_id = collection.insert_one(data)
        print(post_id)

        if post_id:
            return "ok"
        else:
            return "error"
    


@app.route("/get_driver_data")
def get_data():
    db = client["sih"]
    co_ordinates = []
    collection = db["driver_data"]
    cursor = collection.find({})
    for data in cursor:
     
        co_ordinates.append(data['driv_loc_lat'])
        co_ordinates.append(data['driv_loc_long'])

    return co_ordinates[-2:]





if __name__ == "__main__":
    app.run()
