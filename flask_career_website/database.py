from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv  

load_dotenv()  # take environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")  # get the DATABASE_URL from environment variables
engine = create_engine(DATABASE_URL) 

def get_jobs():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs")).mappings() 
        data = [dict(row) for row in result]
        # print(data)    
        return data

def get_job_details(job_id):
    with engine.connect() as conn:
        sql_stmt = text("select * from jobs where id = :job_id")
        result = conn.execute(sql_stmt, {"job_id": job_id}).mappings().one_or_none()
        if result:
            return dict(result)
        else:
            return None
        

def add_application_for_job(job_id, data):
    with engine.connect() as conn:
        sql_stmt = text("insert into applications (job_id, full_name, email, linkedin_url, work_experience, education, resume_url) values (:job_id, :name, :email, :linkedin_url, :work_experience, :education, :resume_url)")
        conn.execute(sql_stmt, {"job_id": job_id, "name": data['name'], "email": data['email'], "linkedin_url": data['linkedIn'], "work_experience": data['work_experience'], "education": data['education'], "resume_url": data['resume']})  

        conn.commit()