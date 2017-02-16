FROM nginx:latest

RUN sed -i 's/user  nginx;/user root;/' /etc/nginx/nginx.conf \
	&& sed -i 's/\/var\/log\/nginx\/access.log  main/off/' /etc/nginx/nginx.conf

COPY ./api.conf /etc/nginx/conf.d/default.conf
