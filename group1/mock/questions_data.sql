-- SQL Data for the "Question" model (Expanded)
-- Note: Table names in Django are typically formatted as `appname_modelname`. I'm assuming your app is named 'quiz'.

INSERT INTO group1_question (id, type, difficulty_level, text_or_prompt, passage_text, image_url, voice_url, word_list, correct_text_answer, parent_question_id) VALUES
-- Original Questions
(1, 'VOCAB', 'Easy', 'A person who is fluent in many languages is known as a ________.', NULL, NULL, NULL, NULL, NULL, NULL),
(2, 'IMAGE', 'Easy', 'What is this piece of equipment called?', NULL, 'https://placehold.co/600x400/8B5CF6/ffffff?text=Telescope', NULL, NULL, NULL, NULL),
(3, 'WRITING', 'Medium', 'Complete the sentence: If I had known you were coming, I ________ a cake.', NULL, NULL, NULL, NULL, 'would have baked', NULL),
(4, 'GRAMMAR', 'Medium', 'The team members are working hard on their project, but they haven''t finished it _______.', NULL, NULL, NULL, NULL, NULL, NULL),
(5, 'SENTENCE', 'Hard', 'Drag the words to form a correct sentence.', NULL, NULL, NULL, '["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]', 'The quick brown fox jumps over the lazy dog.', NULL),
(6, 'LISTENING', 'Easy', 'Listen to the audio and choose the correct statement.', NULL, NULL, 'https://example.com/audio/train_schedule.mp3', NULL, NULL, NULL),
(7, 'READING', 'Medium', 'Read the passage below and answer the questions that follow.', 'The Industrial Revolution, which began in Great Britain in the late 18th century, was a period of major industrialization. It saw the mechanization of agriculture and textile manufacturing and a revolution in power, including steam ships and railroads. This period altered the social, economic, and cultural fabric of the age.', NULL, NULL, NULL, NULL, NULL),
(8, 'READING', 'Medium', 'What was a major outcome of the revolution mentioned in the passage?', NULL, NULL, NULL, NULL, NULL, 7),
(9, 'READING', 'Medium', 'According to the text, where did the Industrial Revolution begin?', NULL, NULL, NULL, NULL, NULL, 7),

-- New Additional Questions
(10, 'VOCAB', 'Medium', 'The act of setting someone free from imprisonment, slavery, or oppression.', NULL, NULL, NULL, NULL, NULL, NULL),
(11, 'GRAMMAR', 'Hard', 'If she ___ more time, she would travel the world.', NULL, NULL, NULL, NULL, NULL, NULL),
(12, 'IMAGE', 'Medium', 'What type of plant is shown in the image?', NULL, 'https://placehold.co/600x400/22c55e/ffffff?text=Cactus', NULL, NULL, NULL, NULL),
(13, 'LISTENING', 'Medium', 'Listen to the announcement. What is the gate number for flight BA249?', NULL, NULL, 'https://example.com/audio/flight_announcement.mp3', NULL, NULL, NULL),
(14, 'WRITING', 'Easy', 'What is your favorite food and why? Write at least one sentence.', NULL, NULL, NULL, NULL, NULL, NULL),
(15, 'SENTENCE', 'Easy', 'Put the words in the correct order.', NULL, NULL, NULL, '["likes", "she", "music", "listening", "to"]', 'She likes listening to music.', NULL),
(16, 'READING', 'Hard', 'Read the passage about photosynthesis and answer the questions.', 'Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy, through a process that converts carbon dioxide and water into sugars and oxygen. The process is crucial for life on Earth as it provides the oxygen we breathe and the primary source of energy for most ecosystems.', NULL, NULL, NULL, NULL, NULL),
(17, 'READING', 'Hard', 'What are the main inputs for photosynthesis according to the text?', NULL, NULL, NULL, NULL, NULL, 16),
(18, 'READING', 'Hard', 'Besides energy, what other critical output does photosynthesis provide for the planet?', NULL, NULL, NULL, NULL, NULL, 16),
(19, 'GRAMMAR', 'Easy', 'She ___ a doctor.', NULL, NULL, NULL, NULL, NULL, NULL),
(20, 'VOCAB', 'Hard', 'A feeling of deep anxiety or dread, typically an unfocused one about the human condition or the state of the world in general.', NULL, NULL, NULL, NULL, NULL, NULL);

