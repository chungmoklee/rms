FROM python:2

MAINTAINER Chungmok Lee <chungmok@gmail.com>


# Install utilities
#RUN locale-gen en_US.UTF-8 && \
#    echo 'LANG="en_US.UTF-8"' > /etc/default/locale && \
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --force-yes \
        build-essential \
        software-properties-common \
        apt-transport-https \
        curl \
        wget \
        git \
        unzip \
        pwgen \
        netcat-openbsd

# Set environment variables
ENV HOME /root

# Define working directory
WORKDIR /scripts

# Define default command
#CMD ["bash"]

# Install and configure CouchDB 1.6.0
RUN DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y --force-yes \
    erlang-dev \
    erlang-manpages \
    erlang-base-hipe \
    erlang-eunit \
    erlang-nox \
    erlang-xmerl \
    erlang-inets \
    libmozjs185-dev \
    libicu-dev \
    libcurl4-gnutls-dev \
    libtool && \
    cd /tmp && \
    wget http://mirror.sdunix.com/apache/couchdb/source/1.6.0/apache-couchdb-1.6.0.tar.gz && \
    tar xzvf apache-couchdb-1.6.0.tar.gz && \
    cd apache-couchdb-1.6.0 && \
    ./configure && \
    make && \
    make install && \
#    sed -e 's/^bind_address = .*$/bind_address = 0.0.0.0/' -i /usr/local/etc/couchdb/default.ini && \
#    sed -e 's/^database_dir = .*$/database_dir = \/data/' -i /usr/local/etc/couchdb/default.ini && \
#    sed -e 's/^view_index_dir = .*$/view_index_dir = \/data/' -i /usr/local/etc/couchdb/default.ini && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD couchdb/default.ini /usr/local/etc/couchdb/

# Install InfluxDB
ENV INFLUXDB_VERSION 0.9.4.2
RUN curl -s -o /tmp/influxdb_latest_amd64.deb https://s3.amazonaws.com/influxdb/influxdb_${INFLUXDB_VERSION}_amd64.deb && \
  dpkg -i /tmp/influxdb_latest_amd64.deb && \
  rm /tmp/influxdb_latest_amd64.deb && \
  rm -rf /var/lib/apt/lists/*

# Add scripts
#ADD couchdb/scripts /scripts
ADD influxdb/run_influxdb.sh /scripts/run_influxdb.sh
RUN chmod +x /scripts/*.sh && \
    touch /.firstrun

ADD influxdb/types.db /usr/share/collectd/types.db
ADD influxdb/config.toml /config/config.toml

# Command to run
#ENTRYPOINT ["/scripts/run.sh"]
#CMD [""]

# Expose listen port (couchDB)
EXPOSE 5984

# Expose our data, logs and configuration volumes
VOLUME ["/data", "/usr/local/var/log", "/web_server"]



ENV PRE_CREATE_DB **None**
ENV SSL_SUPPORT **False**
ENV SSL_CERT **None**

# Admin server WebUI (influxDB)
EXPOSE 8083

# HTTP API (influxDB)
EXPOSE 8086

# Raft port (for clustering, don't expose publicly!)
#EXPOSE 8090

# Protobuf port (for clustering, don't expose publicly!)
#EXPOSE 8099



# Install redis
ENV REDIS_VERSION 2.6.17
ENV REDIS_DOWNLOAD_URL http://download.redis.io/releases/redis-2.6.17.tar.gz
ENV REDIS_DOWNLOAD_SHA1 b5423e1c423d502074cbd0b21bd4e820409d2003


RUN mkdir -p /redis \
    && curl -sSL "$REDIS_DOWNLOAD_URL" -o redis.tar.gz \
    && echo "$REDIS_DOWNLOAD_SHA1 *redis.tar.gz" | sha1sum -c - \
    && tar -xzf redis.tar.gz -C /redis --strip-components=1 \
    && rm redis.tar.gz \
    && make -C /redis \
    && make -C /redis install \
    && rm -r /redis 



# Install python libs
RUN pip install supervisor gevent gevent-socketio colorama anypubsub

ADD supervisord.conf /scripts/supervisord.conf


