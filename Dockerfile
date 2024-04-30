# Use an official Python image as the base
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app
COPY --chown=node . /app

# Copy the requirements file
#COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME=Predictor

# Run predict.py when the container launches
#CMD ["python", "predict.py"]
ENTRYPOINT ["python", "predict.py"]