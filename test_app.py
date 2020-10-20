from unittest import TestCase
from app import app


class AppTestCase (TestCase):
    def test_index_html(self):
        """Testing GET Request"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Currency Converter</h1>", html)

    def test_checkInput_post_request(self):
        """Test post request to check input validity"""
        with app.test_client() as client:
            response = client.post(
                "/checkInput", data={"cnyFrom": "USD", "cnyTo": "PHP", "amount": 1}, follow_redirects=True)

            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("The result is", html)
            self.assertIn("<title> Conversion Value </title>", html)

    def test_checkInput_post_wrong_cnyFrom(self):
        """Test failure data entry on cnyFrom"""
        with app.test_client() as client:
            response = client.post(
                "/checkInput", data={"cnyFrom": "UDS", "cnyTo": "PHP", "amount": 1}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Currency from not a valid code: UDS", html)

    def test_checkInput_post_wrong_cnyTo(self):
        """Test failure data entry on cnyTo"""
        with app.test_client() as client:
            response = client.post(
                "/checkInput", data={"cnyFrom": "USD", "cnyTo": "PPP", "amount": 1}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Currency to not a valid code: PPP", html)

    def test_checkInput_post_wrong_amount(self):
        """Test failure data entry on Amount"""
        with app.test_client() as client:
            response = client.post(
                "/checkInput", data={"cnyFrom": "USD", "cnyTo": "PHP", "amount": 'a'}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Invalid amount", html)

    def test_convert(self):
        """Test post conversion"""
        with app.test_client() as client:
            response = client.post(
                "/checkInput", data={"cnyFrom": "USD", "cnyTo": "USD", "amount": 100}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("The result is US$ 100.", html)
