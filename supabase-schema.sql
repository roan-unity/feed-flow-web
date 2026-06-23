-- ═══════════════════════════════════════════════════════════════════
-- Feed Flow! Ambassador Program — Supabase Schema
-- ═══════════════════════════════════════════════════════════════════
--
-- SETUP STEPS:
--
-- 1. Create a Supabase project at https://supabase.com
--    → choose EU region (Frankfurt) for GDPR compliance
--    → note your project URL and anon public key
--
-- 2. Run this SQL in Supabase → SQL Editor → New query
--
-- 3. In Supabase → Authentication → Email:
--    → Enable "Enable email confirmations"  OFF
--    → Enable "Enable magic link" ON
--    → Set "Site URL" to https://tryfeedflow.app
--    → Add https://tryfeedflow.app/portal.html to redirect URLs
--
-- 4. In portal.html, replace:
--    var SUPABASE_URL      = 'YOUR_SUPABASE_URL';
--    var SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
--    with your actual values from Supabase → Settings → API
--
-- ═══════════════════════════════════════════════════════════════════

-- ── Enable pgcrypto for UUID generation ──
create extension if not exists pgcrypto;


-- ═══════════════════
-- TABLE: ambassadors
-- ═══════════════════
-- One row per ambassador. Created by Robin via ambassador-kit.html.
-- Matched to Supabase auth by email.
create table ambassadors (
  id            uuid primary key default gen_random_uuid(),
  name          text not null,
  email         text not null unique,   -- must match their Supabase auth email
  promo_code    text not null unique,   -- e.g. EMMA15 — created in App Store Connect
  discount_pct  integer not null,       -- e.g. 15 (percent)
  country       text not null default 'OTHER',
                                        -- 'NO' | 'SE' | 'DK' | 'FI' | 'EU' | 'GB' | 'US' | 'OTHER'
  platforms     text[] not null default '{}',
                                        -- e.g. ['instagram','tiktok']
  tier          integer not null default 1 check (tier in (1, 2, 3)),
  recruited_by  uuid references ambassadors(id),  -- null for Tier 1
  status        text not null default 'active' check (status in ('active','paused','removed')),
  created_at    timestamptz not null default now()
);


-- ════════════════════
-- TABLE: monthly_stats
-- ════════════════════
-- Robin uploads monthly stats after pulling the App Store Connect
-- Offer Code Redemptions CSV. One row per ambassador per month.
create table monthly_stats (
  id                        uuid primary key default gen_random_uuid(),
  ambassador_id             uuid not null references ambassadors(id) on delete cascade,
  month                     text not null,           -- 'YYYY-MM' e.g. '2026-06'
  direct_sales              integer not null default 0,
                                                     -- # redemptions via this ambassador's code
  direct_commission_ore     bigint  not null default 0,
                                                     -- 25% of net revenue, in øre (1 kr = 100 øre)
  override_commission_ore   bigint  not null default 0,
                                                     -- 5% of Tier 2 net revenue (Tier 1 only)
  source_currency           text not null default 'NOK',
  notes                     text,
  created_at                timestamptz not null default now(),
  unique (ambassador_id, month)
);


-- ═══════════════════
-- TABLE: payouts
-- ═══════════════════
-- Robin logs a row when an invoice is paid.
create table payouts (
  id             uuid primary key default gen_random_uuid(),
  ambassador_id  uuid not null references ambassadors(id) on delete cascade,
  amount_ore     bigint not null,          -- amount paid, in øre
  currency       text not null default 'NOK',
  method         text not null,            -- 'vipps' | 'bank_transfer' | 'paypal' | 'wise'
  month_covered  text not null,            -- 'YYYY-MM' — which earnings month this covers
  paid_at        timestamptz not null default now(),
  notes          text
);


-- ══════════════════════════
-- ROW LEVEL SECURITY
-- ══════════════════════════

alter table ambassadors   enable row level security;
alter table monthly_stats enable row level security;
alter table payouts       enable row level security;


-- Ambassadors can read their own record
create policy "ambassadors: read own record"
  on ambassadors for select
  using (email = (select email from auth.users where id = auth.uid()));

-- Ambassadors can also read records of their own recruits
-- (so Tier 1 dashboards can show their team)
create policy "ambassadors: read own recruits"
  on ambassadors for select
  using (
    recruited_by = (
      select a.id from ambassadors a
      where a.email = (select email from auth.users where id = auth.uid())
      limit 1
    )
  );

