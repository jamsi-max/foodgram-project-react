server {
    listen ${LISTEN_PORT};
    server_name localhost;
    server_tokens off;

    location /staticfiles/ {
        alias /vol/static/;
    }

    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.html;
    }

    location /api/ {
        try_files $uri @proxy_api;
    }
    location /admin/ {
        try_files $uri @proxy_api;
    }
    location @proxy_api {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }

    location / {
        root /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri /index.html;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
      }
      error_page   500 502 503 504  /50x.html;
      location = /50x.html {
        root   /var/html/frontend/;
      }
}