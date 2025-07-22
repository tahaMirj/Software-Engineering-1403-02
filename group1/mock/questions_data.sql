-- Mock data for the "group1_question" table
-- 10 questions per type: GRAMMAR, VOCAB, IMAGE, WRITING, SENTENCE, LISTENING, READING

INSERT INTO group1_question (id, type, difficulty_level, text_or_prompt, passage_text, image_url, voice_url, word_list, correct_text_answer, parent_question_id) VALUES

-- ========= 10 GRAMMAR QUESTIONS =========
(101, 'GRAMMAR', 'Easy', 'She ___ a doctor.', NULL, NULL, NULL, NULL, 'is', NULL),
(102, 'GRAMMAR', 'Easy', 'They ___ happy.', NULL, NULL, NULL, NULL, 'are', NULL),
(103, 'GRAMMAR', 'Medium', 'He hasn''t finished his homework ___.', NULL, NULL, NULL, NULL, 'yet', NULL),
(104, 'GRAMMAR', 'Medium', 'If I ___ you, I would study harder.', NULL, NULL, NULL, NULL, 'were', NULL),
(105, 'GRAMMAR', 'Medium', 'The book is ___ the table.', NULL, NULL, NULL, NULL, 'on', NULL),
(106, 'GRAMMAR', 'Hard', 'Neither the students nor the teacher ___ satisfied with the results.', NULL, NULL, NULL, NULL, 'was', NULL),
(107, 'GRAMMAR', 'Hard', 'By this time next year, I ___ my studies.', NULL, NULL, NULL, NULL, 'will have completed', NULL),
(108, 'GRAMMAR', 'Easy', 'What time ___ the train leave?', NULL, NULL, NULL, NULL, 'does', NULL),
(109, 'GRAMMAR', 'Medium', 'She is interested ___ learning Spanish.', NULL, NULL, NULL, NULL, 'in', NULL),
(110, 'GRAMMAR', 'Hard', 'The committee ___ decided to postpone the meeting.', NULL, NULL, NULL, NULL, 'has', NULL),

-- ========= 10 VOCABULARY QUESTIONS =========
(111, 'VOCAB', 'Easy', 'What is the opposite of "hot"?', NULL, NULL, NULL, NULL, 'cold', NULL),
(112, 'VOCAB', 'Easy', 'A place where books are kept.', NULL, NULL, NULL, NULL, 'library', NULL),
(113, 'VOCAB', 'Medium', 'To be very successful and admired.', NULL, NULL, NULL, NULL, 'eminent', NULL),
(114, 'VOCAB', 'Medium', 'Something that is very old.', NULL, NULL, NULL, NULL, 'ancient', NULL),
(115, 'VOCAB', 'Medium', 'A person who writes books.', NULL, NULL, NULL, NULL, 'author', NULL),
(116, 'VOCAB', 'Hard', 'To make something worse.', NULL, NULL, NULL, NULL, 'exacerbate', NULL),
(117, 'VOCAB', 'Hard', 'A person who is skilled in many different areas.', NULL, NULL, NULL, NULL, 'polymath', NULL),
(118, 'VOCAB', 'Easy', 'The color of the sky on a clear day.', NULL, NULL, NULL, NULL, 'blue', NULL),
(119, 'VOCAB', 'Medium', 'A synonym for "happy".', NULL, NULL, NULL, NULL, 'joyful', NULL),
(120, 'VOCAB', 'Hard', 'Lasting for a very short time.', NULL, NULL, NULL, NULL, 'ephemeral', NULL),

-- ========= 10 IMAGE QUESTIONS =========
(121, 'IMAGE', 'Easy', 'What animal is this?', NULL, 'https://placehold.co/600x400/3498db/ffffff?text=Dog', NULL, NULL, 'Dog', NULL),
(122, 'IMAGE', 'Easy', 'What fruit is shown in the picture?', NULL, 'https://placehold.co/600x400/e74c3c/ffffff?text=Apple', NULL, NULL, 'Apple', NULL),
(123, 'IMAGE', 'Medium', 'What is the name of this famous landmark?', NULL, 'https://placehold.co/600x400/f1c40f/ffffff?text=Eiffel+Tower', NULL, NULL, 'Eiffel Tower', NULL),
(124, 'IMAGE', 'Medium', 'What activity is being performed?', NULL, 'https://placehold.co/600x400/2ecc71/ffffff?text=Running', NULL, NULL, 'Running', NULL),
(125, 'IMAGE', 'Medium', 'Identify the tool shown in the image.', NULL, 'https://placehold.co/600x400/9b59b6/ffffff?text=Hammer', NULL, NULL, 'Hammer', NULL),
(126, 'IMAGE', 'Hard', 'What is the architectural style of this building?', NULL, 'https://placehold.co/600x400/1abc9c/ffffff?text=Gothic', NULL, NULL, 'Gothic', NULL),
(127, 'IMAGE', 'Hard', 'What type of cloud is depicted?', NULL, 'https://placehold.co/600x400/ecf0f1/000000?text=Cumulonimbus', NULL, NULL, 'Cumulonimbus', NULL),
(128, 'IMAGE', 'Easy', 'What color is the car?', NULL, 'https://placehold.co/600x400/e67e22/ffffff?text=Orange+Car', NULL, NULL, 'Orange', NULL),
(129, 'IMAGE', 'Medium', 'What is this musical instrument?', NULL, 'https://placehold.co/600x400/34495e/ffffff?text=Violin', NULL, NULL, 'Violin', NULL),
(130, 'IMAGE', 'Hard', 'What historical period is this clothing from?', NULL, 'https://placehold.co/600x400/7f8c8d/ffffff?text=Victorian+Era', NULL, NULL, 'Victorian Era', NULL),

