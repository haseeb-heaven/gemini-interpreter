#!/bin/bash

for f in codes/*.py; do
  truncate -s 0 "$f"
done

truncate -s 0 bardcoder.log
