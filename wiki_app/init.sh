#!/bin/sh

echo "Fetching initial Wikipedia page..."

curl -s https://en.wikipedia.org/wiki/Kubernetes -o /usr/share/nginx/html/index.html

echo "Initial page fetched and saved."