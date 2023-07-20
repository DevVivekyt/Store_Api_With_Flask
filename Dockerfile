FROM python:3.11
# EXPOSE 5000 For Docker use
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"] For Development server
CMD ["gunicorn" "--bind" ,"0.0.0.0:80", "app:create_app()"]