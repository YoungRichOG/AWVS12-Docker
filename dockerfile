FROM ubuntu:16.04
RUN mkdir /data
WORKDIR /data
ADD acunetix_trial.sh.zip .
ADD patch_awvs .
RUN apt-get update  -y
RUN apt-get install net-tools -y && \
	apt-get install python -y && \
	apt-get install python3 -y && \
	apt-get install unzip -y && \
	apt-get install libxdamage1 libgtk-3-0 libasound2 libnss3 libxss1 -y && \
	apt install bzip2 -y && \
	apt install vim -y && \
	apt-get install sudo -y
RUN unzip acunetix_trial.sh.zip
RUN chmod +x acunetix_trial.sh
RUN chmod +x patch_awvs
RUN sh -c '/bin/echo -e "\nyes\nubuntu\ntest123@gmail.com\ntest123!@#.\ntest123!@#.\n"| ./acunetix_trial.sh'