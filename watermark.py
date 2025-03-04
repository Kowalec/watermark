import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from typing import List, Tuple

class WatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("Image Watermark Tool")
        
        self.watermark_path = ""
        self.image_paths = []
        self.output_dir = ""
        self.preview_image = None
        self.preview_photo = None
        self.current_preview_index = 0
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container with two panels
        main_container = ttk.PanedWindow(self.root, orient='horizontal')
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # Right panel for preview
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=2)
        
        # Watermark selection
        ttk.Button(left_panel, text="Select Watermark",
                  command=self.select_watermark).pack(pady=5, fill="x")
        
        # Images selection and queue
        ttk.Button(left_panel, text="Add Images to Queue",
                  command=self.select_images).pack(pady=5, fill="x")
        
        # Queue display
        queue_frame = ttk.LabelFrame(left_panel, text="Image Queue")
        queue_frame.pack(pady=5, fill="both", expand=True)
        
        # Queue listbox with scrollbar
        self.queue_listbox = tk.Listbox(queue_frame, selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_listbox.yview)
        self.queue_listbox.configure(yscrollcommand=scrollbar.set)
        self.queue_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.queue_listbox.bind('<<ListboxSelect>>', self.on_queue_select)
        
        # Queue controls
        queue_controls = ttk.Frame(left_panel)
        queue_controls.pack(pady=5, fill="x")
        ttk.Button(queue_controls, text="Remove Selected",
                  command=self.remove_selected).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(queue_controls, text="Clear Queue",
                  command=self.clear_queue).pack(side="left", fill="x", expand=True, padx=2)
        
        # Output directory
        ttk.Button(left_panel, text="Output Directory",
                  command=self.select_output_dir).pack(pady=5, fill="x")
        
        # Watermark size
        size_frame = ttk.Frame(left_panel)
        size_frame.pack(pady=5, fill="x")
        ttk.Label(size_frame, text="Watermark Size (%)").pack(side="left")
        self.size_var = tk.StringVar(value="20")
        ttk.Entry(size_frame, textvariable=self.size_var, width=5).pack(side="left", padx=5)
        
        # Watermark opacity
        opacity_frame = ttk.Frame(left_panel)
        opacity_frame.pack(pady=5, fill="x")
        ttk.Label(opacity_frame, text="Opacity: ").pack(side="left")
        self.opacity_var = tk.IntVar(value=100)
        opacity_slider = ttk.Scale(opacity_frame, from_=0, to=100, variable=self.opacity_var,
                                 orient="horizontal", command=self.update_preview)
        opacity_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        # Position selection
        pos_frame = ttk.LabelFrame(left_panel, text="Watermark Position")
        pos_frame.pack(pady=5, fill="x")
        
        self.position_var = tk.StringVar(value="bottom_right")
        positions = [("Top Left", "top_left"), ("Top Right", "top_right"),
                    ("Center", "center"),
                    ("Bottom Left", "bottom_left"), ("Bottom Right", "bottom_right")]
        
        for pos_text, pos_value in positions:
            ttk.Radiobutton(pos_frame, text=pos_text,
                           variable=self.position_var, value=pos_value,
                           command=self.update_preview).pack(anchor="w")
        
        # Offset
        offset_frame = ttk.Frame(left_panel)
        offset_frame.pack(pady=5, fill="x")
        ttk.Label(offset_frame, text="Offset (px)").pack(side="left")
        self.offset_var = tk.StringVar(value="10")
        ttk.Entry(offset_frame, textvariable=self.offset_var, width=5).pack(side="left", padx=5)
        
        # Format selection
        format_frame = ttk.LabelFrame(left_panel, text="Output Format")
        format_frame.pack(pady=5, fill="x")
        
        self.format_var = tk.StringVar(value="png")
        for fmt in ["jpg", "png", "webp"]:
            ttk.Radiobutton(format_frame, text=fmt.upper(),
                           variable=self.format_var, value=fmt).pack(anchor="w")
        
        # Process button
        ttk.Button(left_panel, text="Process Queue",
                  command=self.process_images).pack(pady=10, fill="x")
        
        # Preview area
        preview_frame = ttk.LabelFrame(right_panel, text="Preview")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(fill="both", expand=True)
        
        # Preview navigation
        nav_frame = ttk.Frame(right_panel)
        nav_frame.pack(fill="x", pady=5)
        ttk.Button(nav_frame, text="Previous", command=self.prev_preview).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Next", command=self.next_preview).pack(side="left")
        
        # Bind events for live preview updates
        self.size_var.trace_add("write", lambda *args: self.update_preview())
        self.offset_var.trace_add("write", lambda *args: self.update_preview())
    
    def select_watermark(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.watermark_path = path
            self.update_preview()
    
    def select_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
        if paths:
            self.image_paths.extend(paths)
            self.update_queue_display()
            if len(self.image_paths) == len(paths):  # First images added
                self.update_preview()
    
    def update_queue_display(self):
        self.queue_listbox.delete(0, tk.END)
        for path in self.image_paths:
            self.queue_listbox.insert(tk.END, os.path.basename(path))
    
    def remove_selected(self):
        selection = self.queue_listbox.curselection()
        if selection:
            index = selection[0]
            self.image_paths.pop(index)
            self.update_queue_display()
            self.update_preview()
    
    def clear_queue(self):
        self.image_paths = []
        self.update_queue_display()
        self.update_preview()
    
    def on_queue_select(self, event):
        selection = self.queue_listbox.curselection()
        if selection:
            self.current_preview_index = selection[0]
            self.update_preview()
    
    def prev_preview(self):
        if self.image_paths:
            self.current_preview_index = (self.current_preview_index - 1) % len(self.image_paths)
            self.queue_listbox.selection_clear(0, tk.END)
            self.queue_listbox.selection_set(self.current_preview_index)
            self.queue_listbox.see(self.current_preview_index)
            self.update_preview()
    
    def next_preview(self):
        if self.image_paths:
            self.current_preview_index = (self.current_preview_index + 1) % len(self.image_paths)
            self.queue_listbox.selection_clear(0, tk.END)
            self.queue_listbox.selection_set(self.current_preview_index)
            self.queue_listbox.see(self.current_preview_index)
            self.update_preview()
    
    def select_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path
    
    def update_preview(self, *args):
        if not self.image_paths:
            self.preview_label.configure(text="No images in queue")
            return
        
        try:
            # Load and resize preview image
            preview_image_path = self.image_paths[self.current_preview_index]
            img = Image.open(preview_image_path).convert("RGBA")
            preview_size = (800, 800)
            img.thumbnail(preview_size, Image.Resampling.LANCZOS)
            
            if self.watermark_path:
                watermark = Image.open(self.watermark_path).convert("RGBA")
                try:
                    watermark_size = int(float(self.size_var.get()) / 100 * img.size[0])
                except ValueError:
                    watermark_size = int(0.2 * img.size[0])
                
                watermark_ratio = watermark.size[1] / watermark.size[0]
                new_watermark_size = (watermark_size, int(watermark_size * watermark_ratio))
                watermark = watermark.resize(new_watermark_size, Image.Resampling.LANCZOS)
                
                # Apply opacity
                opacity = self.opacity_var.get()
                if opacity < 100:
                    watermark.putalpha(Image.eval(watermark.getchannel('A'), 
                                                lambda x: int(x * opacity / 100)))
            else:
                try:
                    watermark_size = int(float(self.size_var.get()) / 100 * img.size[0])
                except ValueError:
                    watermark_size = int(0.2 * img.size[0])
                
                watermark_height = int(watermark_size * 0.75)
                watermark = Image.new('RGBA', (watermark_size, watermark_height), 
                                    (128, 128, 128, int(128 * self.opacity_var.get() / 100)))
            
            # Calculate position
            position = self.get_watermark_position(img.size, watermark.size)
            
            # Create preview
            preview = img.copy()
            preview.paste(watermark, position, watermark)
            
            # Update preview label
            self.preview_photo = ImageTk.PhotoImage(preview)
            self.preview_label.configure(image=self.preview_photo)
            
        except Exception as e:
            self.preview_label.configure(text=str(e))
    
    def get_watermark_position(self, img_size: Tuple[int, int], watermark_size: Tuple[int, int]) -> Tuple[int, int]:
        try:
            offset = int(self.offset_var.get())
        except ValueError:
            offset = 10
        position = self.position_var.get()
        
        if position == "top_left":
            return (offset, offset)
        elif position == "top_right":
            return (img_size[0] - watermark_size[0] - offset, offset)
        elif position == "bottom_left":
            return (offset, img_size[1] - watermark_size[1] - offset)
        elif position == "bottom_right":
            return (img_size[0] - watermark_size[0] - offset,
                   img_size[1] - watermark_size[1] - offset)
        else:  # center
            return ((img_size[0] - watermark_size[0]) // 2,
                   (img_size[1] - watermark_size[1]) // 2)
    
    def process_images(self):
        if not all([self.watermark_path, self.image_paths, self.output_dir]):
            messagebox.showerror("Error", "Please select watermark, images, and output directory")
            return
        
        try:
            watermark = Image.open(self.watermark_path).convert("RGBA")
            
            for img_path in self.image_paths:
                # Open and convert image to RGBA
                img = Image.open(img_path).convert("RGBA")
                
                # Resize watermark
                watermark_size = int(float(self.size_var.get()) / 100 * img.size[0])
                watermark_ratio = watermark.size[1] / watermark.size[0]
                new_watermark_size = (watermark_size, int(watermark_size * watermark_ratio))
                resized_watermark = watermark.resize(new_watermark_size, Image.Resampling.LANCZOS)
                
                # Apply opacity
                opacity = self.opacity_var.get()
                if opacity < 100:
                    resized_watermark.putalpha(Image.eval(resized_watermark.getchannel('A'), 
                                                        lambda x: int(x * opacity / 100)))
                
                # Calculate position
                position = self.get_watermark_position(img.size, resized_watermark.size)
                
                # Create new transparent layer
                watermark_layer = Image.new('RGBA', img.size, (0,0,0,0))
                watermark_layer.paste(resized_watermark, position)
                
                # Combine images
                output = Image.alpha_composite(img, watermark_layer)
                
                # Save with selected format
                output_format = self.format_var.get()
                if output_format == "jpg":
                    output = output.convert("RGB")
                
                filename = os.path.splitext(os.path.basename(img_path))[0]
                output_path = os.path.join(self.output_dir, f"{filename}_watermarked.{output_format}")
                output.save(output_path, format=output_format.upper())
            
            messagebox.showinfo("Success", "Images processed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = WatermarkApp()
    app.root.mainloop()