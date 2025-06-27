import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

kualitas_pelayanan = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'kualitas_pelayanan')
kualitas_makanan = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'kualitas_makanan')
tip_persentase = ctrl.Consequent(np.arange(0, 25.1, 0.1), 'tip_persentase', defuzzify_method='centroid')

kualitas_pelayanan['buruk'] = fuzz.trimf(kualitas_pelayanan.universe, [0, 0, 4])
kualitas_pelayanan['cukup'] = fuzz.trimf(kualitas_pelayanan.universe, [2, 5, 8])
kualitas_pelayanan['baik'] = fuzz.trimf(kualitas_pelayanan.universe, [6, 8, 10])
kualitas_pelayanan['sangat_baik'] = fuzz.trimf(kualitas_pelayanan.universe, [8, 10, 10])

kualitas_makanan['tidak_enak'] = fuzz.trapmf(kualitas_makanan.universe, [0, 0, 2, 4])
kualitas_makanan['biasa_saja'] = fuzz.trapmf(kualitas_makanan.universe, [2, 4, 6, 8])
kualitas_makanan['enak'] = fuzz.trapmf(kualitas_makanan.universe, [5, 7, 9, 10])
kualitas_makanan['sangat_enak'] = fuzz.trapmf(kualitas_makanan.universe, [8, 9, 10, 10])

tip_persentase['kecil'] = fuzz.trimf(tip_persentase.universe, [0, 5, 10])
tip_persentase['sedang'] = fuzz.trimf(tip_persentase.universe, [7, 12.5, 18])
tip_persentase['besar'] = fuzz.trimf(tip_persentase.universe, [15, 20, 25])

rules_list = [
    ctrl.Rule(kualitas_pelayanan['buruk'] | kualitas_makanan['tidak_enak'], tip_persentase['kecil']),
    ctrl.Rule(kualitas_pelayanan['cukup'] & kualitas_makanan['biasa_saja'], tip_persentase['sedang']),
    ctrl.Rule(kualitas_pelayanan['baik'] & kualitas_makanan['enak'], tip_persentase['sedang']),
    ctrl.Rule(kualitas_pelayanan['sangat_baik'] & kualitas_makanan['sangat_enak'], tip_persentase['besar']),
    ctrl.Rule(kualitas_pelayanan['sangat_baik'] | kualitas_makanan['sangat_enak'], tip_persentase['besar']),
    ctrl.Rule(kualitas_pelayanan['cukup'] & kualitas_makanan['enak'], tip_persentase['sedang']),
    ctrl.Rule(kualitas_pelayanan['baik'] & kualitas_makanan['sangat_enak'], tip_persentase['besar']),
    ctrl.Rule(kualitas_pelayanan['buruk'], tip_persentase['kecil']),
    ctrl.Rule(kualitas_pelayanan['sangat_baik'], tip_persentase['besar']),
    ctrl.Rule(kualitas_pelayanan['cukup'] & kualitas_makanan['tidak_enak'], tip_persentase['kecil']),
    ctrl.Rule(kualitas_pelayanan['baik'] & kualitas_makanan['biasa_saja'], tip_persentase['sedang'])
]
sistem_kontrol_tip = ctrl.ControlSystem(rules_list)

