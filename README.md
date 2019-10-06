# u/datascience-bot

![Build Status](https://img.shields.io/travis/com/vogt4nick/datascience-bot/master)
![Last Deployment](https://img.shields.io/github/last-commit/vogt4nick/datascience-bot/master?label=last%20deployment)
![Count Bugs](https://img.shields.io/github/issues/vogt4nick/datascience-bot/bug?color=red)

[u/datascience-bot](https://reddit.com/user/datascience-bot) moderates [r/datascience](https://reddit.com/r/datascience). It automates a handful of tasks:

1. Removing spam submissions
2. Removing submissions from trolls
3. Redirecting common questions from new redditors
4. Updating the [wiki](https://reddit.com/r/datascience/wiki)
5. Facilitating the [weekly entering & transitioning thread](https://reddit.com/r/datascience/search?q=weekly%20thread&restrict_sr=1&sort=new)


## Deployment

Every `master` build of [u/datascience-bot](https://reddit.com/user/datascience-bot) is automatically deployed to AWS Lambda with Travis CI. AWS CloudWatch is manually configured (for now) to run behaviors periodically.


## Testing

[u/datascience-bot](https://reddit.com/user/datascience-bot) has a few friends to help test deployments on [r/datascience_bot_dev](https://reddit.com/r/datascience_bot_dev). They are [u/SubstantialStrain6](https://reddit.com/user/SubstantialStrain6) and [u/b3405920](https://reddit.com/user/b3405920).

## Collaboration

We're not currently encouraging open collaboration of u/datascience-bot, but we will in the near future!
