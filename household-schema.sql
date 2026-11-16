-- STACK household sync: run this in Supabase SQL Editor.
-- Both phones sign in with the same household email/password.
create table if not exists public.household_records (
  user_id uuid not null references auth.users(id) on delete cascade,
  record_key text not null check (record_key in ('shopping-list','favorites','list-extras','prescriptions')),
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, record_key)
);
alter table public.household_records enable row level security;
drop policy if exists "Household members can read own records" on public.household_records;
create policy "Household members can read own records" on public.household_records
  for select to authenticated using (auth.uid() = user_id);
drop policy if exists "Household members can insert own records" on public.household_records;
create policy "Household members can insert own records" on public.household_records
  for insert to authenticated with check (auth.uid() = user_id);
drop policy if exists "Household members can update own records" on public.household_records;
create policy "Household members can update own records" on public.household_records
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
drop policy if exists "Household members can delete own records" on public.household_records;
create policy "Household members can delete own records" on public.household_records
  for delete to authenticated using (auth.uid() = user_id);
alter table public.household_records replica identity full;
-- In Supabase Dashboard > Database > Replication, enable Realtime for household_records.
