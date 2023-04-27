__SLACK_WEBHOOK_VERSION__=$(python3 setup.py --version)

SRC_ROOT=deb_dist/${__SLACK_WEBHOOK_VERSION__}
APT_REPO_ROOT=~/www/bensokol.com/public/deb.bensokol.com

echo "[sdist_dsc]" > ./setup.cfg
echo "compat: 10" >> ./setup.cfg
echo "dist-dir: ${SRC_ROOT}" >> ./setup.cfg

SRC_DEB_FILE=${SRC_ROOT}/python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1_all.deb
SRC_ORG_TAR_XZ_FILE=${SRC_ROOT}/slackwebhook_${__SLACK_WEBHOOK_VERSION__}.orig.tar.gz
SRC_DEB_TAR_XZ_FILE=${SRC_ROOT}/slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1.debian.tar.xz
SRC_DSC_FILE=${SRC_ROOT}/slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1.dsc

DEST_DEB_FILE=${APT_REPO_ROOT}/pool/main/python3-slackwebhook/python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1_all.deb
DEST_ORG_TAR_XZ_FILE=${APT_REPO_ROOT}/pool/main/python3-slackwebhook/python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}.orig.tar.gz
DEST_DEB_TAR_XZ_FILE=${APT_REPO_ROOT}/pool/main/python3-slackwebhook/python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1.debian.tar.xz
DEST_DSC_FILE=${APT_REPO_ROOT}/pool/main/python3-slackwebhook/python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1.dsc

python3 setup.py build
python3 setup.py --command-packages=stdeb.command bdist_deb

#cp ${SRC_DEB_FILE}        ${DEST_DEB_FILE}
#cp ${SRC_ORG_TAR_XZ_FILE} ${DEST_ORG_TAR_XZ_FILE}
#cp ${SRC_DEB_TAR_XZ_FILE} ${DEST_DEB_TAR_XZ_FILE}
#cp ${SRC_DSC_FILE}        ${DEST_DSC_FILE}
