from mmod.app import App

app = App()
app.init_tasks_buttons(tasks=['task1', 'task2', 'task3', 'task4'])

app.mainloop()
