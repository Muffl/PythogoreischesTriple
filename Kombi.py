import math
import tkinter as tk
from tkinter import ttk


def find_pythagorean_triplets(max_sum: int) -> list[tuple[int, int, int]]:
	"""Return all (x, y, z) with x < y < z, x^2 + y^2 = z^2 and x + y + z <= max_sum."""
	triplets: list[tuple[int, int, int]] = []

	for x in range(1, max_sum - 1):
		for y in range(x + 1, max_sum):
			z_sq = x * x + y * y
			z = int(z_sq**0.5)
			if z * z == z_sq and z > y and x + y + z <= max_sum:
				triplets.append((x, y, z))

	return triplets


class CombinedApp:
	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Pythagoras - Dreieck und Tripel")

		self.a_var = tk.StringVar(value="3")
		self.b_var = tk.StringVar(value="4")
		self.max_sum_var = tk.StringVar(value="100")
		self.msg_var = tk.StringVar(value="")

		form = ttk.Frame(root, padding=10)
		form.pack(side=tk.TOP, fill=tk.X)

		ttk.Label(form, text="Kathete a:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
		ttk.Entry(form, textvariable=self.a_var, width=10).grid(row=0, column=1, sticky=tk.W)

		ttk.Label(form, text="Kathete b:").grid(row=0, column=2, sticky=tk.W, padx=4, pady=4)
		ttk.Entry(form, textvariable=self.b_var, width=10).grid(row=0, column=3, sticky=tk.W)

		ttk.Button(form, text="Zeichnen", command=self.draw).grid(
			row=0, column=4, sticky=tk.W, padx=8
		)

		ttk.Label(form, textvariable=self.msg_var, foreground="#b00020").grid(
			row=1, column=0, columnspan=5, sticky=tk.W, padx=4
		)

		main = ttk.Frame(root, padding=10)
		main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.canvas = tk.Canvas(main, width=520, height=380, background="#f8f8f8")
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
		self.canvas.bind("<Configure>", self.on_resize)

		side = ttk.Frame(main)
		side.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		max_frame = ttk.Frame(side)
		max_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 6))
		ttk.Label(max_frame, text="Max Summe:").grid(row=0, column=0, sticky=tk.W, padx=(0, 4))
		ttk.Entry(max_frame, textvariable=self.max_sum_var, width=10).grid(
			row=0, column=1, sticky=tk.W, padx=(0, 6)
		)
		ttk.Button(max_frame, text="Tripel finden", command=self.find_triplets).grid(
			row=0, column=2, sticky=tk.W
		)

		ttk.Label(side, text="Gefundene Tripel:").pack(anchor=tk.W)
		columns = ("idx", "x", "y", "z", "sum", "prod")
		self.triplet_tree = ttk.Treeview(side, columns=columns, show="headings")
		self.triplet_tree.heading("idx", text="Nr")
		self.triplet_tree.heading("x", text="x")
		self.triplet_tree.heading("y", text="y")
		self.triplet_tree.heading("z", text="z")
		self.triplet_tree.heading("sum", text="Summe")
		self.triplet_tree.heading("prod", text="Produkt")

		self.triplet_tree.column("idx", width=40, anchor=tk.CENTER)
		self.triplet_tree.column("x", width=50, anchor=tk.CENTER)
		self.triplet_tree.column("y", width=50, anchor=tk.CENTER)
		self.triplet_tree.column("z", width=50, anchor=tk.CENTER)
		self.triplet_tree.column("sum", width=70, anchor=tk.CENTER)
		self.triplet_tree.column("prod", width=90, anchor=tk.CENTER)

		self.triplet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		scroll = ttk.Scrollbar(side, orient=tk.VERTICAL, command=self.triplet_tree.yview)
		scroll.pack(side=tk.RIGHT, fill=tk.Y)
		self.triplet_tree.configure(yscrollcommand=scroll.set)

		self.draw()
		self.find_triplets()

	def parse_triangle_inputs(self) -> tuple[float, float] | None:
		try:
			a = float(self.a_var.get().replace(",", "."))
			b = float(self.b_var.get().replace(",", "."))
		except ValueError:
			self.msg_var.set("Bitte Zahlen fuer a und b eingeben.")
			return None

		if a <= 0 or b <= 0:
			self.msg_var.set("a und b muessen groesser als 0 sein.")
			return None

		self.msg_var.set("")
		return a, b

	def parse_max_sum(self) -> int | None:
		try:
			value = int(self.max_sum_var.get().strip())
		except ValueError:
			self.msg_var.set("Bitte eine ganze Zahl fuer die Max Summe eingeben.")
			return None

		if value <= 0:
			self.msg_var.set("Die Max Summe muss groesser als 0 sein.")
			return None

		self.msg_var.set("")
		return value

	def on_resize(self, _event: tk.Event) -> None:
		self.draw()

	def draw(self) -> None:
		data = self.parse_triangle_inputs()
		if data is None:
			self.canvas.delete("all")
			return

		a, b = data
		c = math.hypot(a, b)

		self.canvas.delete("all")

		padding = 50
		width = max(1, self.canvas.winfo_width())
		height = max(1, self.canvas.winfo_height())

		max_a = width - 2 * padding
		max_b = height - 2 * padding
		scale = min(max_a / a, max_b / b)

		ax = padding
		ay = height - padding
		bx = ax + a * scale
		by = ay
		cx = ax
		cy = ay - b * scale

		self.canvas.create_polygon(ax, ay, bx, by, cx, cy, outline="#1f2937", fill="#e5e7eb")
		self.canvas.create_line(ax, ay, bx, by, width=3, fill="#111827")
		self.canvas.create_line(ax, ay, cx, cy, width=3, fill="#111827")
		self.canvas.create_line(bx, by, cx, cy, width=3, fill="#111827")

		marker = 22
		self.canvas.create_line(ax, ay, ax + marker, ay, width=2, fill="#111827")
		self.canvas.create_line(ax + marker, ay, ax + marker, ay - marker, width=2, fill="#111827")
		self.canvas.create_line(ax + marker, ay - marker, ax, ay - marker, width=2, fill="#111827")

		a_label_x = (ax + bx) / 2
		a_label_y = ay + 18
		b_label_x = ax - 22
		b_label_y = (ay + cy) / 2
		dx = cx - bx
		dy = cy - by
		length = max(1.0, math.hypot(dx, dy))
		nx = -dy / length
		ny = dx / length
		mid_x = (bx + cx) / 2
		mid_y = (by + cy) / 2
		centroid_x = (ax + bx + cx) / 3
		centroid_y = (ay + by + cy) / 3
		if (mid_x - centroid_x) * nx + (mid_y - centroid_y) * ny < 0:
			nx = -nx
			ny = -ny
		offset = max(18, min(32, 0.08 * min(width, height)))
		right_shift = max(10, min(26, 0.04 * width))
		c_label_x = mid_x + nx * offset + right_shift
		c_label_y = mid_y + ny * offset

		self.canvas.create_text(
			a_label_x,
			a_label_y,
			text=f"a = {a:g}",
			fill="#111827",
			font=("Segoe UI", 11, "bold"),
		)
		self.canvas.create_text(
			b_label_x,
			b_label_y,
			text=f"b = {b:g}",
			fill="#111827",
			font=("Segoe UI", 11, "bold"),
			angle=90,
		)
		self.canvas.create_text(
			c_label_x,
			c_label_y,
			text=f"c = {c:g}",
			fill="#111827",
			font=("Segoe UI", 11, "bold"),
		)

	def find_triplets(self) -> None:
		max_sum = self.parse_max_sum()
		if max_sum is None:
			return

		triplets = find_pythagorean_triplets(max_sum)
		for item in self.triplet_tree.get_children():
			self.triplet_tree.delete(item)
		if not triplets:
			self.msg_var.set("Keine Tripel gefunden.")
			return

		for i, (x, y, z) in enumerate(triplets, start=1):
			sum_value = x + y + z
			prod_value = x * y * z
			self.triplet_tree.insert(
				"",
				tk.END,
				values=(i, x, y, z, sum_value, prod_value),
			)
		self.msg_var.set(f"{len(triplets)} Tripel gefunden.")


def main() -> None:
	root = tk.Tk()
	app = CombinedApp(root)
	root.minsize(900, 420)
	root.mainloop()


if __name__ == "__main__":
	main()