-- ========= 10 WRITING QUESTIONS =========
(131, 'WRITING', 'Easy', 'Write one sentence about your favorite animal.', NULL, NULL, NULL, NULL, NULL, NULL),
(132, 'WRITING', 'Easy', 'What did you eat for breakfast today?', NULL, NULL, NULL, NULL, NULL, NULL),
(133, 'WRITING', 'Medium', 'Describe your dream vacation in two sentences.', NULL, NULL, NULL, NULL, NULL, NULL),
(134, 'WRITING', 'Medium', 'Explain the importance of recycling.', NULL, NULL, NULL, NULL, NULL, NULL),
(135, 'WRITING', 'Medium', 'Write a short story about a friendly robot.', NULL, NULL, NULL, NULL, NULL, NULL),
(136, 'WRITING', 'Hard', 'Summarize your favorite movie in three sentences.', NULL, NULL, NULL, NULL, NULL, NULL),
(137, 'WRITING', 'Hard', 'Argue for or against the use of school uniforms.', NULL, NULL, NULL, NULL, NULL, NULL),
(138, 'WRITING', 'Easy', 'What is your name?', NULL, NULL, NULL, NULL, NULL, NULL),
(139, 'WRITING', 'Medium', 'What is the best way to learn a new language?', NULL, NULL, NULL, NULL, NULL, NULL),
(140, 'WRITING', 'Hard', 'Write a poem about the four seasons.', NULL, NULL, NULL, NULL, NULL, NULL),

