import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class PyDivGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDiv - Advanced Linear Algebra Solver")
        self.root.geometry("850x700")
        self.root.configure(bg="#f0f2f5")

        # Header Banner (FIXED: padding=15 -> padx=15, pady=15)
        header = tk.Frame(self.root, bg="#1e293b", padx=15, pady=15)
        header.pack(fill="x")
        title_label = tk.Label(
            header, 
            text="PyDiv Linear Algebra Solver", 
            font=("Helvetica", 18, "bold"), 
            fg="#ffffff", 
            bg="#1e293b"
        )
        title_label.pack()

        # Main Layout Frame (Left: Inputs, Right: Operations)
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Left Frame: Matrix Inputs
        input_frame = ttk.LabelFrame(main_frame, text=" Matrix Inputs ", padding=10)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Matrix A Input
        ttk.Label(input_frame, text="Matrix A (Row wise, space separated):", font=("Helvetica", 10, "bold")).pack(anchor="w")
        ttk.Label(input_frame, text="Example:\n1 2 3\n4 5 6", font=("Helvetica", 8), foreground="gray").pack(anchor="w")
        self.text_a = tk.Text(input_frame, height=6, width=35, font=("Consolas", 10))
        self.text_a.pack(fill="x", pady=(2, 10))

        # Matrix B Input
        ttk.Label(input_frame, text="Matrix B / Constants Vector (Optionally used):", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.text_b = tk.Text(input_frame, height=5, width=35, font=("Consolas", 10))
        self.text_b.pack(fill="x", pady=(2, 10))

        # Scalar / Power Input
        scalar_frame = ttk.Frame(input_frame)
        scalar_frame.pack(fill="x", pady=5)
        ttk.Label(scalar_frame, text="Scalar Value (k) / Power (p):", font=("Helvetica", 9, "bold")).pack(side="left")
        self.entry_k = ttk.Entry(scalar_frame, width=10)
        self.entry_k.pack(side="left", padx=5)
        self.entry_k.insert(0, "2")

        # Right Frame: Operations Buttons
        ops_frame = ttk.LabelFrame(main_frame, text=" Operations & Properties ", padding=10)
        ops_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Analysis Button
        btn_prop = tk.Button(
            ops_frame, 
            text="🔍 Check Matrix A Properties", 
            bg="#2563eb", 
            fg="white", 
            font=("Helvetica", 10, "bold"), 
            command=self.check_properties
        )
        btn_prop.pack(fill="x", pady=(0, 10))

        # Operations Buttons Grid
        btn_grid = ttk.Frame(ops_frame)
        btn_grid.pack(fill="both", expand=True)

        buttons = [
            ("Addition (A + B)", self.matrix_add),
            ("Subtraction (A - B)", self.matrix_sub),
            ("Multiplication (A * B)", self.matrix_mul),
            ("Scalar Mult (k * A)", self.scalar_mul),
            ("Transpose (A^T)", self.transpose),
            ("Determinant (|A|)", self.determinant),
            ("Inverse (A^-1)", self.inverse),
            ("Trace (Tr(A))", self.trace),
            ("Eigenvalues & Vectors", self.eigenvalues),
            ("Matrix Power (A^k)", self.matrix_power),
            ("Solve Ax = B", self.solve_equations),
            ("Rank of Matrix A", self.rank)
        ]

        for i, (text, cmd) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ttk.Button(btn_grid, text=text, command=cmd)
            btn.grid(row=row, column=col, sticky="ew", padx=3, pady=3)

        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # Clear Button
        btn_clear = ttk.Button(ops_frame, text="🧹 Clear All Inputs", command=self.clear_all)
        btn_clear.pack(fill="x", pady=(10, 0))

        # Bottom Frame: Result Display
        result_frame = ttk.LabelFrame(main_frame, text=" Output Result ", padding=10)
        result_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.text_result = tk.Text(result_frame, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#00ff66")
        self.text_result.pack(fill="both", expand=True)

    def get_matrix(self, text_widget, name="Matrix"):
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Input Error", f"{name} field khaali hai!")
            return None
        
        try:
            lines = content.split('\n')
            matrix = []
            for line in lines:
                if line.strip():
                    row = [float(x) for x in line.strip().split()]
                    matrix.append(row)
            
            row_len = len(matrix[0])
            for r in matrix:
                if len(r) != row_len:
                    messagebox.showerror("Input Error", f"{name} ki saari rows me barabar elements hone chahiye.")
                    return None
            return np.array(matrix)
        except ValueError:
            messagebox.showerror("Input Error", f"{name} me sirf valid numbers enter karein.")
            return None

    def display_result(self, title, output):
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, f"=== {title} ===\n\n{output}")

    def clear_all(self):
        self.text_a.delete("1.0", tk.END)
        self.text_b.delete("1.0", tk.END)
        self.text_result.delete("1.0", tk.END)

    def check_properties(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is None: return

        rows, cols = A.shape
        is_square = (rows == cols)
        
        report = []
        report.append(f"• Dimensions (Shape)  : {rows} x {cols}")
        report.append(f"• Total Elements     : {A.size}")
        report.append(f"• Matrix Rank         : {np.linalg.matrix_rank(A)}")
        report.append(f"• Zero Matrix?       : {'Haan' if np.allclose(A, 0) else 'Nahi'}")

        if is_square:
            report.append("\n--- Square Matrix Properties ---")
            det = np.linalg.det(A)
            report.append(f"• Determinant (|A|)   : {round(det, 4)}")
            report.append(f"• Invertible?         : {'Haan (Non-Singular)' if not np.isclose(det, 0) else 'Nahi (Singular Matrix)'}")
            report.append(f"• Trace               : {round(np.trace(A), 4)}")
            report.append(f"• Identity Matrix?    : {'Haan' if np.allclose(A, np.eye(rows)) else 'Nahi'}")
            report.append(f"• Diagonal Matrix?    : {'Haan' if np.allclose(A, np.diag(np.diag(A))) else 'Nahi'}")
            report.append(f"• Symmetric?          : {'Haan (A = A^T)' if np.allclose(A, A.T) else 'Nahi'}")
            report.append(f"• Skew-Symmetric?     : {'Haan (A = -A^T)' if np.allclose(A, -A.T) else 'Nahi'}")
            report.append(f"• Orthogonal?         : {'Haan (A * A^T = I)' if np.allclose(np.dot(A, A.T), np.eye(rows)) else 'Nahi'}")
            report.append(f"• Upper Triangular?   : {'Haan' if np.allclose(A, np.triu(A)) else 'Nahi'}")
            report.append(f"• Lower Triangular?   : {'Haan' if np.allclose(A, np.tril(A)) else 'Nahi'}")
        else:
            report.append("\n• Type                : Rectangular Matrix (Non-Square)")

        self.display_result("Matrix Properties Report", "\n".join(report))

    def matrix_add(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        B = self.get_matrix(self.text_b, "Matrix B")
        if A is not None and B is not None:
            if A.shape == B.shape:
                self.display_result("Matrix Addition (A + B)", np.add(A, B))
            else:
                messagebox.showerror("Error", "Addition ke liye A aur B ka size same hona zaroori hai.")

    def matrix_sub(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        B = self.get_matrix(self.text_b, "Matrix B")
        if A is not None and B is not None:
            if A.shape == B.shape:
                self.display_result("Matrix Subtraction (A - B)", np.subtract(A, B))
            else:
                messagebox.showerror("Error", "Subtraction ke liye A aur B ka size same hona zaroori hai.")

    def matrix_mul(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        B = self.get_matrix(self.text_b, "Matrix B")
        if A is not None and B is not None:
            try:
                self.display_result("Matrix Multiplication (A * B)", np.dot(A, B))
            except ValueError:
                messagebox.showerror("Error", "Matrix A ke columns aur Matrix B ki rows barabar honi chahiye.")

    def scalar_mul(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            try:
                k = float(self.entry_k.get())
                self.display_result(f"Scalar Multiplication ({k} * A)", np.round(k * A, 4))
            except ValueError:
                messagebox.showerror("Error", "Valid scalar value enter karein.")

    def transpose(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            self.display_result("Matrix Transpose (A^T)", A.T)

    def determinant(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            if A.shape[0] == A.shape[1]:
                det = round(np.linalg.det(A), 4)
                self.display_result("Determinant (|A|)", f"Determinant = {det}")
            else:
                messagebox.showerror("Error", "Determinant sirf Square Matrix ka nikalta hai.")

    def inverse(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            if A.shape[0] == A.shape[1]:
                try:
                    inv = np.linalg.inv(A)
                    self.display_result("Inverse Matrix (A^-1)", np.round(inv, 4))
                except np.linalg.LinAlgError:
                    messagebox.showerror("Error", "Is matrix ka determinant 0 hai, inverse possible nahi hai.")
            else:
                messagebox.showerror("Error", "Inverse sirf Square Matrix ka nikalta hai.")

    def trace(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            if A.shape[0] == A.shape[1]:
                self.display_result("Trace of Matrix", f"Trace = {np.trace(A)}")
            else:
                messagebox.showerror("Error", "Trace sirf Square Matrix ka nikalta hai.")

    def eigenvalues(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            if A.shape[0] == A.shape[1]:
                try:
                    vals, vecs = np.linalg.eig(A)
                    res = f"Eigenvalues:\n{np.round(vals, 4)}\n\nEigenvectors (Columns):\n{np.round(vecs, 4)}"
                    self.display_result("Eigenvalues & Eigenvectors", res)
                except np.linalg.LinAlgError:
                    messagebox.showerror("Error", "Eigenvalues calculate nahi ho paaye.")
            else:
                messagebox.showerror("Error", "Eigenvalues sirf Square Matrix ke nikalte hain.")

    def matrix_power(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            if A.shape[0] == A.shape[1]:
                try:
                    p = int(float(self.entry_k.get()))
                    res = np.linalg.matrix_power(A, p)
                    self.display_result(f"Matrix Power (A^{p})", np.round(res, 4))
                except ValueError:
                    messagebox.showerror("Error", "Power me Integer number enter karein.")
            else:
                messagebox.showerror("Error", "Matrix Power sirf Square Matrix ke liye possible hai.")

    def solve_equations(self):
        A = self.get_matrix(self.text_a, "Matrix A (Coefficients)")
        B = self.get_matrix(self.text_b, "Matrix B (Constants)")
        if A is not None and B is not None:
            if A.shape[0] == A.shape[1]:
                try:
                    sol = np.linalg.solve(A, B)
                    self.display_result("Solution for Ax = B", np.round(sol, 4))
                except Exception as e:
                    messagebox.showerror("Error", f"Solve nahi ho paya: {e}")
            else:
                messagebox.showerror("Error", "Coefficient Matrix (A) Square Matrix honi chahiye.")

    def rank(self):
        A = self.get_matrix(self.text_a, "Matrix A")
        if A is not None:
            rk = np.linalg.matrix_rank(A)
            self.display_result("Rank of Matrix", f"Rank = {rk}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyDivGUI(root)
    root.mainloop()