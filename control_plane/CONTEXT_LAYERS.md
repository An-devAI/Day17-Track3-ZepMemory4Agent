# CONTEXT_LAYERS.md

The agent input is assembled from seven conceptual layers:

1. System context: persona and global constraints
2. Task context: current objective and instructions
3. User context: preferences and relevant history
4. Memory context: recalled facts and episodes
5. Retrieval context: shared/domain knowledge
6. Tool context: function and API outputs
7. Policy context: safety and governance rules

For this lab, the student implements the four memory sublayers inside Memory/Retrieval context. Policy context is protected and is never removed just to save tokens.
