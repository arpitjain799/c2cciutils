FROM swift:5.7.1

RUN apt-get update
RUN apt-get --yes install build-essential git curl

WORKDIR /src
RUN git clone https://github.com/yonaskolb/Mint.git
WORKDIR /src/Mint
RUN swift run mint install yonaskolb/mint

#RUN swift package update
ENV PATH="/root/.mint/bin/:${PATH}"
#RUN find / -name mint&&false
#RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"
#RUN brew --version && \
#    /home/linuxbrew/.linuxbrew/bin/brew install mint
RUN mint --version && \
 mint install WeTransfer/GitBuddy
