-- SQL Data for the "QuizQuestion" model (Expanded)
-- This table associates the questions with specific quiz instances.

INSERT INTO group1_quizquestion (id, quiz_id, question_id, user_answer, is_correct) VALUES
-- Expanded questions for Quiz 1 (user 1, in_progress)
(1, 1, 1, NULL, false),  -- Vocab (Easy)
(2, 1, 19, NULL, false), -- Grammar (Easy)
(3, 1, 2, NULL, false),  -- Image (Easy)
(4, 1, 15, NULL, false), -- Sentence (Easy)
(5, 1, 6, NULL, false),  -- Listening (Easy)
(6, 1, 7, NULL, false),  -- Reading (Medium, main passage)
(7, 1, 4, NULL, false),  -- Grammar (Medium)
(8, 1, 10, NULL, false), -- Vocab (Medium)
(9, 1, 5, NULL, false),  -- Sentence (Hard)
(10, 1, 11, NULL, false),-- Grammar (Hard)

-- Questions for Quiz 2 (user 2, in_progress)
(11, 2, 12, NULL, false), -- Image (Medium)
(12, 2, 13, NULL, false), -- Listening (Medium)
(13, 2, 14, NULL, false), -- Writing (Easy)
(14, 2, 16, NULL, false), -- Reading (Hard, main passage)
(15, 2, 20, NULL, false), -- Vocab (Hard)

-- Questions and answers for Quiz 3 (user 1, completed)
(16, 3, 1, 'Polyglot', true),       -- Correct
(17, 3, 4, 'still', false),      -- Incorrect
(18, 3, 2, 'Telescope', true),    -- Correct
(19, 3, 6, 'The train arrives at 5 PM.', true), -- Correct
(20, 3, 3, 'would bake', false); -- Incorrect

