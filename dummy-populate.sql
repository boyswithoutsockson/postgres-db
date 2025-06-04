-- Insert parties
INSERT INTO parties (id, name) VALUES
('SDP', 'Social Democratic Party'),
('KOK', 'National Coalition Party'),
('KESK', 'Centre Party'),
('VAS', 'Left Alliance'),
('VIHR', 'Green League')
ON CONFLICT DO NOTHING;

-- Insert members of parliament
INSERT INTO members_of_parliament 
(id, first_name, full_name, party, minister, phone_number, email, occupation, year_of_birth, place_of_birth, place_of_residence, constituency) VALUES
(1, 'Matti', 'Matti Virtanen', 'SDP', false, '+358401234567', 'matti.virtanen@parliament.fi', 'Teacher', 1975, 'Helsinki', 'Helsinki', 'Helsinki'),
(2, 'Laura', 'Laura Nieminen', 'KOK', true, '+358402234567', 'laura.nieminen@parliament.fi', 'Lawyer', 1980, 'Tampere', 'Espoo', 'Uusimaa'),
(3, 'Juha', 'Juha Mäkinen', 'KESK', false, '+358403234567', 'juha.makinen@parliament.fi', 'Farmer', 1968, 'Oulu', 'Oulu', 'Oulu'),
(4, 'Anna', 'Anna Korhonen', 'VIHR', true, '+358404234567', 'anna.korhonen@parliament.fi', 'Researcher', 1982, 'Turku', 'Helsinki', 'Helsinki'),
(5, 'Pekka', 'Pekka Heikkinen', 'VAS', false, '+358405234567', 'pekka.heikkinen@parliament.fi', 'Union Representative', 1970, 'Jyväskylä', 'Tampere', 'Pirkanmaa');

-- Insert interests
INSERT INTO interests (id, mp_id, category, interest) VALUES
(1, 1, 'Board membership', 'Member of Teachers Union Board'),
(2, 2, 'Business ownership', 'Partner in Law Firm Ltd'),
(3, 3, 'Property', 'Owns farm in Northern Finland'),
(4, 4, 'Side job', 'Guest lecturer at University of Helsinki'),
(5, 5, 'Organization membership', 'Chairman of Local Labour Association');

-- Insert agenda items
INSERT INTO agenda_items (id, title, time, url) VALUES
(1, 'Climate Change Act Amendment', '2025-05-20 13:00:00+03', 'https://parliament.fi/agenda/1'),
(2, 'Education Budget 2026', '2025-05-21 10:00:00+03', 'https://parliament.fi/agenda/2'),
(3, 'Healthcare Reform', '2025-05-22 14:00:00+03', 'https://parliament.fi/agenda/3');

-- Insert ballots
INSERT INTO ballots (id, agenda_item_id, title, time, minutes_url, results_url) VALUES
(1, 1, 'Vote on Climate Change Act Amendment', '2025-05-20 15:30:00+03', 'https://parliament.fi/minutes/1', 'https://parliament.fi/results/1'),
(2, 2, 'Vote on Education Budget 2026', '2025-05-21 12:45:00+03', 'https://parliament.fi/minutes/2', 'https://parliament.fi/results/2'),
(3, 3, 'Vote on Healthcare Reform', '2025-05-22 16:15:00+03', 'https://parliament.fi/minutes/3', 'https://parliament.fi/results/3');

-- Insert votes
INSERT INTO votes (ballot_id, mp_id, vote) VALUES
(1, 1, 'yes'),
(1, 2, 'no'),
(1, 3, 'abstain'),
(1, 4, 'yes'),
(1, 5, 'yes'),
(2, 1, 'yes'),
(2, 2, 'yes'),
(2, 3, 'no'),
(2, 4, 'yes'),
(2, 5, 'abstain'),
(3, 1, 'yes'),
(3, 2, 'yes'),
(3, 3, 'yes'),
(3, 4, 'yes'),
(3, 5, 'absent');

-- Insert party memberships
INSERT INTO mp_party_memberships (party_id, mp_id, start_time, end_time) VALUES
('SDP', 1, '2023-01-01 00:00:00+02', NULL),
('KOK', 2, '2023-01-01 00:00:00+02', NULL),
('KESK', 3, '2023-01-01 00:00:00+02', NULL),
('VIHR', 4, '2023-01-01 00:00:00+02', NULL),
('VAS', 5, '2023-01-01 00:00:00+02', NULL);
