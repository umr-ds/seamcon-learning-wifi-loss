FROM nvidia/cuda:9.1-cudnn7-devel

# Add some dependencies
RUN apt-get clean && apt-get update -y -qq
RUN apt-get install -y tmux htop curl git build-essential htop tmux

ENV CONDA_DOWNLOAD "Anaconda3-5.1.0-Linux-x86_64.sh"
ENV PATH="/anaconda3/bin:${PATH}"

RUN curl --silent -O https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
RUN bash Anaconda3-5.1.0-Linux-x86_64.sh -b -p /anaconda3

RUN conda update -n base conda
RUN conda install pygpu
RUN conda install tensorflow-gpu=1.4.1

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

USER root
EXPOSE 8888
WORKDIR /jupyter/

CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
