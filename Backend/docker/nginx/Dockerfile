FROM ubuntu:14.04

RUN apt-get update \
  && apt-get -y install nginx openssl

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/ssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/C=US/ST=New York/L=New York City/O=Caffee/OU=Backend/CN=159.203.6.35"

# Copy a configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
