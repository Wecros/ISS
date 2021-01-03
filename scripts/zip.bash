#!/usr/bin/env bash

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/28
# Details: Zip the project, ready to be turned in.

# Set the script's location as the pwd
cd "$(dirname "$0")" || exit 1
cd .. # Project's root folder

tar -czf xfilip46.tar.gz src/ audio/
