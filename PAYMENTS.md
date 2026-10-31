# Turning payment on

The card form is already built. It is Paddle's own form, and it opens **inside
the site** — pressing a plan opens a dialog with real card fields in it, nobody
is sent off to another website, and no server of ours is involved.

What is missing is not code. It is an account that is allowed to take money.
**Nothing anyone writes can skip that part:** a card can only be charged by a
registered merchant, and registering means giving a real name, address, ID and
bank details and waiting for a human to approve it. Everything below is that
account, and the two values you copy out of it.

**Until you paste a token the app is in open mode:** nothing is locked, no
upsell appears anywhere, `paddle.js` is never even downloaded, and the pricing
section says plainly that payment is not open yet. Nobody loses anything while
you take your time.

---

## 1. Open a Paddle account

<https://paddle.com> → *Get started*. Paddle is the right one here for three
reasons:

- It is **merchant of record**. Paddle sells to the customer, not you, so VAT in
  every country is their problem, not yours.
- You can register **as an individual**, without a company.
- Its checkout can run **inside your own page** with no server. That is the
  whole reason the app is written against it. (Stripe cannot: its no-server
  options send the buyer to a Stripe page, and its in-page card fields need a
  secret key on a server, which a GitHub Pages site does not have.)

Approval is manual and takes a few days. They will ask for identification and
for a bank account. Sandbox (step 5) works immediately, so you can test the
whole flow while you wait.

## 2. Create the product and the two prices

In Paddle: **Catalog → Products → New product**.

1. Name it *Proactivity Pro*.
2. Add two **prices** to it:
   - **monthly**, recurring every 1 month
   - **annual**, recurring every 1 year
3. Copy the **price ID** of each. They look like `pri_01h4k...`.

> **Make the amounts match the page.** The app shows ₪19/month and ₪149/year
> (and $4.99 / $39, €4.99 / €39, ₽399 / ₽2990). Those numbers live in `PRICES`
> in `tools/js_app.py`. Set the Paddle prices to exactly the same amounts, or
> change `PRICES` to match what you set. A page that advertises one price and
> charges another is the one mistake here that is not recoverable with an
> apology.

## 3. Get the client-side token

**Developer tools → Authentication → Client-side tokens → New token.**

Copy it. It starts with `live_` (or `test_` in sandbox).

This token is meant to be published in front-end code: it can start a checkout
and nothing else — it cannot read your account, your customers or your money.
That is why it can live in a public repository. The **API key** on that same
screen is the opposite: it is a secret, it has no business being in a web page,
and nothing in this app ever asks for it.

## 4. Set the payment link and get the domain approved

Two settings, both under **Checkout** in Paddle:

1. **Checkout settings → Default payment link** → set it to
   `https://karentti-cpu.github.io/proactivity/`.
2. **Request domain approval** → add that same domain.

Paddle only opens its checkout on a domain it has approved, and the symptom when
it has not is a dialog that opens and stays empty. On **sandbox this is
automatic**, so step 6 works straight away; the live domain is reviewed, which
is another reason to ask for it early rather than on launch day.

## 5. Paste three values

Open **`tools/js_pro.py`**. The block is at the very top:

```js
var BILLING={
  provider:'paddle',
  token:'',
  env:'production',
  prices:{monthly:'', annual:''},
  portal:'',
  licProvider:''
};
```

Fill it in:

```js
var BILLING={
  provider:'paddle',
  token:'live_xxxxxxxxxxxxxxxxxxxxxxx',
  env:'production',
  prices:{monthly:'pri_01aaaaaaaaaa', annual:'pri_01bbbbbbbbbb'},
  portal:'',
  licProvider:''
};
```

Then rebuild and push:

```
python3 tools/build.py
git add -A && git commit -m "Turn payment on" && git push
```

GitHub Pages redeploys in a minute or two. That is the whole switch.

## 6. Test it in sandbox first

Do this before the live account is even approved.

1. Register at <https://sandbox-vendors.paddle.com> — a separate, free account.
2. Repeat steps 2–4 there. The token starts with `test_`.
3. Set `token` to that `test_...` and **`env:'sandbox'`**, then rebuild and open
   the site locally (`python3 -m http.server` and visit
   `http://localhost:8000`, because `file://` is not a domain Paddle can
   approve).
