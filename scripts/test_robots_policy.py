"""Run with: python3 -m unittest discover -s scripts -p 'test_robots_policy.py'."""

from pathlib import Path
import unittest
from urllib.robotparser import RobotFileParser


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.premium-landscapes.co.uk"
SEARCH_AGENTS = (
    "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User",
    "Claude-SearchBot", "Claude-User", "Googlebot", "bingbot",
)
TRAINING_AGENTS = (
    "GPTBot", "ClaudeBot", "CCBot", "Bytespider", "Applebot-Extended",
    "meta-externalagent", "MistralAI-Training", "cohere-ai",
)


class RobotsPolicyTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.policy = RobotFileParser()
        self.policy.parse(self.text.splitlines())

    def test_search_can_read_pages_and_assets(self):
        for agent in SEARCH_AGENTS:
            for path in ("/", "/landscaping-leicester", "/case-studies",
                         "/projects/full-garden-design-evington", "/images/logo.png"):
                with self.subTest(agent=agent, path=path):
                    self.assertTrue(self.policy.can_fetch(agent, BASE + path))

    def test_training_opt_outs(self):
        for agent in TRAINING_AGENTS:
            with self.subTest(agent=agent):
                self.assertFalse(self.policy.can_fetch(agent, BASE + "/"))

    def test_sitemap_is_preserved(self):
        self.assertEqual(self.policy.site_maps(), [BASE + "/sitemap.xml"])

    def test_no_conflicting_rules_for_search_agents(self):
        # Mirrors Cloudflare prepending training restrictions to the origin file.
        managed = "\n".join(
            f"User-agent: {agent}\nDisallow: /\n" for agent in TRAINING_AGENTS
        )
        combined = RobotFileParser()
        combined.parse((managed + "\n" + self.text).splitlines())
        for agent in SEARCH_AGENTS:
            with self.subTest(agent=agent):
                self.assertTrue(combined.can_fetch(agent, BASE + "/case-studies"))


if __name__ == "__main__":
    unittest.main()
