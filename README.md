# slack-webhook

Sends a message to a specified slack webhook



### Add source to APT
```bash
echo deb [signed-by=/etc/apt/trusted.gpg.d/bensokol.gpg] https://deb.bensokol.com/debian public main | sudo tee /etc/apt/sources.list.d/deb.bensokol.com.list
```

### Add key
```bash
curl https://deb.bensokol.com/public.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/bensokol.gpg
```

### Update and install
```bash
sudo apt update && sudo apt install python3-slackwebhook
```
