FROM ubuntu:14.04

RUN apt-get update \
  && apt-get -y install nginx openssl

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

RUN mkdir /usr/share/nginx/html

COPY 4B85FA976333A604FF4AEECEE2062452.txt /usr/share/nginx/html/4B85FA976333A604FF4AEECEE2062452.txt

# Copy a configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
