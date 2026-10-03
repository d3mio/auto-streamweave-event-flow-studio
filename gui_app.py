import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import threading
import random

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class StreamWeaveApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('StreamWeave Live Event Flow Studio')
        self.geometry('1200x800')

        self.stream_data = pd.DataFrame(columns=['Timestamp', 'Latency', 'Payload'])
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.chart_frame = ctk.CTkFrame(self.frame)
        self.chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.table_frame = ctk.CTkFrame(self.frame)
        self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.table = ttk.Treeview(self.table_frame, columns=('Timestamp', 'Latency', 'Payload'), show='headings')
        self.table.heading('Timestamp', text='Timestamp')
        self.table.heading('Latency', text='Latency')
        self.table.heading('Payload', text='Payload')
        self.table.pack(fill=tk.BOTH, expand=True)

        self.control_frame = ctk.CTkFrame(self.frame)
        self.control_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.start_button = ctk.CTkButton(self.control_frame, text='Start Stream', command=self.start_stream)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = ctk.CTkButton(self.control_frame, text='Stop Stream', command=self.stop_stream)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = ctk.CTkLabel(self.control_frame, text='Status: Stopped')
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_chart()

    def start_stream(self):
        self.status_label.configure(text='Status: Running')
        self.stream_thread = threading.Thread(target=self.simulate_stream, daemon=True)
        self.stream_thread.start()

    def stop_stream(self):
        self.status_label.configure(text='Status: Stopped')
        self.stream_data = pd.DataFrame(columns=['Timestamp', 'Latency', 'Payload'])

    def simulate_stream(self):
        while self.status_label.cget('text') == 'Status: Running':
            new_data = pd.DataFrame({
                'Timestamp': [pd.Timestamp.now()],
                'Latency': [random.uniform(0, 100)],
                'Payload': [random.randint(100, 1000)]
            })
            self.stream_data = pd.concat([self.stream_data, new_data], ignore_index=True)
            self.update_chart()
            self.update_table()
            self.after(1000)

    def update_chart(self):
        self.ax.clear()
        self.ax.plot(self.stream_data['Timestamp'], self.stream_data['Latency'], label='Latency')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Latency (ms)')
        self.ax.legend()
        self.canvas.draw()

    def update_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
        for _, row in self.stream_data.tail(10).iterrows():
            self.table.insert('', 'end', values=(row['Timestamp'], row['Latency'], row['Payload']))


if __name__ == '__main__':
    app = StreamWeaveApp()
    app.mainloop()