# Stack

Private grocery-deals app for Middleville/Wayland, MI.

- `index.html` — the app
- `data/` — deals, coupons and restaurants, refreshed every morning
- `scripts/fetch_images.py` + `.github/workflows/images.yml` — finds product photos daily (Open Food Facts)
- `scripts/fetch_showtimes.py` + `.github/workflows/showtimes.yml` — refreshes nearby movie showtimes once daily

## Movie showtimes setup

The in-app movie finder reads `data/showtimes.json`. To populate live sessions, create a free API Cinéma account, generate an API key, then add it to this GitHub repository under **Settings → Secrets and variables → Actions** as `API_CINEMA_KEY`. The key is used only by the scheduled GitHub Action and is never sent to app visitors.

The provider's documented free plan includes 100 requests per week. Its showtime feed includes theaters, movies, local session times, formats and booking links, but does **not** provide ticket prices; the app therefore shows "Price at checkout" unless a source actually supplies a price. Ticket purchase opens only when the user chooses a screening.

## Household app setup

See HOUSEHOLD-SETUP.md for Android/iPhone installation and secure shared-list setup.
