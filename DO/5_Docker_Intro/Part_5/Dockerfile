FROM alpine:3.20 AS build
COPY Part_3/mini_server.c /mini_server.c
RUN apk add --no-cache build-base fcgi-dev \
 && gcc /mini_server.c -o /mini_server -lfcgi

FROM alpine:3.20
RUN apk add --no-cache nginx spawn-fcgi fcgi
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /mini_server /mini_server
EXPOSE 81
USER nginx
CMD spawn-fcgi -p 8080 -- /mini_server && nginx -g 'daemon off;'