class FuzzyTipApp:
    def __init__(self, master):
        self.master = master
        master.title("Kalkulator Tip Fuzzy Modern")
        master.geometry("800x950")

        self.simulasi_terakhir = None
        self.default_pelayanan = 7.0
        self.default_makanan = 8.0
        self.default_harga = "100000.00"

        self.style = ttk.Style.get_instance()
        self.colors = self.style.colors

        main_frame = ttk.Frame(master, padding=(20, 20))
        main_frame.pack(expand=True, fill=tk.BOTH)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Kalkulator Tip Cerdas", font="-size 20 -weight bold").pack(side=LEFT)
        ttk.Label(header_frame, text="berbasis Logika Fuzzy", font="-size 12").pack(side=LEFT, pady=(5,0), padx=10)

        input_frame = ttk.LabelFrame(main_frame, text=" Penilaian Anda ", padding=20)
        input_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(input_frame, text="Kualitas Pelayanan (0-10):").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.pelayanan_var = tk.DoubleVar(value=self.default_pelayanan)
        self.pelayanan_scale = ttk.Scale(input_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.pelayanan_var, length=200, bootstyle=SECONDARY)
        self.pelayanan_scale.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.pelayanan_label_val = ttk.Label(input_frame, text=f"{self.pelayanan_var.get():.1f}", font="-weight bold")
        self.pelayanan_label_val.grid(row=0, column=2, padx=10, pady=10)
        self.pelayanan_scale.configure(command=lambda val: self.pelayanan_label_val.config(text=f"{float(val):.1f}"))
        
        ttk.Label(input_frame, text="Kualitas Makanan (0-10):").grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.makanan_var = tk.DoubleVar(value=self.default_makanan)
        self.makanan_scale = ttk.Scale(input_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.makanan_var, length=200, bootstyle=SECONDARY)
        self.makanan_scale.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        self.makanan_label_val = ttk.Label(input_frame, text=f"{self.makanan_var.get():.1f}", font="-weight bold")
        self.makanan_label_val.grid(row=1, column=2, padx=10, pady=10)
        self.makanan_scale.configure(command=lambda val: self.makanan_label_val.config(text=f"{float(val):.1f}"))
        
        ttk.Label(input_frame, text="Total Harga Makanan (Rp):").grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.harga_var = tk.StringVar(value=self.default_harga)
        self.harga_entry = ttk.Entry(input_frame, textvariable=self.harga_var, width=25)
        self.harga_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        self.details_visible = tk.BooleanVar(value=False)
        self.toggle_button = ttk.Checkbutton(main_frame, text="Tampilkan Detail Sistem Fuzzy ▼", variable=self.details_visible, command=self.toggle_details, bootstyle="info-toolbutton")
        self.toggle_button.pack(fill='x', pady=(15, 5))
        self.detail_frame = ttk.Frame(main_frame)
        self._create_detail_widgets()
        self._update_membership_graphs() 

        self.hitung_button = ttk.Button(main_frame, text="Hitung Rekomendasi Tip", command=self.hitung_tip, bootstyle=PRIMARY, padding=10)
        self.hitung_button.pack(pady=15, fill=tk.X)

        output_frame = ttk.LabelFrame(main_frame, text=" Hasil Rekomendasi ", padding=20)
        output_frame.pack(pady=5, fill=tk.X)
        self.hasil_persen_label = ttk.Label(output_frame, text="Persentase Tip: - %", font="-size 14 -weight bold", bootstyle=SUCCESS)
        self.hasil_persen_label.pack(pady=5)
        self.hasil_jumlah_label = ttk.Label(output_frame, text="Jumlah Tip: Rp -", font="-size 14 -weight bold", bootstyle=SUCCESS)
        self.hasil_jumlah_label.pack(pady=5)
        self.feedback_label = ttk.Label(output_frame, text="Silakan masukkan penilaian dan klik hitung.")
        self.feedback_label.pack(pady=10)

        secondary_action_frame = ttk.Frame(main_frame)
        secondary_action_frame.pack(pady=15, fill=tk.X)
        
        self.tampil_grafik_button = ttk.Button(secondary_action_frame, text="Tampilkan Grafik Output", command=self.tampilkan_grafik, state=DISABLED, bootstyle="info")
        self.tampil_grafik_button.pack(side=tk.LEFT, padx=(0,5), fill=tk.X, expand=True)
        self.bersihkan_button = ttk.Button(secondary_action_frame, text="Bersihkan", command=self.bersihkan_perhitungan, bootstyle="danger-outline")
        self.bersihkan_button.pack(side=tk.LEFT, padx=(5,0), fill=tk.X, expand=True)
        
    def _create_detail_widgets(self):
        rules_frame = ttk.LabelFrame(self.detail_frame, text=" Basis Aturan (Rule Base) ", padding=10)
        rules_frame.pack(fill='x', expand=True, pady=5)
        rules_text_content = "\n".join([f"{i+1}. {str(rule).splitlines()[0]}" for i, rule in enumerate(rules_list)])
        rules_text = tk.Text(rules_frame, height=8, width=80, wrap=tk.WORD, font="Courier 10", relief=FLAT, bg=self.colors.get('bg'))
        rules_text.insert(tk.END, rules_text_content)
        rules_text.config(state=DISABLED)
        scrollbar = ttk.Scrollbar(rules_frame, command=rules_text.yview, bootstyle="secondary-round")
        rules_text['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        rules_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        graphs_frame = ttk.LabelFrame(self.detail_frame, text=" Grafik Fungsi Keanggotaan ", padding=10)
        graphs_frame.pack(fill='both', expand=True, pady=5)
        graphs_canvas = tk.Canvas(graphs_frame, height=400, bg=self.colors.get('bg'), highlightthickness=0) 
        graphs_scrollbar = ttk.Scrollbar(graphs_frame, orient="vertical", command=graphs_canvas.yview, bootstyle="secondary-round")
        graphs_canvas.configure(yscrollcommand=graphs_scrollbar.set)
        graphs_scrollbar.pack(side="right", fill="y")
        graphs_canvas.pack(side="left", fill="both", expand=True)
        graphs_content_frame = ttk.Frame(graphs_canvas)
        graphs_window_id = graphs_canvas.create_window((0, 0), window=graphs_content_frame, anchor="nw")
        graphs_content_frame.bind("<Configure>", lambda e: graphs_canvas.configure(scrollregion=graphs_canvas.bbox("all")))
        graphs_canvas.bind("<Configure>", lambda e: graphs_canvas.itemconfig(graphs_window_id, width=e.width))

        plot_figsize = (7, 3)
        self.fig_pelayanan, self.ax_pelayanan = plt.subplots(figsize=plot_figsize)
        self.canvas_pelayanan = FigureCanvasTkAgg(self.fig_pelayanan, master=graphs_content_frame)
        self.canvas_pelayanan.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.fig_makanan, self.ax_makanan = plt.subplots(figsize=plot_figsize)
        self.canvas_makanan = FigureCanvasTkAgg(self.fig_makanan, master=graphs_content_frame)
        self.canvas_makanan.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.fig_output, self.ax_output = plt.subplots(figsize=plot_figsize)
        self.canvas_output = FigureCanvasTkAgg(self.fig_output, master=graphs_content_frame)
        self.canvas_output.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=2)
        
        plt.close('all')

    def _update_membership_graphs(self, pelayanan_val=None, makanan_val=None):
        plot_colors = [self.colors.primary, self.colors.info, self.colors.success, self.colors.warning, self.colors.danger]
        for i, (ax, fig, canvas, data, title, val) in enumerate([
            (self.ax_pelayanan, self.fig_pelayanan, self.canvas_pelayanan, kualitas_pelayanan, 'Input: Kualitas Pelayanan', pelayanan_val),
            (self.ax_makanan, self.fig_makanan, self.canvas_makanan, kualitas_makanan, 'Input: Kualitas Makanan', makanan_val),
            (self.ax_output, self.fig_output, self.canvas_output, tip_persentase, 'Output: Persentase Tip', None)
        ]):
            ax.clear(); fig.set_facecolor(self.colors.get('bg')); ax.set_facecolor(self.colors.get('bg'))
            for j, term in enumerate(data.terms):
                ax.plot(data.universe, data[term].mf, label=term, color=plot_colors[j % len(plot_colors)], linewidth=2)
            if val is not None:
                for term in data.terms:
                    memb_degree = fuzz.interp_membership(data.universe, data[term].mf, val)
                    if memb_degree > 0:
                        ax.vlines(val, 0, memb_degree, color=self.colors.secondary, linestyle='--')
                        ax.hlines(memb_degree, 0, val, color=self.colors.secondary, linestyle='--')
                        ax.plot(val, memb_degree, marker='o', color=self.colors.fg, markersize=8)
            ax.set_title(title, color=self.colors.fg, fontsize=12, fontweight='bold')
            ax.tick_params(colors=self.colors.secondary)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color(self.colors.secondary); ax.spines['left'].set_color(self.colors.secondary)
            legend = ax.legend()
            for text in legend.get_texts(): text.set_color(self.colors.fg)
            legend.get_frame().set_alpha(0)
            fig.tight_layout(); canvas.draw()

    def toggle_details(self):
        if self.details_visible.get():
            self.detail_frame.pack(before=self.hitung_button, fill='both', expand=True, pady=(5,15), padx=2)
            self.toggle_button.config(text="Sembunyikan Detail Sistem Fuzzy ▲")
        else:
            self.detail_frame.pack_forget()
            self.toggle_button.config(text="Tampilkan Detail Sistem Fuzzy ▼")

    def hitung_tip(self):
        try:
            pelayanan_val = self.pelayanan_var.get()
            makanan_val = self.makanan_var.get()

            penentu_tip_sim = ctrl.ControlSystemSimulation(sistem_kontrol_tip)
            penentu_tip_sim.input['kualitas_pelayanan'] = pelayanan_val
            penentu_tip_sim.input['kualitas_makanan'] = makanan_val
            penentu_tip_sim.compute()
            self.simulasi_terakhir = penentu_tip_sim
            
            harga_val = float(self.harga_var.get())
            if harga_val < 0: messagebox.showerror("Input Error", "Total harga makanan tidak boleh negatif."); self.bersihkan_perhitungan(); return

            self._update_membership_graphs(pelayanan_val, makanan_val)

            hasil_tip_persen = self.simulasi_terakhir.output['tip_persentase']
            nilai_tip_absolut = (hasil_tip_persen / 100) * harga_val
            self.hasil_persen_label.config(text=f"Persentase Tip: {hasil_tip_persen:.2f}%")
            self.hasil_jumlah_label.config(text=f"Jumlah Tip: Rp {nilai_tip_absolut:,.2f}")
            if hasil_tip_persen < 10: self.feedback_label.config(text="Tip ini tergolong kecil.", bootstyle=(INFO))
            elif hasil_tip_persen < 18: self.feedback_label.config(text="Tip ini tergolong sedang.", bootstyle=(SUCCESS))
            else: self.feedback_label.config(text="Tip ini tergolong besar. Luar biasa!", bootstyle=(WARNING))
            self.tampil_grafik_button.config(state=NORMAL)
        except (ValueError, TypeError): messagebox.showerror("Input Error", "Pastikan input harga makanan adalah angka yang valid."); self.bersihkan_perhitungan()
        except Exception as e: messagebox.showerror("Error", f"Terjadi kesalahan: {e}"); self.bersihkan_perhitungan()
    
    def tampilkan_grafik(self):
        if self.simulasi_terakhir:
            tip_persentase.view(sim=self.simulasi_terakhir)
            plt.show() 
        else:
            messagebox.showinfo("Info", "Tidak ada data perhitungan untuk ditampilkan.")

    def bersihkan_perhitungan(self):
        self.pelayanan_var.set(self.default_pelayanan)
        self.makanan_var.set(self.default_makanan)
        self.harga_var.set(self.default_harga)
        self.pelayanan_label_val.config(text=f"{self.default_pelayanan:.1f}")
        self.makanan_label_val.config(text=f"{self.default_makanan:.1f}")
        self.hasil_persen_label.config(text="Persentase Tip: - %")
        self.hasil_jumlah_label.config(text="Jumlah Tip: Rp -")
        self.feedback_label.config(text="Silakan masukkan penilaian dan klik hitung.", bootstyle=DEFAULT)
        self.tampil_grafik_button.config(state=DISABLED)
        self.simulasi_terakhir = None
        self._update_membership_graphs()

if __name__ == '__main__':
    plt.ioff()
    root = ttk.Window(themename="litera")
    app = FuzzyTipApp(root)
    root.mainloop()