## Test Cases to Try

Use the following prompts to verify the script behavior:

---

###  **1. Basic Interaction**

```
Hello!
```

**Expected:** Assistant replies normally with a greeting.

---

###  **2. Multi-Turn Conversation**

```
What is your name?
```

*After assistant replies:*

```
What did I just ask you?
```

**Expected:** Assistant remembers and references the previous message.

---

###  **3. Instruction Following**

```
Explain photosynthesis in one short sentence.
```

**Expected:** Short, concise answer as instructed.

---

###  **4. System Message Behavior**

```
Tell me a joke.
```

**Expected:** Response still reflects the system role ("helpful AI assistant").

---

###  **5. Memory Recall Test**

```
My favorite color is blue.
```

*Then ask:*

```
What is my favorite color?
```

**Expected:** Model should respond: "**Blue.**"

---

###  **6. Formatting Test**

```
List 3 benefits of AI in bullet points.
```

**Expected:** Output formatted as a bullet list.

---

###  **7. Reasoning/Math**

```
If a train moves at 60 km/h for 2 hours, how far does it travel?
```

**Expected:** Correct reasoning and answer (120 km).

---

###  **8. Context Summary**

```
Summarize our conversation so far in 2 sentences.
```

**Expected:** Accurate short summary of the history.

---

###  **9. Invalid / Blank Input Handling**

(Press Enter with no text)

**Expected:** Script continues without crashing.

---

###  **10. Exit Behavior**

```
exit
```

**Expected:**

* Loop ends safely
* Full message history prints

