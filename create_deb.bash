__SLACK_WEBHOOK_VERSION__=$(python3 setup.py --version)
__SLACK_WEBHOOK_DEBFILE__=python3-slackwebhook_${__SLACK_WEBHOOK_VERSION__}-1_all.deb

__APT_ROOT_LOCATION__=~/www/bensokol.com/public/deb.bensokol.com


python3 setup.py --command-packages=stdeb.command bdist_deb
cp deb_dist/${__SLACK_WEBHOOK_DEBFILE__} ${__APT_ROOT_LOCATION__}/pool/main/python3-slackwebhook/${__SLACK_WEBHOOK_DEBFILE__}

${__APT_ROOT_LOCATION__}/do_release.bash
