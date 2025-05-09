import json
import pyttsx3
import time

# Load the symbolic tree
with open("LexOS_Symbolic_Voice_Tree.json", "r", encoding="utf-8") as f:
    tree = json.load(f)

engine = pyttsx3.init()
engine.setProperty('rate', 165)

print("🌀 LexOS Drift Voice Engine")
print("Press [Enter] to speak each symbolic node. Type 'q' to quit.")

i = 0
while i < len(tree):
    node = tree[i]
    print(f"\n→ {node['SymbolicText']}")
    engine.say(node['SymbolicText'])
    engine.runAndWait()
    
    cmd = input(">> ")
    if cmd.lower() == 'q':
        break
    i += 1

print("Spiral closed.")