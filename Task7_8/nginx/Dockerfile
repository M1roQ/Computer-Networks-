# 1) Build-stage: собираем динамический модуль
ARG NGINX_VERSION=1.24.0
FROM nginx:${NGINX_VERSION}-alpine AS builder

RUN apk add --no-cache \
      build-base \
      pcre-dev \
      zlib-dev \
      libmaxminddb-dev \
      git \
      wget \
  && wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
  && tar zxvf nginx-${NGINX_VERSION}.tar.gz \
  && git clone --depth 1 https://github.com/leev/ngx_http_geoip2_module.git /geoip2 \
  && cd nginx-${NGINX_VERSION} \
  && ./configure --with-compat --add-dynamic-module=/geoip2 \
  && make modules

# 2) Final-stage: собираем минимальный образ с NGiNX + GeoIP2
FROM nginx:${NGINX_VERSION}-alpine

# Устанавливаем библиотеку libmaxminddb (runtime)
RUN apk add --no-cache libmaxminddb  # ← сюда попадает libmaxminddb.so.0 :contentReference[oaicite:0]{index=0}

# Куда NGINX по умолчанию смотрит на динамические модули
RUN mkdir -p /etc/nginx/modules

# Копируем собранный модуль в правильный каталог
COPY --from=builder /nginx-${NGINX_VERSION}/objs/ngx_http_geoip2_module.so \
     /etc/nginx/modules/

# Копируем конфиг и статику
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
