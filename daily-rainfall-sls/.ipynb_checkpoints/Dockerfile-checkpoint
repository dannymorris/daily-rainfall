# Start with Python 3.7 image which replicates the Lambda environment
FROM lambci/lambda:build-python3.8

# Create a virtual env
ENV VIRTUAL_ENV=venv
ENV PATH $VIRTUAL_ENV/bin:$PATH
RUN python3 -m venv $VIRTUAL_ENV

# Install Python packages using pip
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy function code to the image
WORKDIR /var/task/venv/lib/python3.8/site-packages
COPY stations.py .
COPY hourly.py .

# Zip the deployment package
RUN zip -9qr daily-rainfall-sls.zip *