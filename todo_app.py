import streamlit as st
import requests

# Sheety API URL
SHEETY_URL = "https://api.sheety.co/4f6df431532083f87864de6d23e2825f/todoApp/sheet1"

st.title("📝 Cloud To-Do List (Google Sheets)")

# Function to get tasks from Google Sheet
def get_tasks():
    response = requests.get(SHEETY_URL)
    if response.status_code == 200:
        return response.json()["sheet1"]
    else:
        st.error("Failed to fetch tasks")
        return []

# Function to add a new task
def add_task(task):
    new_task = {
        "sheet1": {
            "task": task,
            "done": False
        }
    }
    response = requests.post(SHEETY_URL, json=new_task)
    if response.status_code != 200:
        st.error("Failed to add task")

# Function to update a task's 'done' status
def update_task(task_id, done):
    update_data = {
        "sheet1": {
            "done": done
        }
    }
    url = f"{SHEETY_URL}/{task_id}"
    response = requests.put(url, json=update_data)
    if response.status_code != 200:
        st.error("Failed to update task")

# Function to clear completed tasks
def delete_task(task_id):
    url = f"{SHEETY_URL}/{task_id}"
    response = requests.delete(url)
    if response.status_code != 200:
        st.error("Failed to delete task")

# Add new task
new_task = st.text_input("Add a new task:")
if st.button("➕ Add Task"):
    if new_task.strip():
        add_task(new_task.strip())
        st.experimental_rerun()
    else:
        st.warning("Task cannot be empty!")

st.subheader("Your Tasks:")
tasks = get_tasks()
for task in tasks:
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    with col1:
        checked = st.checkbox("", value=task["done"], key=task["id"])
        if checked != task["done"]:
            update_task(task["id"], checked)
            st.experimental_rerun()
    with col2:
        st.markdown(f"{'✅' if task['done'] else '🔲'} {task['task']}")
    with col3:
        if task["done"]:
            if st.button("🗑️", key=f"delete_{task['id']}"):
                delete_task(task["id"])
                st.experimental_rerun()
