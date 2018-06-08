FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y git wget python-pip python-dev build-essential && \
    python -m pip install --upgrade pip && \
    python-tk && \
    pip install numpy==1.11.2 && \
    pip install cython==0.25.2 && \
    pip install EQcorrscan==0.1.6 && \
    pip install librosa==0.4.3 && \
    pip install matplotlib==1.5.3 && \
    pip install obspy==1.0.2 && \
    pip install pytest==2.8.7 && \
    pip install -e git+https://github.com/gem/oq-hazardlib.git@589fa31ddca3697e6b167082136dc0174a77bc16#egg=openquake.hazardlib && \
    pip install pandas==0.19.0 && \
    pip install protobuf==3.0.0 && \
    pip install scikit-image==0.12.3 && \
    pip install scikit-learn==0.18 && \
    pip install scipy==0.18.1 && \
    pip install seaborn==0.7.1 && \
    pip install setproctitle==1.1.10 && \
    pip install tensorflow==0.12.0 && \
    pip install terminado==0.6 && \
    pip install python-tk && \
    pip install tqdm==4.9.0
