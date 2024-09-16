FROM ubuntu:22.04

COPY . /app
WORKDIR /app

# Install system dependencies
RUN apt update
RUN apt install cron python3-venv supervisor python3-pip redis-server mariadb-server mariadb-client curl git -y
RUN pip install frappe-bench python-dotenv pexpect --no-input
RUN service mariadb start
RUN python3 mysql-init.py

# To prevent permission denied
RUN useradd -ms /bin/bash frappe-bench -u 1000
RUN chown frappe-bench /app

# Install NodeJS and NPM
RUN mkdir /usr/local/nvm
ENV NVM_DIR=/usr/local/nvm
ENV NODE_VERSION=v20.17.0
ENV PATH=${NVM_DIR}:$PATH
ENV PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && . "$NVM_DIR/bash_completion" \
    && nvm install $NODE_VERSION \ 
    && nvm use $NODE_VERSION \
    && node --version \
    && npm install -g yarn

# Verify NodeJS and NPM is installed
RUN npm --version
RUN node --version

USER frappe-bench