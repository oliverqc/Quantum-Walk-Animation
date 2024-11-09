import os
import signal
import sys

import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")
import cv2
from moviepy.editor import VideoFileClip
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator


class QuantumWalkAnimator:
    def __init__(self, animation_dir, n_steps=100, max_runtime=300):
        self.animation_dir = animation_dir
        self.n_steps = n_steps
        self.max_runtime = max_runtime
        self.start_time = None
        self.running = True
        self.current_clip = None

        signal.signal(signal.SIGINT, self.signal_handler)

        self.animation_map = {
            "00": "simonscatanimationvertex1.mp4",
            "01": "simonscatanimationvertex2.mp4",
            "10": "simonscatanimationvertex3.mp4",
            "11": "simonscatanimationvertex4.mp4",
        }

    def signal_handler(self, signum, frame):
        if self.current_clip:
            self.current_clip.close()
        self.running = False
        cv2.destroyAllWindows()
        sys.exit(0)

    def create_shift_circuit(self):
        shift_q = QuantumRegister(2)
        shift_circ = QuantumCircuit(shift_q, name="shift_circ")

        shift_circ.h(shift_q[0])
        shift_circ.ry(np.pi / 4, shift_q[1])
        shift_circ.cx(shift_q[0], shift_q[1])
        shift_circ.s(shift_q[0])

        return shift_circ.to_instruction()

    def perform_quantum_walk(self):
        q = QuantumRegister(2, name="q")
        c = ClassicalRegister(2, name="c")

        circuits = []
        for step in range(self.n_steps):
            circ = QuantumCircuit(q, c)

            if step == 0:
                circ.h(q)

            shift_gate = self.create_shift_circuit()
            for i in range(step + 1):
                circ.append(shift_gate, [q[0], q[1]])

            circ.measure(q, c)
            circuits.append(circ)

        simulator = AerSimulator()
        jobs = []
        for circ in circuits:
            transpiled = transpile(circ, simulator)
            job = simulator.run(transpiled, shots=1)
            jobs.append(job)

        path = []
        for job in jobs:
            result = job.result()
            counts = result.get_counts()
            state = list(counts.keys())[0]
            path.append(state)

        return path

    def play_video(self, video_path):
        try:
            # Load video with audio using moviepy
            self.current_clip = VideoFileClip(video_path).resize(0.5)
            self.current_clip.preview()
            self.current_clip.close()
            return True

        except Exception as e:
            if self.current_clip:
                self.current_clip.close()
            return False

    def run(self):
        try:
            print(f"\nCalculating quantum walk path for {self.n_steps} steps...")
            path = self.perform_quantum_walk()

            print("\nQuantum Walk Path:")
            print(" -> ".join(path))
            print(f"\nTotal steps: {len(path)}")

            for state in path:
                if not self.running:
                    break

                video_file = self.animation_map[state]
                video_path = os.path.join(self.animation_dir, video_file)

                if os.path.exists(video_path):
                    self.play_video(video_path)

        except KeyboardInterrupt:
            if self.current_clip:
                self.current_clip.close()
        finally:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    animation_dir = (
        "/your/directory"
    )
    qw_animator = QuantumWalkAnimator(animation_dir)
    qw_animator.run()
