CREATE TABLE public.bets (
	bet_id uuid NOT NULL,
	event_id text NOT NULL,
	price numeric(100, 2) NOT NULL,
	state varchar(4) NULL,
	CONSTRAINT bets_pkey PRIMARY KEY (bet_id)
);