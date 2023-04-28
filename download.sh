# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the GNU General Public License version 3.

PRESIGNED_URL="https://dobf1k6cxlizq.cloudfront.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kb2JmMWs2Y3hsaXpxLmNsb3VkZnJvbnQubmV0LyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2ODM4MzkwOTV9fX1dfQ__&Signature=E2uOP8grn9oltbx1eXuxtSqKQJD-vW7-zkt~ZEYgGvXoWY1RQqqQF3OD6lGUo7Z0fbPPJuvBDWJf4HWHSPM2twxeK2dS4JKM6BAwylzmRwTfe0Ek8hC68NHcIhJbWsFgHXThYM~4YtQDNKoKaw23VjO3DyefgDpqEy-gcMNcE-WUxS0SczIWKJC4NcdI60RpeiPDoy4q1RW~UgryFVgAYY3rs5zAuKftLknHUZOhlPFth968x7k~PeX7iGv8xPkBLkkPTONFN53KchhGfueFQvCmeQgD51iYTgtQJTS2zn5oVYe4xZOoSBlZtpAmxc3YsvQbal-4AgcC9kXsom9qVA__&Key-Pair-Id=K231VYXPC1TA1R"             # replace with presigned url from email
MODEL_SIZE="7"  # edit this list with the model sizes you wish to download
TARGET_FOLDER="models"             # where all files should end up


declare -A N_SHARD_DICT

N_SHARD_DICT["7"]="0"
N_SHARD_DICT["13"]="1"
N_SHARD_DICT["30"]="3"
N_SHARD_DICT["65"]="7"

echo "Downloading tokenizer"
wget ${PRESIGNED_URL/'*'/"tokenizer.model"} -O ${TARGET_FOLDER}"/tokenizer.model"
wget ${PRESIGNED_URL/'*'/"tokenizer_checklist.chk"} -O ${TARGET_FOLDER}"/tokenizer_checklist.chk"

(cd ${TARGET_FOLDER} && md5 tokenizer_checklist.chk)

for i in ${MODEL_SIZE//,/ }
do
    echo "Downloading ${i}B"
    mkdir -p ${TARGET_FOLDER}"/${i}B"
    for s in $(seq -f "0%g" 0 ${N_SHARD_DICT[$i]})
    do
        echo "Downloading shard ${s}"
        wget ${PRESIGNED_URL/'*'/"${i}B/consolidated.${s}.pth"} -O ${TARGET_FOLDER}"/${i}B/consolidated.${s}.pth"
    done
    wget ${PRESIGNED_URL/'*'/"${i}B/params.json"} -O ${TARGET_FOLDER}"/${i}B/params.json"
    wget ${PRESIGNED_URL/'*'/"${i}B/checklist.chk"} -O ${TARGET_FOLDER}"/${i}B/checklist.chk"
    echo "Checking checksums"
    (cd ${TARGET_FOLDER}"/${i}B" && md5 checklist.chk)
done
