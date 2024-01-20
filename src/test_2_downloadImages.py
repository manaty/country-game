import unittest

class TestDownloadLandmarksImages(unittest.TestCase):
    def test_response_is_url(self):
        # Assuming you have a function called `download_landmarks_images` that takes a CSV file as input
        csv_file = "/path/to/your/csv/file.csv"
        response = download_landmarks_images(csv_file)
        
        # Check if the response is a valid URL
        self.assertTrue(response.startswith("http://") or response.startswith("https://"))

if __name__ == '__main__':
    unittest.main()