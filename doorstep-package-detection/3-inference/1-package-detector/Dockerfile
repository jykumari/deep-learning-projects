# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:l4t-pytorch

FROM nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx python3-opencv

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache -r requirements.txt coremltools gsutil 
RUN pip3 install paho-mqtt
RUN pip3 install --no-cache -U torch torchvision

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app

# Set environment variables
ENV HOME=/usr/src/app

CMD ["python3","package-detector.py"]


