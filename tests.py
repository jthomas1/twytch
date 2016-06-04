import unittest
import twytch


class TwytchTests(unittest.TestCase):
    def test_check_twitch_url_legit_urls_returns_true(self):
        self.assertTrue(
            twytch.check_twitch_url("https://twitch.tv/mychannel"))
        self.assertTrue(
            twytch.check_twitch_url("http://twitch.tv/mychannel"))
        self.assertTrue(
            twytch.check_twitch_url("twitch.tv/mychannel"))
        self.assertTrue(
            twytch.check_twitch_url("www.twitch.tv/mychannel"))
        self.assertTrue(
            twytch.check_twitch_url("https://www.twitch.tv/mychannel"))
        self.assertTrue(
            twytch.check_twitch_url("http://www.twitch.tv/mychannel"))

    def test_check_twitch_url_bad_urls_returns_false(self):
        self.assertFalse(
            twytch.check_twitch_url("https://ttwitch.tv/mychannel"))
        self.assertFalse(
            twytch.check_twitch_url("https://witch.tv/mychannel"))
        self.assertFalse(
            twytch.check_twitch_url("https://twitch.tv/myc  hannel"))
        self.assertFalse(
            twytch.check_twitch_url("https://twitch.com/mychannel"))
        self.assertFalse(
            twytch.check_twitch_url("https://twitch.tv.com/mychannel"))
        self.assertFalse(
            twytch.check_twitch_url("https:// twitch.com/mychannel"))


if __name__ == '__main__':
    unittest.main()
