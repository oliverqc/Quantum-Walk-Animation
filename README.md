# Quantum-Walk-Animation
This program generates animation sequences by combining classical images using a Quantum Random Walk algorithm. The project explores how quantum computing can create new avenues of creative expression for artists.

The system utilizes a four-vertex graph where each vertex connects to two others via edges. It's implemented as a small quantum circuit using only two qubits, capable of calculating 100 vertices in 4.53 seconds. At each step, the walker applies a coin operator and position-space shift to determine which vertex to visit next.

In this context, the walker represents a sequence of classical images, with each vertex corresponding to a different animation state. For example, when animating a cat, vertex 1 might represent a happy state while vertex 2 represents a sad state, and so on. This concept could be expanded to develop complex geometries where features like ears, eyes, or paws are mapped to sheets of qubits, allowing entangled edges to influence the overall animation.

Currently, the implementation uses a simple four-vertex cycle to determine the states of a sushi chef character. While basic, this demonstrates the potential for quantum-driven animation techniques.


https://github.com/user-attachments/assets/a746e264-7948-4c23-982e-ec8d7be5aa3c

