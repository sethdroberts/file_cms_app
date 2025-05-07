import unittest
from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("about.md", response.get_data(as_text=True))
            self.assertIn("changes.txt", response.get_data(as_text=True))
            self.assertIn("history.txt", response.get_data(as_text=True))
        
    def test_file(self):
        with self.client.get('files/history.txt') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/plain; charset=utf-8")
            self.assertIn("Python 0.9.0 (initial release) is released.",
                          response.get_data(as_text=True))
    
    def test_nonexistent_file(self):
       # Attempt to access a nonexistent file and verify a redirect happens
        with self.client.get("files/notafile.ext") as response:
            self.assertEqual(response.status_code, 302)

        # Verify redirect and message handling works
        with self.client.get(response.headers['Location']) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("notafile.ext does not exist",
                          response.get_data(as_text=True))

        # Assert that a page reload removes the message
        with self.client.get("/") as response:
            self.assertNotIn("notafile.ext does not exist",
                             response.get_data(as_text=True))
                             
    def test_markdown_file(self):
        with self.client.get('files/about.md') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("A dynamic, <strong>open source</strong> programming language",
                          response.get_data(as_text=True))
            

if __name__ == "__main__":
    unittest.main()