from flask import Flask, render_template, request, jsonify
import os
from database import get_jobs, get_job_details, add_application_for_job

app = Flask("__name__")

@app.route("/")
def welcome():
    jobs = get_jobs()
    return render_template('home.html', jobs=jobs)

@app.route("/job/<int:job_id>")
def show_job(job_id):
    job = get_job_details(job_id)
    if job is None:
        return "Job not found", 404
    return render_template('jobpage.html', job=job)

@app.route("/apply/<int:job_id>" , methods=["post"])
def apply(job_id):
    # data = request.args # for GET request using query parameters
    # return jsonify({"message": "Application received", "data": data})   

    data = request.form # for POST request
    job = get_job_details(job_id)
    # try:
    add_application_for_job(job['id'], data)
    return render_template('application_submit.html', job=job, data=data)
    # except Exception as e:
    #     print("Error while adding application to database", str(e))
    #     return "There was an error while submitting your application. Please try again later.", 500
    

if __name__ == '__main__':
    app.run(debug=True)
