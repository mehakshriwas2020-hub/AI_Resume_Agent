# AI Resume Screening System

## Project Overview
AI Resume Screening System is a Python-based application that automatically analyzes resumes and matches them with job descriptions. It extracts key skills, calculates ATS score, detects missing skills, and generates interview questions to help recruiters evaluate candidates efficiently.

## Features
- Resume PDF Upload and Processing
- Automatic Text Extraction from Resume
- Skill Extraction using NLP techniques
- ATS Score Calculation based on job description match
- Missing Skills Identification
- Interview Question Generation
- REST API built with FastAPI
- Swagger UI for API testing

## Tech Stack
- Python
- FastAPI
- pdfplumber
- NLP
- Uvicorn

## How to Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
