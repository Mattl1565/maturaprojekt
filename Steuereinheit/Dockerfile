# Use the official Python image with Python 3.9 slim variant
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the sin.py file into the container
COPY graphische_steuerung.py .
COPY steuereinheit.py .
COPY json_commands_for_ai.py .
COPY GTA_Stuff/busted_sound_effect.wav .
COPY GTA_Stuff/gta5.ttf .

EXPOSE 80

# Specify the command to run on container start
CMD ["python", "./steuereinheit.py", "&&", "python", "./graphische_steuerung.py"]