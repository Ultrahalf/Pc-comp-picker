#!/bin/sh

for SCRAPE in $HOME/pccp/src/node/*
do
    node $SCRAPE >/dev/null 2>&1
done
