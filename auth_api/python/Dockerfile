FROM python:3

# Add your instructions to dockerize the application

# Define present directory
WORKDIR /python
# Copy files from directory 
COPY api.py /python/api.py
COPY methods.py /python/methods.py
COPY requirements.txt /python/requirements.txt
# Specify script
ADD . /python/methods.py
ADD . /python/api.py
# Imports
RUN pip install -r /python/requirements.txt
# Define command to start container
CMD ["python", "api.py"]
