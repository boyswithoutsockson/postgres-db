SELECT id,
       title,
       session_item_title,
       start_time,
       minutes_url,
       results_url
FROM public.ballots
WHERE start_time > '2023-01-01'
LIMIT 1000;