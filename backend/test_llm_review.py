from app.agent.graph import run_llm_review


files = [
    {
        "filename": "test.py",
        "patch": """
+def get_user(users, user_id):
+    for user in users:
+        if user["id"] == user_id:
+            return user
+
+    return users[0]
"""
    }
]


findings = run_llm_review(files)

print(findings)