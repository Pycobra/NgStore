import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "ARu-_pPT7to2ublMfXlzrhpsL9Xlye694JATZR3RBYPU3bQbmhqdTpkDvmq9KZleBmP0g5qGRYafWfRq"
        self.client_secret = "EBrknqFpM_6j_XE6JzZdtaG9vo19BCRBbqm6cYoT3hekIN1h9o93Zef2vpnELgJE2eESK3k-U3HuArqk"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
