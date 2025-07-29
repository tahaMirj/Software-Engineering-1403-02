-- Mock data for the "group1_quizquestion" table
-- This table links questions to their respective quizzes.

INSERT INTO group1_quizquestion (id, quiz_id, question_id, user_answer, is_correct) VALUES
-- Grammar Quiz (Quiz ID: 1) -> Questions 101-110
(1, 1, 101, NULL, false), (2, 1, 102, NULL, false), (3, 1, 103, NULL, false), (4, 1, 104, NULL, false), (5, 1, 105, NULL, false), (6, 1, 106, NULL, false), (7, 1, 107, NULL, false), (8, 1, 108, NULL, false), (9, 1, 109, NULL, false), (10, 1, 110, NULL, false),

-- Vocabulary Quiz (Quiz ID: 2) -> Questions 111-120
(11, 2, 111, NULL, false), (12, 2, 112, NULL, false), (13, 2, 113, NULL, false), (14, 2, 114, NULL, false), (15, 2, 115, NULL, false), (16, 2, 116, NULL, false), (17, 2, 117, NULL, false), (18, 2, 118, NULL, false), (19, 2, 119, NULL, false), (20, 2, 120, NULL, false),

-- Image Quiz (Quiz ID: 3) -> Questions 121-130
(21, 3, 121, NULL, false), (22, 3, 122, NULL, false), (23, 3, 123, NULL, false), (24, 3, 124, NULL, false), (25, 3, 125, NULL, false), (26, 3, 126, NULL, false), (27, 3, 127, NULL, false), (28, 3, 128, NULL, false), (29, 3, 129, NULL, false), (30, 3, 130, NULL, false),

-- Writing Quiz (Quiz ID: 4) -> Questions 131-140
(31, 4, 131, NULL, false), (32, 4, 132, NULL, false), (33, 4, 133, NULL, false), (34, 4, 134, NULL, false), (35, 4, 135, NULL, false), (36, 4, 136, NULL, false), (37, 4, 137, NULL, false), (38, 4, 138, NULL, false), (39, 4, 139, NULL, false), (40, 4, 140, NULL, false),

-- Sentence Building Quiz (Quiz ID: 5) -> Questions 141-150
(41, 5, 141, NULL, false), (42, 5, 142, NULL, false), (43, 5, 143, NULL, false), (44, 5, 144, NULL, false), (45, 5, 145, NULL, false), (46, 5, 146, NULL, false), (47, 5, 147, NULL, false), (48, 5, 148, NULL, false), (49, 5, 149, NULL, false), (50, 5, 150, NULL, false),

-- Listening Quiz (Quiz ID: 6) -> Questions 151-160
(51, 6, 151, NULL, false), (52, 6, 152, NULL, false), (53, 6, 153, NULL, false), (54, 6, 154, NULL, false), (55, 6, 155, NULL, false), (56, 6, 156, NULL, false), (57, 6, 157, NULL, false), (58, 6, 158, NULL, false), (59, 6, 159, NULL, false), (60, 6, 160, NULL, false),

-- Reading Quiz (Quiz ID: 7) -> Questions 161-170
(61, 7, 161, NULL, false), (62, 7, 162, NULL, false), (63, 7, 163, NULL, false), (64, 7, 164, NULL, false), (65, 7, 165, NULL, false), (66, 7, 166, NULL, false), (67, 7, 167, NULL, false), (68, 7, 168, NULL, false), (69, 7, 169, NULL, false), (70, 7, 170, NULL, false);

