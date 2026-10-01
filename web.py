from flask import Flask, render_template, jsonify, request
import subprocess
import json
import os

app = Flask(__name__)
CONFIG_FILE = "config.json"

def load_config():
    """Load button configuration."""
    if not os.path.exists(CONFIG_FILE):
        return {"groups": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", title=config.get("title", 'control'), groups=config.get("groups", []))

@app.route("/run", methods=["POST"])
def run_command():
    """Run a command sent from the frontend."""
    data = request.get_json()
    command = data.get("command")
    result = data.get("result",0)
    
    #print(command)

    if 'ssh' in command: command=command.replace('&&','\\&\\&')    
    #print(command)    

    try:
        pp=subprocess.Popen(command, shell=True,stdin=subprocess.PIPE, stdout = subprocess.PIPE)
        if result: 
            r,e=pp.communicate()
            r=r.decode().strip()
            if ':' in r: r=r.split(':')[-1]
            elif r=='0': r='off'
            elif r=='1': r='on'
            return jsonify({"status": "ok", "message": r.strip()})            
        else: return jsonify({"status": "ok", "message": f"Command '{command}' executed."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
