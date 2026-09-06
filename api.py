from flask import Flask, request, jsonify

# imports functions from db.py and generate.py. connect API to the project
from db import init_db, save_generation, get_generation, update_status
from generate import generate_ad_copy

# initalises the flask application instance
app = Flask(__name__)
init_db() # does nothing expect checks whether tables exist or no, if they dont it creates it

@app.post("/generate") # Tells to only run this function is something is sending or recieving data to this specific address.more readable that doing using @app.route(). create POST endpoint called /generate
def generate():
    data = request.get_json() #takes json sent by the user and turns it into a python dictionary
    brief = data.get("brief", "") # gets the purpose(brief)
    campaign_id = data.get("campaign_id",1) # gets campaign ID

# prevents the user from asking the AI to generate when they have not provided the brief
    if not brief.strip():
        return jsonify({"error": "Brief cannot be empty"}), 400

    prompt = f"Write 2 short Instagram ad captions for this brief:\n{brief}"

#issue face by the code at this point is its inability to gracefully handle unhandled errors when communicating with gemini
    try:
        result = generate_ad_copy(prompt)
    except Exception as e:
        return jsonify({"error": f"Generation failed: {e}"}), 502 # returns n error message instead of wondering what to do

    new_id = save_generation(campaign_id=campaign_id, text=result) # saves the generation made by gemini
    return jsonify({"id": new_id, "text": result}) # converts info into JSON and sends it back as the API

@app.post("/generations/<int:generation_id>/approve")
def approve(generation_id):
    update_status(generation_id, "approved")
    return jsonify({"id": generation_id, "status": "approved"})

@app.post("/generations/<int:generation_id>/reject")
def reject(generation_id):
    update_status(generation_id, "rejected")
    return jsonify({"id": generation_id, "status": "rejected"})

@app.post("/generations/<int:generation_id>/improve")
def improve(generation_id):
    data = request.get_json()
    original_text = data.get("original_text", "")
    instruction = data.get("instruction", "")
    campaign_id = data.get("campaign_id", 1)

    new_prompt = f"Revise this: {original_text}\nInstruction: {instruction}"
    try:
        new_result = generate_ad_copy(new_prompt)
    except Exception as e:
        return jsonify({"error": f"Improve failed: {e}"}), 502

    new_id = save_generation(campaign_id=campaign_id, text=new_result, parent_id=generation_id)
    return jsonify({"id": new_id, "text": new_result})