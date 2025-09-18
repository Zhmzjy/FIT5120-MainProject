FROM python:3.11-slim
WORKDIR /app
COPY app.py animal_details_top_animals.csv dictionary_questions_bool.csv ./
RUN pip install --no-cache-dir fastapi uvicorn pydantic
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
