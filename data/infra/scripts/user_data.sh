#!/bin/bash

log_file="/home/ubuntu/user_data_execution.log"
function log() {
    sep="----------------------------------------------------------"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $sep " | tee -a "$log_file"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "$log_file"
}

log "Starting user data script execution"

log "Updating packages"
apt-get update

log "Installing jq"
apt-get install -y jq

log "Installing s3cmd"
apt-get install -y s3cmd

log "Configuring s3cmd"
cat <<EOF > /home/ubuntu/.s3cfg
[default]
access_key = ${ACCESS_KEY}
secret_key = ${SECRET_KEY}
host_base = storage.yandexcloud.net
host_bucket = %(bucket)s.storage.yandexcloud.net
use_https = True
EOF

# chown ubuntu:ubuntu /home/ubuntu/.s3cfg
# chmod 600 /home/ubuntu/.s3cfg

log "Installing ffmpeg"
apt-get install -y ffmpeg

log "Installing python3-pip"
apt-get install -y python3-pip

log "Downloading data"
cd /home/ubuntu
RESPONSE=$(curl -X POST "${COMMON_VOICE_DATASET}" \
  -H "Authorization: Bearer ${COMMON_VOICE_API_KEY}" \
  -H "Content-Type: application/json")

DOWNLOAD_URL=$(echo $RESPONSE | jq -r '.downloadUrl')
curl -o common_voice.tar.gz "$DOWNLOAD_URL"

log "Extracting data"
tar -xzf common_voice.tar.gz

log "Creating dir 'manifests/'"
mkdir /home/ubuntu/manifests/

log "Installing pandas"
pip install pandas

log "Installing scikit-learn"
pip install scikit-learn

log "Installing boto3"
pip install boto3

log "Copying 'preprocess_data.py' script on virtual machine"
echo $'${preprocess_data_base64}' |  base64 -d > preprocess_data.py

log "Copying 'convert_data.py' script on virtual machine"
echo $'${convert_data_base64}' |  base64 -d > convert_data.py

# log "Fixing permissions"
# chown -R ubuntu:ubuntu /home/ubuntu/

log "Starting 'preprocess_data.py' script"
python3 preprocess_data.py

log "Starting 'convert_data.py' script"
S3_BUCKET=${S3_BUCKET} ACCESS_KEY=${ACCESS_KEY} SECRET_KEY=${SECRET_KEY} python3 convert_data.py

log "Copying manifests to S3"
s3cmd sync --config=/home/ubuntu/.s3cfg /home/ubuntu/manifests/ s3://${S3_BUCKET}/

log "Finished"
