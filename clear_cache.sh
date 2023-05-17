#!/bin/bash

# clearing codes
for f in codes/*.py; do
  truncate -s 0 "$f"
done

# clearing response files and logs
truncate -s 0 bardcoder.log
truncate -s 0 response/content.md
truncate -s 0 response/response.json
