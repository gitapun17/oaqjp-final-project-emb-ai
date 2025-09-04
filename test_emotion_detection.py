import unittest
from emotion_detection import emotion_detector  # Adjust import if needed

class TestEmotionDetection(unittest.TestCase):
    def test_emotions(self):
        test_cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        ]

        for statement, expected_emotion in test_cases:
            with self.subTest(statement=statement):
                result = emotion_detector(statement)
                # result is a dictionary, check dominant_emotion key
                dominant_emotion = result.get('dominant_emotion')
                self.assertEqual(dominant_emotion, expected_emotion)

if __name__ == '__main__':
    unittest.main()