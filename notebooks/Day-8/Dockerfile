# Base Image
FROM python:3.13.9

# Working Directory
WORKDIR /app

# Copy
COPY . /app/

# run
RUN pip install -r requirements.txt

# port
EXPOSE 5001

# Command
CMD ["python","./app.py"]