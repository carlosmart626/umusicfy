FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
RUN apt-get update && apt-get install -y openssl && apt-get upgrade -y
ADD sites-enabled/ /etc/nginx/sites-enabled
