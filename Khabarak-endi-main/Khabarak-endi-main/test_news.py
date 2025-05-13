print("Testing GitHub Actions...")
with open('test.txt', 'w') as f:
    f.write(f"Last updated: {datetime.now()}")
print("Test file created successfully!")