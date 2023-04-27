__SLACK_WEBHOOK_VERSION__=$(python3 setup.py --version)

SRC=deb_dist/${__SLACK_WEBHOOK_VERSION__}
DEST=~/www/bensokol.com/public/deb.bensokol.com/debian/pool/main/python3-slackwebhook/

GPG_KEY=1C6BFAD873C7B6D2241FEFDA2DBA02F97C909F11

echo "[sdist_dsc]" > ./setup.cfg
echo "compat: 10" >> ./setup.cfg
echo "dist-dir: ${SRC}" >> ./setup.cfg

python3 setup.py --command-packages=stdeb.command bdist_deb

debsign -k ${GPG_KEY} --re-sign ${SRC}/slackwebhook_1.0.7-1_amd64.changes
debsign -k ${GPG_KEY} --re-sign ${SRC}/slackwebhook_1.0.7-1_source.changes
debsign -k ${GPG_KEY} --re-sign ${SRC}/slackwebhook_1.0.7-1.dsc
#debsign -k 1C6BFAD873C7B6D2241FEFDA2DBA02F97C909F11 --re-sign ${SRC}/
debsigs --sign=origin -k ${GPG_KEY} ${SRC}/python3-slackwebhook_1.0.7-1_all.deb

mkdir -p ${DEST}
cp ${SRC}/*.deb  ${DEST}
cp ${SRC}/*.tar.xz ${DEST}
cp ${SRC}/*.tar.gz ${DEST}
cp ${SRC}/*.dsc ${DEST}
