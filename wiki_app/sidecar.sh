#!/bin/sh

while true; do

  sleep_time=$(( (RANDOM % 11 + 5) * 60 ))

  echo "Sleeping for $sleep_time seconds..."
  sleep $sleep_time

  echo "Fetching random Wikipedia page..."
  curl -s -L https://en.wikipedia.org/wiki/Special:Random -o /usr/share/nginx/html/index.html

  echo "Random page fetched and saved as index.html."
done