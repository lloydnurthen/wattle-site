# wattle-site

The public site at **https://wattle.nurthen.au**, served by GitHub Pages.

It exists mainly because Tesla needs wattle's public key at a public address. Everything
else about wattle is private (`lloydnurthen/wattle`). The full rules are in
`docs/public-site.md` and decision 0005 in that repository.

| Path | What it is | Change it? |
| --- | --- | --- |
| `/` | Holding page | Freely |
| `/.well-known/appspecific/com.tesla.3p.public-key.pem` | Tesla public key | **Never**, unless re-registering with Tesla |
| `/auth/callback/` | Where Tesla sends people after sign-in | Only with the app's sign-in code |
| `CNAME` | Tells GitHub Pages the address | No |
| `.nojekyll` | Stops GitHub Pages hiding `.well-known` | Never remove |

This repository is public. Only public things go in it: never the private key, tokens or secrets.
