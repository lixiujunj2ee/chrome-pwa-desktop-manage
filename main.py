import flet as ft
import os
import subprocess
import threading # Use threads instead of asynchronous operations to solve the white screen problem.
from tendo import singleton

try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException:
    sys.exit(0)

def main(page: ft.Page):
    page.title = "Chrome PWA Desktop Manager"
    page.window_width = 1000
    page.window_height = 700
    
    BASE_PATH = os.path.expanduser("~/.local/share/applications/")

    # --- State variables ---
    current_selected_file = None

    # --- UI Components ---
    detail_title = ft.Text("", weight="bold", size=14)
    content_display = ft.Text(value="", font_family="Courier New", size=13, selectable=True)
    file_list_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # --- Core logic function ---

    def refresh_all():
        """Refresh the entire page"""
        search_input.value = ""
        filter_files("")
        detail_title.value = ""
        content_display.value = ""
        page.update()

    def filter_files(search_term=""):
        file_list_column.controls.clear()
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        files = [f for f in os.listdir(BASE_PATH) if f.endswith(".desktop")]
        for f in files:
            if search_term.lower() in f.lower():
                file_list_column.controls.append(
                    ft.ListTile(
                        title=ft.Text(f, size=12),
                        on_click=lambda e, name=f: read_file_content(name),
                        dense=True
                    )
                )
        page.update()

    def read_file_content(filename):
        nonlocal current_selected_file
        current_selected_file = filename
        detail_title.value = f"{filename} - Document details"
        full_path = os.path.join(BASE_PATH, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content_display.value = f.read()
        except:
            content_display.value = "Unable to read file"
        page.update()

    # --- pop-up function area ---
    
    # 1. Add shortcut
    def add_shortcut(e):
        # 1. Define input components
        app_id = ft.TextField(label="APP_ID", hint_text="caidcmannjgahlnbpmidmiecjcoiiigg")
        app_name = ft.TextField(label="APP_NAME", hint_text="Gemini")
        file_name = ft.TextField(label="FILE_NAME", hint_text="gemini")
        
        error_msg = ft.Text(color="red", visible=False)
        loading_ring = ft.ProgressRing(width=20, height=20, visible=False)

        def run_pwa_task():
            """Run the binary file in a child thread to prevent the main interface from freezing."""
            try:
                # Get the absolute path of the binary file
                curr_dir = os.path.dirname(os.path.abspath(__file__))
                pwa_bin = os.path.join(curr_dir, "pwa")

                # Execute command
                result = subprocess.run(
                    [pwa_bin, "create", app_id.value, app_name.value, file_name.value],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    page.close(dlg)
                    refresh_all()
                else:
                    # Display error message
                    error_msg.value = f"error: {result.stderr or result.stdout}"
                    error_msg.visible = True
                    submit_btn.disabled = False
                    loading_ring.visible = False
                    page.update()

            except Exception as ex:
                error_msg.value = f"System malfunction: {str(ex)}"
                error_msg.visible = True
                submit_btn.disabled = False
                loading_ring.visible = False
                page.update()

        def on_submit(e):
            # Click to update UI status immediately
            submit_btn.disabled = True
            loading_ring.visible = True
            error_msg.visible = False
            page.update()
            
            # Start running the thread without blocking the main thread.
            threading.Thread(target=run_pwa_task, daemon=True).start()

        submit_btn = ft.ElevatedButton("Confirm Submission", on_click=on_submit)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Add shortcut"),
            content=ft.Column([
                app_id, app_name, file_name,
                ft.Row([loading_ring, error_msg], alignment="center")
            ], tight=True, width=400),
            actions=[
                submit_btn,
                ft.TextButton("Cancel", on_click=lambda _: page.close(dlg))
            ]
        )
        page.open(dlg)

    # 2. Change icon
    def change_icon(e):
        # 1. Define input components
        png_path = ft.TextField(label="APP_NAME", hint_text="/home/jey/Pictures/test.png")
        app_id = ft.TextField(label="APP_ID", hint_text="cadlkienfkclaiaibeoongdcgmdikeeg")
        
        error_msg = ft.Text(color="red", visible=False)
        loading_ring = ft.ProgressRing(width=20, height=20, visible=False)

        def run_pwa_task():
            """Run the binary file in a child thread to prevent the main interface from freezing."""
            try:
                # 
                curr_dir = os.path.dirname(os.path.abspath(__file__))
                pwa_bin = os.path.join(curr_dir, "pwa")

                # 
                result = subprocess.run(
                    [pwa_bin, "icon", png_path.value, app_id.value],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    page.close(dlg)
                    refresh_all()
                else:
                    #
                    error_msg.value = f"error: {result.stderr or result.stdout}"
                    error_msg.visible = True
                    submit_btn.disabled = False
                    loading_ring.visible = False
                    page.update()

            except Exception as ex:
                error_msg.value = f"System malfunction: {str(ex)}"
                error_msg.visible = True
                submit_btn.disabled = False
                loading_ring.visible = False
                page.update()

        def on_submit(e):
            #
            submit_btn.disabled = True
            loading_ring.visible = True
            error_msg.visible = False
            page.update()
            
            # Start running the thread without blocking the main thread.
            threading.Thread(target=run_pwa_task, daemon=True).start()

        submit_btn = ft.ElevatedButton("Confirm Submission", on_click=on_submit)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Change app icon"),
            content=ft.Column([
                png_path, app_id,
                ft.Row([loading_ring, error_msg], alignment="center")
            ], tight=True, width=400),
            actions=[
                submit_btn,
                ft.TextButton("Cancel", on_click=lambda _: page.close(dlg))
            ]
        )
        page.open(dlg)
    
    # 3. Delete shortcut
    def delete_shortcut(e):
        if not current_selected_file: return
        
        def confirm(e):
            os.remove(os.path.join(BASE_PATH, current_selected_file))
            page.close(dlg)
            refresh_all()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirm deletion"),
            content=ft.Text(f"Confirm deletion {current_selected_file} ？"),
            actions=[
                ft.TextButton("Sure", on_click=confirm),
                ft.TextButton("Cancel", on_click=lambda _: page.close(dlg)),
            ],
        )
        page.open(dlg)

    # --- UI ---
    search_input = ft.TextField(label="Search...", on_change=lambda e: filter_files(search_input.value), height=40)

    page.add(
        ft.Row([
            # left
            ft.Column([search_input, file_list_column], width=250),
            ft.VerticalDivider(width=1),
            # right
            ft.Column([
                ft.Row([
                    detail_title,
                    ft.ElevatedButton("Add", icon=ft.Icons.ADD, on_click=add_shortcut),
                    ft.ElevatedButton("Icon", icon=ft.Icons.IMAGE, on_click=change_icon),
                    ft.ElevatedButton("Dele", icon=ft.Icons.DELETE, color="red", on_click=delete_shortcut),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=1),
                ft.Container(
                    content=ft.Column([content_display], scroll=ft.ScrollMode.ALWAYS),
                    expand=True,
                    bgcolor=ft.Colors.GREY_50,
                    padding=10
                )
            ], expand=True)
        ], expand=True)
    )

    filter_files("")

ft.app(target=main)