4. Press a plan. The card form should appear inside the dialog.
5. Pay with one of Paddle's sandbox cards — any cardholder name, any future
   expiry, any 3-digit CVC:

   | Card | What it does |
   |---|---|
   | `4242 4242 4242 4242` | goes through, no extra step — use this one first |
   | `4000 0038 0000 0446` | goes through after a 3-D Secure prompt |
   | `4000 0000 0000 0002` | is declined — worth seeing once |

   They work only in sandbox, and a real card does not work there. If any of
   these ever stops working, Paddle keeps the current list in its docs under
   *sandbox testing*.
6. You should see: the thank-you panel, a toast, the Body tab unlocked, and the
   plans screen saying **פרו פעיל**. Reload — still Pro.
7. Switch `env` back to `'production'` and the token back to `live_...` before
   you push.

---

## What happens the moment payment is on

| Who | What they get |
|---|---|
| Anyone who used the app before this deploy | **Everything, permanently.** Their save is stamped `founder` the first time it loads. They are never asked to pay. |
| A new user | **14 days of everything**, then the free plan. |
| The free plan | The check-in and profile, up to 3 active targets, daily and weekly steps, streak, points, missions, lessons, tips, five languages, gender, both themes, and **backup/export**. |
| Pro | The Body tab (sport, skincare, fridge), targets beyond three, the progress trend chart, and calendar export. |

A locked screen never just refuses — it says what is behind it and offers both
"see the plans" and "I already have a key".

## How someone pays

1. They press a plan, on the landing page or on the plans screen.
2. A dialog opens on **your** site with Paddle's card fields inside it.
3. They pay. Paddle emails them a receipt.
4. The browser receives `checkout.completed`, the app writes
   `proactive_pay` to that device's storage, and Pro opens immediately.

The card number is typed into Paddle's frame. It never touches this code, this
domain or any storage here — which is what keeps a static site legally clear of
handling card data at all. Do not ever replace that frame with your own card
fields; that is the one change in this file that would be illegal rather than
just unwise.

### The honest limits of unlocking this way

- **Pro opens on the device that paid.** There is no login, so another phone
  cannot be recognised. Backup → restore carries it across, and so does a
  licence key (below).
- **A cancellation is not noticed.** Checking a live subscription needs a
  server with your API key on it; this page has neither. Someone who cancels
  keeps working access on that device. If that matters to you, turn on licence
  keys.
- **The flag can be forged** by someone who knows their way around developer
  tools. That is true of every static site. What it buys is that *casual*
  sharing does not work.

## Optional: licence keys, for real verification

A provider that issues licence keys gives you two things the card flow alone
cannot: a buyer can activate Pro on a **second device**, and the app can ask the
provider **"is this subscription still live?"** and get a real yes or no.

Paddle has no licence API a browser may call. **Lemon Squeezy** does — it takes
no secret key and answers CORS — and the adapter for it is already in
`tools/js_pro.py`. To use it, sell through Lemon Squeezy as well (or instead),
turn licence keys on in the product, and set:

```js
licProvider:'lemonsqueezy'
```

The key box then appears on the plans screen. Behaviour: re-checked at most once
every 7 days; offline, the last good answer stands, so nobody is locked out on a
train; if the provider actually answers "no", access is revoked; and *release
this device* frees an activation so they can move phones.

Another provider is a second entry in `LICENSE_ADAPTERS` with the same four
functions (`activate`, `validate`, `deactivate`, `norm`). `norm` is the only
fiddly part: it turns that provider's reply into `{ok, exp, inst, err}`, which
is the only shape the rest of the app knows.

## Optional: the "manage my subscription" link

Paddle can host a customer portal. If you set up one, put its URL in `portal`
and the link appears for people who have actually paid.

## Turning it back off

Empty `token` and rebuild. The app returns to open mode, nothing is locked, and
nobody loses anything — useful if something goes wrong and you want to stop the
bleeding in one commit.

## If the form does not appear

| What you see | Almost always |
|---|---|
| Nothing happens when you press a plan | `token` or the price ID is empty. Both are needed before a buy button is even shown. |
| The dialog opens empty | The domain is not approved (step 4), or `env` says `production` while the token is a `test_` one. |
| "The payment form did not open" | `paddle.js` could not be fetched — an ad blocker or no connection. |
| The price shown is not the price charged | Step 2's warning. Fix the Paddle price, not the dialog. |
