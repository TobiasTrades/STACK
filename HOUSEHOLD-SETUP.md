# STACK household sync and phone installation

## Install on both phones
- Android: open the deployed STACK URL in Chrome, use the browser menu, then Install app / Add to Home screen.
- iPhone: open the deployed STACK URL in Safari, tap Share, then Add to Home Screen. Enable Open as Web App if offered.
- Both phones can use the same household email/password. This first implementation intentionally uses one shared household login.

## Enable shared household sync (one-time owner setup)
The repository cannot create a hosted database project or obtain its credentials on your behalf. Create a free Supabase project, then:

1. Open the Supabase project dashboard and copy the Project URL and anon/publishable key.
2. Copy config.example.js to config.js, replace the two placeholder values, and commit config.js to this private app repository. The browser anon/publishable key is public by design; never use a service-role key.
3. In Supabase SQL Editor, run household-schema.sql.
4. In Database > Replication, enable Realtime for public.household_records.
5. Deploy the GitHub Pages site. Open Settings > Household account, create the household account once, then sign in on the other phone with the same credentials.

The table is protected by Row Level Security: only the signed-in household user can read/write its records. Do not share the household password outside the household.

If email confirmation is enabled in Supabase, confirm the account from the email before signing in. You can disable email confirmations in Supabase Auth settings for a simpler private household setup, but keep a strong password.

## Offline behavior
The app shell and artwork are cached for offline launch. Deals, coupons, restaurants and other fresh data still require internet and may show their last cached version offline. Shared household changes sync when online; this first version is not an offline-first conflict-resolution system.
