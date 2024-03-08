import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from geometry import circle_centers_gui, angle_from_point_gui, calculate_end_angle_gui, dist

class DrawingApp:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.root.title("Drawing Tool")

        self.mode = "line"  # Default mode is line
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        self.coordinates = []  # Store lines and circle arcs [(type, points), (type, points), ...]

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        #line button
        self.line_button = tk.Button(self.root, text="Line", command=lambda: self.set_mode("line"), relief=tk.SUNKEN)
        self.line_button.pack(side=tk.LEFT, padx=5, pady=10)
        #circle arc clockwise button
        self.circle_arc_cw_button = tk.Button(self.root, text="Clockwise Circle Arc", command=lambda: self.set_mode("circle_arc_cw"))
        self.circle_arc_cw_button.pack(side=tk.LEFT, padx=5, pady=10)
        #circle arc counter-clockwise button
        self.circle_arc_ccw_button = tk.Button(self.root, text="Counter-Clockwise Circle Arc", command=lambda: self.set_mode("circle_arc_ccw"))
        self.circle_arc_ccw_button.pack(side=tk.LEFT, padx=5, pady=10)
        #radius entry
        self.radius_label = tk.Label(self.root, text="Enter Radius:")
        self.radius_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.radius_entry = tk.Entry(self.root)
        self.radius_entry.pack(side=tk.LEFT, padx=5, pady=10)
        #save button
        self.save_button = tk.Button(self.root, text="Save Drawing", command=self.save_drawing)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=10)
        #back button
        self.back_button = tk.Button(self.root, text="Back", command=self.close_drawing)
        self.back_button.pack(side=tk.RIGHT, padx=5, pady=10)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.create_line(0, 200, 400, 200, fill="gray", width=1)
        self.canvas.create_line(200, 0, 200, 400, fill="gray", width=1)
        for x in range(0, 401, 10):
            self.canvas.create_line(x, 0, x, 400, fill="gray", width=1)
        for y in range(0, 401, 10):
            self.canvas.create_line(0, y, 400, y, fill="gray", width=1)        
    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        if self.mode == "line":
            self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill="black", width=2)
            self.coordinates.append(("line", [(self.start_x, self.start_y), (end_x, end_y)]))
        elif self.mode == "circle_arc_cw" or self.mode == "circle_arc_ccw":
            stringradius = self.radius_entry.get()
            if not stringradius:
                messagebox.showwarning("Warning", "Please enter a radius")
                return
            radius = int(stringradius)
            mx = (self.start_x + end_x) / 2
            my = (self.start_y + end_y) / 2
            d1 = dist(self.start_x, self.start_y, mx, my)
            if radius < d1:
                messagebox.showwarning("Warning", "Radius is too small for circle, it should be at least " + str(int(d1)))
                return
            else:
                clockwise = True if self.mode == "circle_arc_cw" else False
                self.draw_circle_arc(self.start_x, self.start_y, end_x, end_y, radius, clockwise)
                self.coordinates.append(("circle_arc", [(self.start_x, self.start_y), (end_x, end_y), radius, clockwise]))
        #todo swap start and end if end is before start
    def set_mode(self, mode):
        self.mode = mode
        # Reset relief for all buttons
        self.line_button.config(relief=tk.RAISED)
        self.circle_arc_cw_button.config(relief=tk.RAISED)
        self.circle_arc_ccw_button.config(relief=tk.RAISED)
        # Highlight the active button
        if mode == "line":
            self.line_button.config(relief=tk.SUNKEN)
        elif mode == "circle_arc_cw":
            self.circle_arc_cw_button.config(relief=tk.SUNKEN)
        elif mode == "circle_arc_ccw":
            self.circle_arc_ccw_button.config(relief=tk.SUNKEN)

    def close_drawing(self):
        self.root.destroy()
        self.parent.update_coordinates(self.coordinates)  # Update coordinates in the main GUI

    def draw_circle_arc(self, start_x, start_y, end_x, end_y, radius, clockwise):
        # 1 is clockwise, 2 is counter-clockwise
        center_x, center_y, center2_x, center2_y = circle_centers_gui(start_x, start_y, end_x, end_y, radius)
        if clockwise:
            start_angle = angle_from_point_gui(center_x, center_y, start_x, start_y)
            extent = calculate_end_angle_gui(start_x, start_y, end_x, end_y, center_x, center_y)
        else:
            start_angle = angle_from_point_gui(center2_x, center2_y, start_x, start_y)
            extent = calculate_end_angle_gui(start_x, start_y, end_x, end_y, center2_x, center2_y)    
            
        #current bugs: 
        #   when creating clockwise circle arc, if the end point is (somewhat) directly below the start point, the arc is drawn in reverse
        #   when creating counter-clockwise circle arc, if the end point is (somewhat) directly above the start point, the arc is drawn in reverse     
        
        # canvas.create_arc() has parameters:
        #   x1, y1 of top left of square enclosing (full) circle    (center.x - r, center.y - r)
        #   x2, y2 of bottom right of square                        (center.x + r, center.y + r)     
        #   start angle, extent
        #   style = 'arc'
        #   width of line
        
        if clockwise:       
            top_left_x = center_x - radius
            top_left_y = center_y - radius 
            bottom_right_x = center_x + radius
            bottom_right_y = center_y + radius   
        else:
            top_left_x = center2_x - radius
            top_left_y = center2_y - radius 
            bottom_right_x = center2_x + radius
            bottom_right_y = center2_y + radius

        self.canvas.create_arc(top_left_x, top_left_y, bottom_right_x, bottom_right_y, 
                               start=start_angle, extent=extent, style='arc', width=2)
        
    def save_drawing(self):
        gcode_str = "G00 X0 Y0 F3 \n"
        for elem in self.coordinates:
            if elem[0] == 'line':
                # translate from tkinter canvas coordinates to turtle canvas coordinates
                # canvas is 400*400 in tkinter, 800*800 in turtle
                # canvas is top-left (0, 0), turtle is bottom left (-400, -400), top right (400, 400)

                # x should be (x-200) * 2
                # y should be ((400 - y)-200) * 2 => (200 - y) * 2
                # radius should be radius * 2
                x1 = (elem[1][0][0] - 200) * 2
                x2 = (elem[1][1][0] - 200) * 2
                y1 = (200 - elem[1][0][1]) * 2
                y2 = (200 - elem[1][1][1]) * 2
                gcode_str += "G00 X" + str(x1) + " Y" + str(y1) + "\n"
                gcode_str += "G01 X" + str(x2) + " Y" + str(y2) + "\n"
            elif elem[0] == 'circle_arc':
                #("circle_arc", [(self.start_x, self.start_y), (end_x, end_y), radius, clockwise])
                x1 = (elem[1][0][0] - 200) * 2
                x2 = (elem[1][1][0] - 200) * 2
                y1 = (200 - elem[1][0][1]) * 2
                y2 = (200 - elem[1][1][1]) * 2
                radius = elem[1][2] * 2
                clockwise = elem[1][3]
                gcode_str += "G00 X" + str(x1) + " Y" + str(y1) + "\n"
                if clockwise:
                    gcode_str += "G02 X"
                else:
                    gcode_str += "G03 X"
                gcode_str += str(x2) + " Y" + str(y2) + " R" + str(radius) + "\n"
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".g", filetypes=[("G-code files", "*.g")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(gcode_str)
                print("Text saved to", file_path)
            else:
                print("Operation canceled.")
        except IOError:
            print("Error: Unable to save text.")            
                

class CNCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Machining Simulation")

        self.file_path = ""
        self.coordinates = []

        self.file_frame = tk.Frame(self.root, width=600, height=200)
        self.file_frame.pack(padx=20, pady=20)

        self.select_file_button = tk.Button(self.file_frame, text="Select File", command=self.select_file)
        self.select_file_button.pack(padx=10, pady=10)

        self.file_path_label = tk.Label(self.file_frame, text="")
        self.file_path_label.pack(padx=10, pady=10)

        self.open_drawing_button = tk.Button(self.root, text="Open Drawing Frame", command=self.open_drawing)
        self.open_drawing_button.pack(pady=10)

        self.run_simulation_button = tk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        self.run_simulation_button.pack(pady=10)

    def select_file(self):
        self.file_path = tk.filedialog.askopenfilename(initialdir="./gcode_files", title="Select Simulation File",
                                                    filetypes=(("G-code files", "*.g"), ("All files", "*.*")))
        if self.file_path:
            self.file_path_label.config(text=self.file_path)

    def open_drawing(self):
        drawing_window = tk.Toplevel(self.root)
        drawing_window.title("Drawing Frame")
        self.drawing_app = DrawingApp(drawing_window, self)

    def update_coordinates(self, coordinates):
        self.coordinates = coordinates

    def run_simulation(self):
        if self.file_path:
            # Pass file path and coordinates to the simulation process
            args = ["python3", "sim.py", self.file_path]
            subprocess.run(args)
        else:
            print("Please select a file and draw something.")

def run_gui():
    root = tk.Tk()
    app = CNCApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()


# todo: add "circle" button, which draws a circle (not an arc) with the given radius
#       use G02/03 with IJ, center is where the click is released   

     