FROM rootproject/root-cc7

# labels
LABEL name="plotlib"

# variables
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/usr/local/lib"

# workdir
WORKDIR /root

# prepare yum
RUN yum -y update
RUN yum -y install yum-plugin-priorities yum-utils

# basic software
RUN yum -y groupinstall development
RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel
RUN yum -y install which wget nano screen git cmake cmake3 python-pip

# cleanup yum
RUN yum clean all

# python packages
RUN pip install six flake8

# micro editor
RUN cd /usr/bin && curl https://getmic.ro | bash
