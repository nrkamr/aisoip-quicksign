import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime


APP_NAME = "AISOIP QuickSign"


class QuickSignApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("760x520")
        self.root.minsize(620, 420)

        self.files = []
        self.output_dir = str(Path.home() / "Documents" / "AISOIP_QuickSign")

        title = tk.Label(
            root,
            text="AISOIP QuickSign",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            root,
            text="Помощник по подготовке документов к подписанию ЭЦП"
        )
        subtitle.pack(pady=(0, 14))

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x", padx=18, pady=5)

        tk.Button(
            toolbar,
            text="Добавить документы",
            command=self.add_files,
            height=2
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            toolbar,
            text="Удалить выбранные",
            command=self.remove_selected,
            height=2
        ).pack(side="left", padx=8)

        tk.Button(
            toolbar,
            text="Очистить список",
            command=self.clear_files,
            height=2
        ).pack(side="left", padx=8)

        self.file_list = tk.Listbox(
            root,
            selectmode=tk.EXTENDED,
            font=("Arial", 10)
        )
        self.file_list.pack(fill="both", expand=True, padx=18, pady=10)

        output_frame = tk.Frame(root)
        output_frame.pack(fill="x", padx=18, pady=4)

        tk.Label(
            output_frame,
            text="Папка для подготовленных копий:"
        ).pack(anchor="w")

        path_frame = tk.Frame(output_frame)
        path_frame.pack(fill="x", pady=5)

        self.output_entry = tk.Entry(path_frame)
        self.output_entry.insert(0, self.output_dir)
        self.output_entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            path_frame,
            text="Обзор...",
            command=self.choose_output
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            root,
            text="Подготовить копии документов",
            command=self.prepare_files,
            height=2,
            bg="#176B45",
            fg="white"
        ).pack(fill="x", padx=18, pady=(8, 12))

        self.status = tk.Label(
            root,
            text="Готово к работе. Добавьте документы.",
            anchor="w"
        )
        self.status.pack(fill="x", padx=18, pady=(0, 12))

    def add_files(self):
        selected = filedialog.askopenfilenames(
            title="Выберите документы",
            filetypes=[
                ("Документы", "*.pdf *.doc *.docx *.xls *.xlsx *.rtf"),
                ("Все файлы", "*.*")
            ]
        )

        for name in selected:
            if name not in self.files:
                self.files.append(name)
                self.file_list.insert(tk.END, name)

        self.status.config(
            text=f"Документов в списке: {len(self.files)}"
        )

    def remove_selected(self):
        indexes = list(self.file_list.curselection())

        for index in reversed(indexes):
            self.file_list.delete(index)
            del self.files[index]

        self.status.config(
            text=f"Документов в списке: {len(self.files)}"
        )

    def clear_files(self):
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.status.config(text="Список очищен.")

    def choose_output(self):
        folder = filedialog.askdirectory(
            title="Выберите папку для подготовленных копий"
        )

        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def prepare_files(self):
        if not self.files:
            messagebox.showwarning(
                APP_NAME,
                "Сначала добавьте хотя бы один документ."
            )
            return

        destination = self.output_entry.get().strip()

        if not destination:
            messagebox.showwarning(
                APP_NAME,
                "Выберите папку для сохранения."
            )
            return

        try:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_dir = Path(destination) / f"Пакет_{stamp}"
            batch_dir.mkdir(parents=True, exist_ok=False)

            copied = 0

            for source in self.files:
                source_path = Path(source)

                if not source_path.is_file():
                    continue

                target = batch_dir / source_path.name

                if target.exists():
                    target = batch_dir / (
                        f"{source_path.stem}_{copied + 1}"
                        f"{source_path.suffix}"
                    )

                shutil.copy2(source_path, target)
                copied += 1

            if copied == 0:
                messagebox.showwarning(
                    APP_NAME,
                    "Не удалось найти доступные файлы."
                )
                return

            self.status.config(
                text=f"Подготовлено копий: {copied}. Папка: {batch_dir}"
            )

            messagebox.showinfo(
                APP_NAME,
                "Подготовка завершена.\n\n"
                f"Создано копий: {copied}\n\n"
                f"Папка:\n{batch_dir}\n\n"
                "Оригиналы не изменены. Документы не подписывались."
            )

        except Exception as error:
            messagebox.showerror(
                APP_NAME,
                f"Не удалось подготовить документы:\n{error}"
            )


def main():
    root = tk.Tk()
    QuickSignApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
