import streamlit as st
import requests
from datetime import datetime

# Google Sheet API URL (Sheety)
SHEETY_URL = "https://api.sheety.co/4f6df431532083f87864de6d23e2825f/todoApp/sheet1"

st.title("🧠 Cloud To-Do List + Planner")

# --------------- Helper Functions ---------------

def get_tasks():
    response = requests.get(SHEETY_URL)
    if response.status_code == 200:
        return response.json()["sheet1"]
    else:
        st.error("Error fetching tasks")
        return []

def add_task(task, category, due, priority):
    new_task = {
        "sheet1": {
            "task": task,
            "done": False,
            "category": category,
            "due": due,
            "priority": priority
        }
    }
    response = requests.post(SHEETY_URL, json=new_task)
    if response.status_code != 200:
        st.error("Failed to add task")

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

def delete_task(task_id):
    url = f"{SHEETY_URL}/{task_id}"
    response = requests.delete(url)
    if response.status_code != 200:
        st.error("Failed to delete task")

# --------------- UI: Add New Task ---------------

st.subheader("➕ Add a New Task")

with st.form("add_task_form"):
    col1, col2 = st.columns(2)
    with col1:
        task = st.text_input("Task")
        category = st.selectbox("Category", ["Work", "Personal", "Study", "Other"])
    with col2:
        due = st.date_input("Due Date", value=datetime.today())
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    submit = st.form_submit_button("Add Task")

    if submit:
        if task.strip() != "":
            add_task(task.strip(), category, str(due), priority)
            st.success("Task added!")
            st.rerun()
        else:
            st.warning("Task title can't be empty.")

# --------------- UI: Display Tasks ---------------

st.subheader("🗂️ Your Tasks")
tasks = get_tasks()

if tasks:
    for task in tasks:
        col1, col2, col3, col4 = st.columns([0.05, 0.5, 0.3, 0.15])
        with col1:
            checked = st.checkbox("", value=task["done"], key=task["id"])
            if checked != task["done"]:
                update_task(task["id"], checked)
                st.rerun()
        with col2:
            st.markdown(
                f"{'✅' if task['done'] else '🔲'} **{task['task']}**  \n"
                f"📁 *{task.get('category', 'N/A')}* | 🗓️ *{task.get('due', 'N/A')}*"
            )
        with col3:
            priority = task.get("priority", "Medium")
            emoji = "🔥" if priority == "High" else ("💧" if priority == "Low" else "⚡")
            st.markdown(f"**Priority:** {emoji} {priority}")
        with col4:
            if task["done"]:
                if st.button("🗑️", key=f"delete_{task['id']}"):
                    delete_task(task["id"])
                    st.rerun()
else:
    st.info("No tasks yet. Start adding some above!")

