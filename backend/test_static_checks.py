from app.static_checks.bandit_check import run_bandit
from app.static_checks.semgrep_check import run_semgrep
from app.static_checks.secret_scan import scan_for_secrets


python_code = """
password = "secret123"
eval("print('hello')")
"""

secret_code = """
aws_key = "AKIA1234567890ABCDEF"
api_key = "sk-abcdefghijklmnopqrstuvwxyz123456"
"""


print("----- BANDIT -----")
print(run_bandit("test.py", python_code))

print("\n----- SEMGREP -----")
print(run_semgrep("test.py", python_code))

print("\n----- SECRET SCAN -----")
print(scan_for_secrets("config.py", secret_code))