-- CEO-GPT Supabase Setup
-- Einmalig im SQL Editor ausführen:
-- supabase.com → dein Projekt → SQL Editor → New query → reinkopieren → Run

-- Schreibzugriff freigeben (privater Bot, ein Nutzer)
alter table if exists produkte    disable row level security;
alter table if exists verkauf     disable row level security;
alter table if exists buchhaltung disable row level security;

create table if not exists produkte (
    id serial primary key,
    kategorie text not null,
    name text not null unique,
    einheit text not null default 'Stück',
    bestand decimal(10,2) default 0,
    mindestbestand decimal(10,2) default 0,
    preis decimal(10,2),
    notiz text,
    aktualisiert_am timestamptz default now()
);

create table if not exists verkauf (
    id serial primary key,
    datum date not null default current_date,
    produkt text not null,
    menge decimal(10,2) default 1,
    preis decimal(10,2) not null,
    kanal text default 'Direktverkauf',
    notiz text,
    erstellt_am timestamptz default now()
);

create table if not exists buchhaltung (
    id serial primary key,
    datum date not null default current_date,
    typ text not null check (typ in ('Einnahme', 'Ausgabe')),
    kategorie text not null,
    betrag decimal(10,2) not null,
    beschreibung text,
    erstellt_am timestamptz default now()
);