-- ========= 10 SENTENCE BUILDING QUESTIONS =========
(141, 'SENTENCE', 'Easy', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["cat", "the", "sat", "mat", "on", "the"]', 'The cat sat on the mat.', NULL),
(142, 'SENTENCE', 'Easy', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["I", "love", "programming"]', 'I love programming.', NULL),
(143, 'SENTENCE', 'Medium', 'Arrange the words to form a question.', NULL, NULL, NULL, '["is", "your", "name", "what"]', 'What is your name?', NULL),
(144, 'SENTENCE', 'Medium', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["makes", "practice", "perfect"]', 'Practice makes perfect.', NULL),
(145, 'SENTENCE', 'Medium', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["is", "learning", "fun", "new", "things"]', 'Learning new things is fun.', NULL),
(146, 'SENTENCE', 'Hard', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["never", "judge", "a", "book", "by", "its", "cover"]', 'Never judge a book by its cover.', NULL),
(147, 'SENTENCE', 'Hard', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["the", "early", "bird", "gets", "the", "worm"]', 'The early bird gets the worm.', NULL),
(148, 'SENTENCE', 'Easy', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["sky", "the", "is", "blue"]', 'The sky is blue.', NULL),
(149, 'SENTENCE', 'Medium', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["a", "day", "an", "apple", "keeps", "the", "doctor", "away"]', 'An apple a day keeps the doctor away.', NULL),
(150, 'SENTENCE', 'Hard', 'Arrange the words to form a sentence.', NULL, NULL, NULL, '["actions", "speak", "louder", "than", "words"]', 'Actions speak louder than words.', NULL),

-- ========= 10 LISTENING QUESTIONS =========
(151, 'LISTENING', 'Easy', 'Listen to the sound. What animal is it?', NULL, NULL, 'https://placehold.co/audio/dog_bark.mp3', NULL, 'Dog', NULL),
(152, 'LISTENING', 'Easy', 'Listen to the number and write it down.', NULL, NULL, 'https://placehold.co/audio/number_seven.mp3', NULL, '7', NULL),
(153, 'LISTENING', 'Medium', 'Listen to the announcement. What is the flight number?', NULL, NULL, 'https://placehold.co/audio/flight_announcement.mp3', NULL, 'BA249', NULL),
(154, 'LISTENING', 'Medium', 'Listen to the conversation. Where are they going?', NULL, NULL, 'https://placehold.co/audio/conversation_park.mp3', NULL, 'To the park', NULL),
(155, 'LISTENING', 'Medium', 'Listen to the weather forecast. What will the weather be like tomorrow?', NULL, NULL, 'https://placehold.co/audio/weather_forecast.mp3', NULL, 'Sunny', NULL),
(156, 'LISTENING', 'Hard', 'Listen to the lecture snippet. What is the main topic?', NULL, NULL, 'https://placehold.co/audio/lecture_photosynthesis.mp3', NULL, 'Photosynthesis', NULL),
(157, 'LISTENING', 'Hard', 'Listen to the story. What is the moral?', NULL, NULL, 'https://placehold.co/audio/story_moral.mp3', NULL, 'Honesty is the best policy', NULL),
(158, 'LISTENING', 'Easy', 'Listen to the word and spell it.', NULL, NULL, 'https://placehold.co/audio/word_hello.mp3', NULL, 'H-E-L-L-O', NULL),
(159, 'LISTENING', 'Medium', 'Listen to the directions. Where is the library?', NULL, NULL, 'https://placehold.co/audio/directions_library.mp3', NULL, 'Next to the post office', NULL),
(160, 'LISTENING', 'Hard', 'Listen to the poem. What is the primary emotion conveyed?', NULL, NULL, 'https://placehold.co/audio/poem_sadness.mp3', NULL, 'Sadness', NULL),

-- ========= 10 READING QUESTIONS (3 Main + 7 Sub) =========
-- Main Reading Question 1
(161, 'READING', 'Medium', 'Read the passage about the solar system and answer the questions that follow.', 'Our solar system is a vast and fascinating place, consisting of the Sun and everything that orbits it, including eight planets, their moons, dwarf planets, asteroids, and comets. The four inner planets—Mercury, Venus, Earth, and Mars—are known as terrestrial planets because of their solid, rocky surfaces. The four outer planets—Jupiter, Saturn, Uranus, and Neptune—are gas giants, much larger and composed mostly of hydrogen, helium, and methane.', NULL, NULL, NULL, NULL, 161),
-- Sub-questions for Main Question 1
(162, 'READING', 'Medium', 'How many planets are in our solar system?', NULL, NULL, NULL, NULL, '8', 161),
(163, 'READING', 'Medium', 'Which are the terrestrial planets?', NULL, NULL, NULL, NULL, 'Mercury, Venus, Earth, and Mars', 161),
(164, 'READING', 'Hard', 'What are the primary components of the gas giants?', NULL, NULL, NULL, NULL, 'Hydrogen, helium, and methane', 161),

-- Main Reading Question 2
(165, 'READING', 'Hard', 'Read the passage about artificial intelligence and answer the questions that follow.', 'Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. AI research deals with tasks such as reasoning, knowledge representation, planning, learning, and natural language processing. While narrow AI has already become a part of our daily lives through applications like virtual assistants and recommendation engines, the pursuit of Artificial General Intelligence (AGI), which would possess human-like cognitive abilities, remains a long-term goal with profound ethical implications.', NULL, NULL, NULL, NULL, 165),
-- Sub-questions for Main Question 2
(166, 'READING', 'Hard', 'What is the ultimate goal of AGI?', NULL, NULL, NULL, NULL, 'To possess human-like cognitive abilities', 165),
(167, 'READING', 'Hard', 'Name one application of narrow AI mentioned in the text.', NULL, NULL, NULL, NULL, 'Virtual assistants or recommendation engines', 165),

-- Main Reading Question 3
(168, 'READING', 'Easy', 'Read the passage about honeybees and answer the questions that follow.', 'Honeybees are vital for pollinating many of the crops we rely on for food. They live in large colonies with a single queen, many male drones, and thousands of female worker bees. Worker bees perform various tasks, including foraging for nectar and pollen, building the honeycomb, and defending the hive. They communicate with each other using a special ''waggle dance''.', NULL, NULL, NULL, NULL, 168),
-- Sub-questions for Main Question 3
(169, 'READING', 'Easy', 'What is the primary role of honeybees in agriculture?', NULL, NULL, NULL, NULL, 'Pollinating crops', 168),
(170, 'READING', 'Easy', 'How do honeybees communicate?', NULL, NULL, NULL, NULL, 'Using a waggle dance', 168);

