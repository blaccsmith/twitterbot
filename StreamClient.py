from constants import CONSTANTS
from TweepyClient import TweepyClient as client

# Authenticate to Twitter
stream = client(CONSTANTS['Consumer_Key'], CONSTANTS['Consumer_Secret'], CONSTANTS['Access_Key'], CONSTANTS['Access_Secret'])