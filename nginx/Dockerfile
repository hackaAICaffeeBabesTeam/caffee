FROM ubuntu:14.04

RUN apt-get update \
  && apt-get -y install nginx openssl

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/ssl
COPY ssl-bundle.crt /etc/nginx/ssl/ssl-bundle.crt
COPY caffee.tech.key /etc/nginx/ssl/caffee.tech.key


# Copy a configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
