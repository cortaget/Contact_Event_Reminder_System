from ui.main_window import MainWindow
import sys

if __name__ == '__main__':
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
