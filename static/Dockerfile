FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN apt install sudo
# RUN apt install nano
# RUN pip3 install Flask
# RUN pip3 install passlib
# RUN pip3 install six
# RUN pip3 install pam

WORKDIR /usr/app/src
COPY . .


RUN pip3 install -r requirements.txt

EXPOSE 5000

RUN useradd -m -s /bin/bash -p $(openssl passwd -6 1234) user1
RUN useradd -m -s /bin/bash -p $(openssl passwd -6 1234) user2

RUN usermod -aG sudo user1
RUN usermod -aG sudo user2

RUN chmod -R 755 /home/user1
RUN chmod -R 755 /home/user2

WORKDIR /home/user1

RUN touch a1.txt
RUN touch b1.sh
RUN mkdir dir1
RUN touch dir1/a2.sh
RUN touch dir1/b2.txt
RUN mkdir dir2
RUN mkdir dir2/dir3
RUN touch dir2/dir3/a3.sh
RUN touch dir2/dir3/b3.txt

WORKDIR /usr/app/src
