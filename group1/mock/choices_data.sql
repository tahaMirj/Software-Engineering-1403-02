-- SQL Data for the "Choice" model (Expanded)

INSERT INTO group1_choice (id, question_id, text, is_correct) VALUES
-- Choices for Question 1 (VOCAB)
(1, 1, 'Linguist', false), (2, 1, 'Polyglot', true), (3, 1, 'Bilingual', false), (4, 1, 'Orator', false),
-- Choices for Question 2 (IMAGE)
(5, 2, 'Microscope', false), (6, 2, 'Telescope', true), (7, 2, 'Binoculars', false), (8, 2, 'Kaleidoscope', false),
-- Choices for Question 4 (GRAMMAR)
(9, 4, 'already', false), (10, 4, 'yet', true), (11, 4, 'still', false), (12, 4, 'since', false),
-- Choices for Question 6 (LISTENING)
(13, 6, 'The train arrives at 5 PM.', true), (14, 6, 'The plane departs at 9 AM.', false), (15, 6, 'The meeting is on Tuesday.', false),
-- Choices for Question 8 (READING sub-question)
(16, 8, 'A decline in manufacturing.', false), (17, 8, 'The mechanization of agriculture.', true), (18, 8, 'A return to traditional farming.', false),
-- Choices for Question 9 (READING sub-question)
(19, 9, 'France', false), (20, 9, 'The United States', false), (21, 9, 'Great Britain', true),

-- New Choices for Expanded Data
-- Choices for Question 10 (VOCAB)
(22, 10, 'Emancipation', true), (23, 10, 'Incarceration', false), (24, 10, 'Subjugation', false),
-- Choices for Question 11 (GRAMMAR)
(25, 11, 'has', false), (26, 11, 'have', false), (27, 11, 'had', true),
-- Choices for Question 12 (IMAGE)
(28, 12, 'Rose', false), (29, 12, 'Fern', false), (30, 12, 'Cactus', true),
-- Choices for Question 13 (LISTENING)
(31, 13, 'Gate 12A', false), (32, 13, 'Gate 24B', true), (33, 13, 'Gate 36C', false),
-- Choices for Question 17 (READING sub-question)
(34, 17, 'Sugars and oxygen', false), (35, 17, 'Light energy and chemical energy', false), (36, 17, 'Carbon dioxide and water', true),
-- Choices for Question 18 (READING sub-question)
(37, 18, 'Oxygen', true), (38, 18, 'Sugars', false), (39, 18, 'Carbon dioxide', false),
-- Choices for Question 19 (GRAMMAR)
(40, 19, 'is', true), (41, 19, 'are', false), (42, 19, 'am', false),
-- Choices for Question 20 (VOCAB)
(43, 20, 'Euphoria', false), (44, 20, 'Angst', true), (45, 20, 'Apathy', false);

