FROM alpine:3.20 AS build
COPY Part_3/mini_server.c /mini_server.c
RUN apk add build-base fcgi-dev \
 && gcc /mini_server.c -o /mini_server -lfcgi

FROM nginx:alpine
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /mini_server /mini_server
RUN apk add spawn-fcgi fcgi
EXPOSE 80
CMD spawn-fcgi -p 8080 -- /mini_server && nginx -g 'daemon off;'