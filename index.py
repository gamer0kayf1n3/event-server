from flask import Flask, jsonify, request, render_template
import json
import datetime

app = Flask(__name__)

@app.route('/api/set', methods=['POST'])
def set_event():
    data = request.form
    print(data)
    title = data['title']
    description = data['description']
    expire_date = datetime.datetime.strptime(data['expire_date'], '%Y-%m-%d %H:%M:%S')
    event = {'title': title, 'description': description, 'expire_date': expire_date.isoformat()}
    with open('events.json', 'r') as f:
        events = json.load(f)
    events.append(event)
    with open('events.json', 'w') as f:
        json.dump(events, f)
    return jsonify({'message': 'Event set successfully'})

@app.route('/', methods=['GET'])
def dashboard():
    current_time = datetime.datetime.now()
    with open('events.json', 'r') as f:
        events = json.load(f)
    upcoming_events = [event for event in events if datetime.datetime.fromisoformat(event['expire_date']) > current_time]
    return render_template('dashboard.html', upcoming_events=upcoming_events)

@app.route('/add', methods=['GET'])
def add_event():
    return render_template('add_event.html')

if __name__ == '__main__':
    app.run(debug=True)
