# Crypto Bot

## Overview

A bot that scrappes tradingview.com website and give you insights about BitCoin and Ethereum

This chat-bot is written in Python and uses selenium, chrome-headless and beautiful soup to scrappe tradingview web page looking for insights and tips of when buy or sell crypto coins.

## Pre Reqs

- Docker
- [Telegram Bot Token](https://core.telegram.org/bots)
- Docker Compose

## Running the project

1. Clone the project locally

2. Change the `docker-compose.yaml` as described below

With docker-compose you are able to run the project locally, just follow the steps.

```yaml
version: '3.3'
services:
  bot:
      build: .
      networks:
        - project-network
      restart: always
      environment:
        TELEGRAM_TOKEN: "<FILL_WITH_YOUR_TOKEN>"
networks:
  project-network:
    driver: bridge
```

Change the value of `TELEGRAM_TOKEN` with you bot user token that you generated before.

3. Execute `docker-compose up`

## ToDo List

- [ ] Add option for more coins
- [ ] Create CloudFormation to provision the environment on AWS
- [ ] Change to a remote Database
- [ ] Send automatic insight about coins

## License

The source code for the site is licensed under the MIT license.
