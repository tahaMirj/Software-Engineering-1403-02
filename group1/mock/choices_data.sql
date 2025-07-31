-- Mock data for the "group1_choice" table

INSERT INTO group1_choice (id, question_id, text, is_correct) VALUES

-- ========= CHOICES FOR GRAMMAR QUESTIONS (101-110) =========
(101, 101, 'is', true), (102, 101, 'are', false), (103, 101, 'am', false),
(104, 102, 'is', false), (105, 102, 'are', true), (106, 102, 'am', false),
(107, 103, 'already', false), (108, 103, 'yet', true), (109, 103, 'still', false),
(110, 104, 'was', false), (111, 104, 'were', true), (112, 104, 'is', false),
(113, 105, 'on', true), (114, 105, 'in', false), (115, 105, 'at', false),
(116, 106, 'was', true), (117, 106, 'were', false), (118, 106, 'are', false),
(119, 107, 'will complete', false), (120, 107, 'will be completing', false), (121, 107, 'will have completed', true),
(122, 108, 'do', false), (123, 108, 'does', true), (124, 108, 'is', false),
(125, 109, 'in', true), (126, 109, 'on', false), (127, 109, 'at', false),
(128, 110, 'has', true), (129, 110, 'have', false), (130, 110, 'is', false),

-- ========= CHOICES FOR VOCABULARY QUESTIONS (111-120) =========
(131, 111, 'cold', true), (132, 111, 'warm', false), (133, 111, 'cool', false),
(134, 112, 'museum', false), (135, 112, 'library', true), (136, 112, 'cinema', false),
(137, 113, 'notorious', false), (138, 113, 'eminent', true), (139, 113, 'obscure', false),
(140, 114, 'modern', false), (141, 114, 'recent', false), (142, 114, 'ancient', true),
(143, 115, 'reader', false), (144, 115, 'author', true), (145, 115, 'publisher', false),
(146, 116, 'ameliorate', false), (147, 116, 'exacerbate', true), (148, 116, 'mitigate', false),
(149, 117, 'specialist', false), (150, 117, 'amateur', false), (151, 117, 'polymath', true),
(152, 118, 'green', false), (153, 118, 'red', false), (154, 118, 'blue', true),
(155, 119, 'sad', false), (156, 119, 'joyful', true), (157, 119, 'angry', false),
(158, 120, 'permanent', false), (159, 120, 'eternal', false), (160, 120, 'ephemeral', true),

-- ========= CHOICES FOR IMAGE QUESTIONS (121-130) =========
(161, 121, 'Cat', false), (162, 121, 'Dog', true), (163, 121, 'Bird', false),
(164, 122, 'Banana', false), (165, 122, 'Apple', true), (166, 122, 'Orange', false),
(167, 123, 'Statue of Liberty', false), (168, 123, 'Eiffel Tower', true), (169, 123, 'Big Ben', false),
(170, 124, 'Swimming', false), (171, 124, 'Running', true), (172, 124, 'Cycling', false),
(173, 125, 'Screwdriver', false), (174, 125, 'Wrench', false), (175, 125, 'Hammer', true),
(176, 126, 'Modern', false), (177, 126, 'Gothic', true), (178, 126, 'Baroque', false),
(179, 127, 'Cirrus', false), (180, 127, 'Stratus', false), (181, 127, 'Cumulonimbus', true),
(182, 128, 'Blue', false), (183, 128, 'Red', false), (184, 128, 'Orange', true),
(185, 129, 'Guitar', false), (186, 129, 'Piano', false), (187, 129, 'Violin', true),
(188, 130, 'Renaissance', false), (189, 130, 'Victorian Era', true), (190, 130, 'Roaring Twenties', false),

-- ========= CHOICES FOR LISTENING QUESTIONS (151-160) =========
(191, 151, 'Cat', false), (192, 151, 'Dog', true), (193, 151, 'Cow', false),
(194, 152, '5', false), (195, 152, '7', true), (196, 152, '9', false),
(197, 153, 'AA123', false), (198, 153, 'BA249', true), (199, 153, 'DL456', false),
(200, 154, 'To the cinema', false), (201, 154, 'To the park', true), (202, 154, 'To the restaurant', false),
(203, 155, 'Rainy', false), (204, 155, 'Cloudy', false), (205, 155, 'Sunny', true),
(206, 156, 'History', false), (207, 156, 'Biology', false), (208, 156, 'Photosynthesis', true),
(209, 157, 'Slow and steady wins the race', false), (210, 157, 'Honesty is the best policy', true), (211, 157, 'Look before you leap', false),
(212, 158, 'H-E-L-L-O', true), (213, 158, 'G-O-O-D-B-Y-E', false), (214, 158, 'W-E-L-C-O-M-E', false),
(215, 159, 'Across the street', false), (216, 159, 'Next to the post office', true), (217, 159, 'Behind the bank', false),
(218, 160, 'Joy', false), (219, 160, 'Anger', false), (220, 160, 'Sadness', true),

-- ========= CHOICES FOR READING QUESTIONS (162-170) =========
-- Sub-choices for Main Question 161
(221, 162, '8', true), (222, 162, '9', false), (223, 162, '10', false),
(224, 163, 'Jupiter, Saturn, Uranus, Neptune', false), (225, 163, 'Mercury, Venus, Earth, Mars', true), (226, 163, 'Pluto, Eris, Ceres', false),
(227, 164, 'Rock and metal', false), (228, 164, 'Ice and dust', false), (229, 164, 'Hydrogen, helium, and methane', true),

-- Sub-choices for Main Question 165
(230, 166, 'To perform narrow tasks', false), (231, 166, 'To possess human-like cognitive abilities', true), (232, 166, 'To replace human jobs', false),
(233, 167, 'Self-driving cars', false), (234, 167, 'Virtual assistants', true), (235, 167, 'Medical diagnosis', false),

-- Sub-choices for Main Question 168
(236, 169, 'Producing honey', false), (237, 169, 'Pollinating crops', true), (238, 169, 'Building hives', false),
(239, 170, 'By releasing pheromones', false), (240, 170, 'Through telepathy', false), (241, 170, 'Using a waggle dance', true);