-- monthly_stats: own records only
create policy "monthly_stats: read own"
  on monthly_stats for select
  using (
    ambassador_id = (
      select a.id from ambassadors a
      where a.email = (select email from auth.users where id = auth.uid())
      limit 1
    )
  );

-- monthly_stats: Tier 1 can also read their recruits' stats
create policy "monthly_stats: read recruits"
  on monthly_stats for select
  using (
    ambassador_id in (
      select a.id from ambassadors a
      where a.recruited_by = (
        select b.id from ambassadors b
        where b.email = (select email from auth.users where id = auth.uid())
        limit 1
      )
    )
  );

-- payouts: own records only
create policy "payouts: read own"
  on payouts for select
  using (
    ambassador_id = (
      select a.id from ambassadors a
      where a.email = (select email from auth.users where id = auth.uid())
      limit 1
    )
  );

-- No ambassador-facing insert/update/delete — all writes are Robin-only via service role


-- ══════════════════════════════════════════════════
-- VIEWS (useful for Robin's admin work)
-- ══════════════════════════════════════════════════

-- Current month earnings summary (all ambassadors)
create or replace view v_earnings_current_month as
  select
    a.name,
    a.email,
    a.promo_code,
    a.tier,
    a.country,
    coalesce(s.direct_sales, 0) as sales,
    round((coalesce(s.direct_commission_ore, 0) + coalesce(s.override_commission_ore, 0)) / 100.0, 2) as earned_kr,
    coalesce(
      (select sum(p.amount_ore) / 100.0 from payouts p where p.ambassador_id = a.id),
      0
    ) as paid_total_kr
  from ambassadors a
  left join monthly_stats s on s.ambassador_id = a.id
    and s.month = to_char(current_date, 'YYYY-MM')
  where a.status = 'active'
  order by earned_kr desc;

-- All-time summary per ambassador
create or replace view v_earnings_all_time as
  select
    a.name,
    a.email,
    a.promo_code,
    a.tier,
    a.status,
    coalesce(sum(s.direct_sales), 0) as total_sales,
    round(coalesce(sum(s.direct_commission_ore + s.override_commission_ore), 0) / 100.0, 2) as total_earned_kr,
    round(coalesce((select sum(p.amount_ore) from payouts p where p.ambassador_id = a.id), 0) / 100.0, 2) as total_paid_kr
  from ambassadors a
  left join monthly_stats s on s.ambassador_id = a.id
  group by a.id, a.name, a.email, a.promo_code, a.tier, a.status
  order by total_earned_kr desc;


-- ══════════════════════════════════════════════════
-- SAMPLE: add your first ambassador (run manually)
-- ══════════════════════════════════════════════════
/*
insert into ambassadors (name, email, promo_code, discount_pct, country, platforms, tier)
values (
  'Emma Andersson',
  'emma@example.com',      -- this must match the email she logs in with
  'EMMA15',
  15,
  'NO',
  array['instagram', 'tiktok'],
  1
);
*/


-- ══════════════════════════════════════════════════
-- MONTHLY WORKFLOW: uploading stats after ASC report
-- ══════════════════════════════════════════════════
/*
Step 1 — Download the CSV from:
  App Store Connect → Analytics → Offer Code Redemptions → Export

Step 2 — Open Google Sheets, paste CSV
  Column setup: code | redemptions | product | net_revenue_nok
  Add formula: =net_revenue_nok * 0.25  → direct commission (kr)
  Add formula: =kr_amount * 100          → convert to øre

Step 3 — For each ambassador, paste the row into Supabase:
  (adjust month, amounts, then run)
*/
-- insert into monthly_stats (ambassador_id, month, direct_sales, direct_commission_ore)
-- select id, '2026-06', 12, 189000
-- from ambassadors where promo_code = 'EMMA15'
-- on conflict (ambassador_id, month)
-- do update set direct_sales = excluded.direct_sales, direct_commission_ore = excluded.direct_commission_ore;

/*
Step 4 — For Tier 1 overrides, calculate 5% of Tier 2 net revenue:
  Net_revenue * 0.05 * 100 → override_commission_ore for the Tier 1 ambassador
*/
-- update monthly_stats
-- set override_commission_ore = 42000  -- 5% of Tier 2 sales in øre
-- where ambassador_id = (select id from ambassadors where promo_code = 'TIER1CODE')
-- and month = '2026-06';

/*
Step 5 — Log the payout when invoice is paid:
*/
-- insert into payouts (ambassador_id, amount_ore, method, month_covered)
-- select id, 189000, 'vipps', '2026-06'
-- from ambassadors where promo_code = 'EMMA15';
